"""
会计常识预检逻辑 —— 资本化/费用化判断 + 模糊地带检测 + 强制手动干预

功能：
1. 区分"资产型"与"费用型"业务（黑/白名单原则）
2. 模糊匹配 → 黄色提示 + 推荐可选科目
3. 强制手动干预入口
"""

import re

# ─── 黑名单：强制费用化关键词 ──────────────────────────────
# 无论金额多大，命中这些词就标记为费用化支出
EXPENSE_FORCE_KEYWORDS = [
    "维修", "修理", "保养", "更换配件", "更换零件",
    "清理", "清洁", "清洗", "打扫",
    "维护", "检修", "年检",
    "加固", "补修", "翻新", "改造（非资本化）",
]

# ─── 白名单：触发资本化判断的关键词 ────────────────────────
CAPITALIZE_KEYWORDS = [
    "购买", "新增", "新购", "建造", "购置",
    "购入", "采购（固定资产）", "自建", "修建",
    "安装（需资本化）", "扩建", "新建",
]

# ─── 模糊地带关键词（命中任意一个即触发黄色提示） ──────────
# 这些词既不像费用化也不像资本化，需要人工判断
AMBIGUOUS_KEYWORDS = [
    "消防", "检测", "检测费", "评估费", "审计费", "咨询费",
    "认证费", "许可费", "备案费", "登记费",
    "手续费", "服务费（非明确期间费用）",
    "调试费", "测试费", "验收费",
]

# ─── 模糊地带的推荐科目映射 ────────────────────────────────
AMBIGUOUS_RECOMMENDATIONS = {
    "消防": {
        "expense": "管理费用-消防维护费",
        "capital": "在建工程-消防工程",
        "note": "日常消防维护→费用化；新建项目消防工程→资本化",
    },
    "检测": {
        "expense": "管理费用-检测费",
        "capital": "在建工程-检测费",
        "note": "日常检测→费用化；工程验收检测→资本化",
    },
    "评估": {
        "expense": "管理费用-评估费",
        "capital": "在建工程-评估费",
        "note": "日常评估→费用化；资产购建评估→资本化",
    },
    "审计": {
        "expense": "管理费用-审计费",
        "capital": None,
        "note": "审计费通常全部费用化",
    },
    "认证": {
        "expense": "管理费用-认证费",
        "capital": "无形资产-认证资质",
        "note": "费用化；若形成长期资质可资本化",
    },
    "咨询": {
        "expense": "管理费用-咨询费",
        "capital": "在建工程-咨询费",
        "note": "日常咨询→费用化；项目可研咨询→资本化",
    },
    "许可": {
        "expense": "管理费用-许可费",
        "capital": "无形资产-特许权",
        "note": "短期许可→费用化；长期特许权→资本化",
    },
    "登记": {
        "expense": "管理费用-登记费",
        "capital": None,
        "note": "登记费通常全部费用化",
    },
    "备案": {
        "expense": "管理费用-备案费",
        "capital": None,
        "note": "备案费通常全部费用化",
    },
    "调试": {
        "expense": "管理费用-调试费",
        "capital": "在建工程-调试费",
        "note": "日常调试→费用化；设备安装调试→资本化",
    },
    "测试": {
        "expense": "管理费用-测试费",
        "capital": "在建工程-测试费",
        "note": "日常测试→费用化；系统验收测试→资本化",
    },
    "验收": {
        "expense": "管理费用-验收费",
        "capital": "在建工程-验收费",
        "note": "日常验收→费用化；工程验收→资本化",
    },
}


def check_capitalization(text: str) -> dict:
    """
    核心预检函数：判断一笔支出应该费用化还是资本化。

    返回字典：
    {
        "verdict": "expense" | "capital" | "ambiguous" | "unknown",
        "confidence": "high" | "medium" | "low",
        "matched_keywords": [...],
        "message": str,           # 展示给用户的提示
        "recommendations": [...],  # 推荐科目列表
        "force_manual": bool,      # 是否强制手动干预
    }
    """
    text_lower = text.lower()

    # ── 0. 特殊业务：自产产品发福利（视同销售，不走常规费用化/资本化判断） ──
    if "自产" in text and ("福利" in text or "发给员工" in text or "发放" in text):
        return {
            "verdict": "expense",
            "confidence": "high",
            "matched_keywords": ["自产", "福利"],
            "message": (
                f"✅ 系统判定：**自产产品发福利（视同销售）**\n\n"
                f"检测到关键词「自产」「福利」，根据会计准则：\n"
                f"1. 自产产品发福利视同销售，按市场售价确认收入并计提增值税销项税额\n"
                f"2. 同时按成本价结转库存商品\n"
                f"3. 借方计入职工福利费（市场售价+销项税）"
            ),
            "recommendations": [
                {"account": "管理费用-职工福利费", "type": "expense", "note": "自产产品发福利（视同销售）"},
            ],
            "force_manual": False,
        }

    # ── 0.5. 非费用/非资本类业务（投资、借款、收款、分配利润等）──
    # 这些业务不涉及费用化/资本化判断，直接放行让规则引擎处理
    NON_CAPITAL_EXPENSE_KEYWORDS = [
        "投资", "注资", "实收资本", "资本公积", "股东",
        "借款", "贷款", "借入",
        "收款", "收到货款", "回款",
        "分配利润", "分红", "股利",
        "结转",
        "计提",  # 涵盖计提工资、计提折旧、计提社保等所有计提类业务
        "完工产品", "完工成本",
        "城建税", "教育费附加",
    ]
    for kw in NON_CAPITAL_EXPENSE_KEYWORDS:
        if kw in text:
            return {
                "verdict": "expense",
                "confidence": "high",
                "matched_keywords": [kw],
                "message": (
                    f"✅ 系统判定：**非费用化/资本化业务，直接匹配规则库**\n\n"
                    f"检测到关键词「{kw}」，该业务不涉及费用化/资本化判断，"
                    f"系统将直接匹配规则库生成推荐凭证。"
                ),
                "recommendations": [],
                "force_manual": False,
            }

    # ── 1. 检查黑名单（强制费用化） ──
    matched_expense = []
    for kw in EXPENSE_FORCE_KEYWORDS:
        if kw in text:
            matched_expense.append(kw)

    if matched_expense:
        return {
            "verdict": "expense",
            "confidence": "high",
            "matched_keywords": matched_expense,
            "message": (
                f"✅ 系统判定：**费用化支出**\n\n"
                f"检测到关键词「{'」「'.join(matched_expense)}」，"
                f"根据会计准则，维修保养类支出无论金额大小均应费用化处理。"
            ),
            "recommendations": [
                {"account": "管理费用-维修费", "type": "expense", "note": "日常维修保养费用"},
                {"account": "管理费用-维护费", "type": "expense", "note": "设备/系统维护费用"},
            ],
            "force_manual": False,
        }

    # ── 2. 检查白名单（触发资本化判断） ──
    matched_capital = []
    for kw in CAPITALIZE_KEYWORDS:
        if kw in text:
            matched_capital.append(kw)

    if matched_capital:
        # 提取金额判断是否达到资本化门槛
        amount = _extract_amount_for_check(text)
        if amount is not None and amount >= 5000:
            return {
                "verdict": "capital",
                "confidence": "high",
                "matched_keywords": matched_capital,
                "message": (
                    f"✅ 系统判定：**建议资本化处理**\n\n"
                    f"检测到关键词「{'」「'.join(matched_capital)}」，"
                    f"金额 ¥{amount:,.2f} ≥ ¥5,000.00，符合固定资产资本化条件。"
                    f"建议计入固定资产科目，按月计提折旧。"
                ),
                "recommendations": [
                    {"account": "固定资产", "type": "capital", "note": f"金额 ¥{amount:,.2f}，建议资本化"},
                    {"account": "管理费用-办公设备购置", "type": "expense", "note": "若不符合固定资产确认条件"},
                ],
                "force_manual": False,
            }
        elif amount is not None:
            return {
                "verdict": "expense",
                "confidence": "medium",
                "matched_keywords": matched_capital,
                "message": (
                    f"⚠️ 系统判定：**建议费用化处理**\n\n"
                    f"检测到关键词「{'」「'.join(matched_capital)}」，"
                    f"但金额 ¥{amount:,.2f} < ¥5,000.00，"
                    f"低于固定资产确认门槛，建议直接费用化处理。"
                ),
                "recommendations": [
                    {"account": "管理费用-办公费", "type": "expense", "note": "小额资产购置，直接费用化"},
                ],
                "force_manual": False,
            }
        else:
            # 有购买关键词但无法提取金额 → 模糊
            return {
                "verdict": "ambiguous",
                "confidence": "low",
                "matched_keywords": matched_capital,
                "message": (
                    f"⚠️ **系统无法确定此支出应费用化还是资本化**\n\n"
                    f"检测到购买类关键词「{'」「'.join(matched_capital)}」，"
                    f"但无法提取金额。请手动确认金额是否达到资本化门槛（¥5,000.00）。"
                ),
                "recommendations": [
                    {"account": "固定资产", "type": "capital", "note": "金额≥¥5,000 且使用寿命超过一年"},
                    {"account": "管理费用-办公费", "type": "expense", "note": "金额<¥5,000 或使用寿命短"},
                ],
                "force_manual": True,
            }

    # ── 3. 检查模糊地带关键词 ──
    matched_ambiguous = []
    for kw in AMBIGUOUS_KEYWORDS:
        if kw in text:
            matched_ambiguous.append(kw)

    if matched_ambiguous:
        # 查找推荐科目
        recs = []
        for mk in matched_ambiguous:
            for amb_key, amb_val in AMBIGUOUS_RECOMMENDATIONS.items():
                if amb_key in mk or mk in amb_key:
                    if amb_val["expense"]:
                        recs.append({
                            "account": amb_val["expense"],
                            "type": "expense",
                            "note": amb_val["note"],
                        })
                    if amb_val.get("capital"):
                        recs.append({
                            "account": amb_val["capital"],
                            "type": "capital",
                            "note": amb_val["note"],
                        })

        # 去重
        seen = set()
        unique_recs = []
        for r in recs:
            if r["account"] not in seen:
                seen.add(r["account"])
                unique_recs.append(r)

        if not unique_recs:
            unique_recs = [
                {"account": "管理费用-其他费用", "type": "expense", "note": "费用化处理"},
                {"account": "无形资产/在建工程", "type": "capital", "note": "若形成长期资产"},
            ]

        return {
            "verdict": "ambiguous",
            "confidence": "low",
            "matched_keywords": matched_ambiguous,
            "message": (
                f"⚠️ **系统无法确定此支出是费用化还是资本化**\n\n"
                f"检测到关键词「{'」「'.join(matched_ambiguous)}」，"
                f"该业务性质介于费用化与资本化之间。"
                f"建议您手动选择科目方向："
            ),
            "recommendations": unique_recs,
            "force_manual": True,
        }

    # ── 4. 什么都没命中 → 尝试模糊匹配 mock_data 中的科目 ──
    fuzzy = _fuzzy_match_account(text)
    if fuzzy is not None:
        return {
            "verdict": "fuzzy_match",
            "confidence": "low",
            "matched_keywords": [],
            "message": (
                f"⚠️ **系统未精确匹配，已根据业务描述模糊推荐科目**\n\n"
                f"未检测到明确的费用化或资本化关键词，"
                f"但根据业务描述语义，推荐入账方向为「{fuzzy}」。"
            ),
            "recommendations": [
                {"account": fuzzy, "type": "fuzzy", "note": "模糊匹配推荐"},
                {"account": "管理费用-其他费用", "type": "expense", "note": "费用化处理"},
                {"account": "固定资产/无形资产", "type": "capital", "note": "若符合资产确认条件"},
            ],
            "force_manual": False,
            "fuzzy_account": fuzzy,
        }

    # ── 5. 完全找不到任何关联 → 弹选择题 ──
    return {
        "verdict": "unknown",
        "confidence": "low",
        "matched_keywords": [],
        "message": (
            "⚠️ **系统无法确定此支出是费用化还是资本化**\n\n"
            "未检测到明确的费用化或资本化关键词，"
            "建议您手动选择科目（已为您推荐常用科目）。"
        ),
        "recommendations": [
            {"account": "管理费用-其他费用", "type": "expense", "note": "费用化处理（默认推荐）"},
            {"account": "固定资产/无形资产", "type": "capital", "note": "若符合资产确认条件"},
        ],
        "force_manual": True,
    }


# ─── 从 mock_data 提取所有唯一借方科目 ─────────────────────
def _get_all_debit_accounts():
    """从 MOCK_SCENARIOS 提取所有唯一的借方科目"""
    try:
        from mock_data import MOCK_SCENARIOS
        seen = set()
        accounts = []
        for s in MOCK_SCENARIOS:
            acct = s["debit_account"]
            if acct not in seen:
                seen.add(acct)
                accounts.append(acct)
        return accounts
    except Exception:
        return []


# ─── 科目关键词映射（用于模糊匹配） ─────────────────────────
ACCOUNT_KEYWORD_MAP = {
    "管理费用-业务招待费": ["请客", "吃饭", "招待", "餐饮", "宴请", "餐费", "客户"],
    "管理费用-办公费": ["办公用品", "文具", "打印纸", "笔", "墨盒", "硒鼓", "办公耗材", "办公"],
    "管理费用-差旅费": ["差旅", "出差", "交通", "住宿", "机票", "火车票", "高铁", "打车", "出租车"],
    "管理费用-租赁费": ["房租", "租金", "租赁", "办公室租", "房屋租赁", "租房"],
    "管理费用-水电费": ["水电", "水电费", "物业", "物业费", "电费", "水费"],
    "管理费用-快递费": ["快递", "邮寄", "邮费", "快递费"],
    "管理费用-职工教育经费": ["培训", "培训费", "教育", "职工教育", "进修"],
    "管理费用-中介服务费": ["咨询", "咨询费", "审计", "审计费", "律师", "律师费", "顾问"],
    "管理费用-会议费": ["会议", "会议费", "研讨会", "论坛"],
    "管理费用-维修费": ["维修", "修理", "修缮", "维修费", "修理费", "保养"],
    "管理费用-折旧费": ["折旧", "计提折旧", "累计折旧"],
    "管理费用-工资": ["计提工资", "工资计提"],
    "管理费用-软件服务费": ["软件", "软件费", "SaaS", "云服务", "会员"],
    "管理费用-消防维护费": ["消防"],
    "管理费用-检测费": ["检测"],
    "管理费用-评估费": ["评估"],
    "管理费用-认证费": ["认证"],
    "管理费用-许可费": ["许可"],
    "管理费用-登记费": ["登记"],
    "管理费用-调试费": ["调试"],
    "管理费用-测试费": ["测试"],
    "管理费用-验收费": ["验收"],
    "固定资产-电子设备": ["电脑", "笔记本", "台式机", "服务器", "显示器", "空调", "冰箱", "家电", "电器"],
    "固定资产-办公家具": ["办公桌", "办公椅", "文件柜", "家具", "办公家具", "沙发"],
    "固定资产-运输设备": ["汽车", "车辆", "轿车", "货车", "机动车", "购车"],
    "固定资产-机器设备": ["机器", "设备", "生产设备", "机床", "仪器"],
    "应付职工薪酬-工资": ["工资", "薪酬", "薪资", "奖金", "发工资", "工资表"],
    "应付职工薪酬-社保公积金": ["社保", "五险", "养老保险", "医疗保险", "失业保险", "公积金", "住房公积金"],
    "应付职工薪酬-职工福利费": ["福利", "福利费", "过节", "节日福利", "体检", "员工福利"],
    "销售费用-广告费": ["广告", "推广", "宣传", "营销", "广告费", "推广费", "宣传费"],
    "销售费用-运输费": ["运输", "运费", "物流费", "配送", "送货"],
    "原材料": ["原材料", "材料", "采购材料", "进货", "买材料", "采购原料"],
    "库存商品": ["库存商品", "商品", "采购商品", "进货商品", "买货"],
    "周转材料-包装物": ["包装", "包装物", "包装箱", "包装盒"],
    "银行存款": ["货款", "收到货款", "收款", "回款", "客户付款", "收到钱", "收货款", "销售"],
    "应交税费": ["增值税", "交税", "缴税", "所得税", "附加税", "印花税", "税费"],
    "财务费用-手续费": ["利息", "银行手续费", "手续费", "转账费", "账户管理费"],
    "财务费用-利息收入": ["利息收入", "存款利息"],
    "营业外支出-捐赠支出": ["捐赠", "捐款", "赞助", "公益"],
    "营业外支出-罚款支出": ["罚款", "罚金", "违约金", "赔偿", "滞纳金"],
    "主营业务收入": ["销售商品", "卖货", "出售", "销售收入", "主营业务收入"],
}


def _fuzzy_match_account(text: str):
    """
    模糊匹配：用输入文本中的关键词与 ACCOUNT_KEYWORD_MAP 比对，
    返回匹配度最高的科目名称。如果完全匹配不到，返回 None。
    """
    from rule_engine import _strip_punctuation, _clean_text

    # 清洗文本
    cleaned = _clean_text(_strip_punctuation(text)).strip()
    if len(cleaned) <= 2:
        return None

    best_account = None
    best_score = 0

    for account, keywords in ACCOUNT_KEYWORD_MAP.items():
        score = 0
        for kw in keywords:
            if kw in cleaned or kw in text:
                score += 1
        if score > best_score:
            best_score = score
            best_account = account

    # 至少命中 1 个关键词才算匹配
    if best_score >= 1:
        return best_account
    return None


def _extract_amount_for_check(text: str):
    """
    从文本中提取金额（用于资本化门槛判断）。
    支持格式：8000元、8000.00元、8000 元、花了8000、8000块钱
    """
    patterns = [
        r"(\d+\.?\d*)\s*万元",
        r"(\d+\.?\d*)\s*万",
        r"(\d+\.?\d*)\s*元",
        r"花了\s*(\d+\.?\d*)",
        r"(\d+\.?\d*)\s*块钱",
        r"(\d+\.?\d*)",
    ]
    for pat in patterns:
        match = re.search(pat, text)
        if match:
            val = float(match.group(1))
            # 如果是"万元"单位，乘以10000
            if "万" in pat and "元" not in pat:
                val *= 10000
            return val
    return None


def render_capitalization_ui(verdict_result: dict):
    """
    生成 Streamlit UI 组件，展示预检结果。
    返回 True 表示需要强制手动干预，False 表示可以继续自动推荐。
    """
    import streamlit as st

    verdict = verdict_result["verdict"]
    confidence = verdict_result["confidence"]
    message = verdict_result["message"]
    recommendations = verdict_result["recommendations"]
    force_manual = verdict_result["force_manual"]

    # ── 展示判定结果 ──
    if verdict == "expense" and confidence == "high":
        st.success(message)
        return False  # 不需要手动干预

    elif verdict == "capital" and confidence == "high":
        st.success(message)
        return False  # 不需要手动干预

    elif verdict == "expense" and confidence == "medium":
        st.warning(message)
        return False

    elif verdict == "fuzzy_match":
        # ── 黄色提醒框（模糊匹配，不弹选择题） ──
        fuzzy_account = verdict_result.get("fuzzy_account", "")
        st.markdown(
            f'<div class="warning-box" style="background:#fff3cd; border-color:#ffc107;">'
            f'<span style="font-size:1.1rem; font-weight:600;">🔶 会计常识预检</span><br>'
            f'{message}'
            f"</div>",
            unsafe_allow_html=True,
        )
        # 存入 session_state 供后续使用
        st.session_state["manual_account_selected"] = fuzzy_account
        st.session_state["capitalization_verdict"] = verdict
        st.session_state["capitalization_confirmed"] = True
        return False  # 不需要弹选择题，直接继续

    elif verdict == "ambiguous" or verdict == "unknown":
        # ── 如果用户已经确认过选择，直接跳过弹窗 ──
        if st.session_state.get("capitalization_confirmed", False):
            return False

        # ── 黄色提示框 ──
        st.markdown(
            f'<div class="warning-box" style="background:#fff3cd; border-color:#ffc107;">'
            f'<span style="font-size:1.1rem; font-weight:600;">🔶 会计常识预检</span><br>'
            f'{message}'
            f"</div>",
            unsafe_allow_html=True,
        )

        # ── 推荐科目选择（优化选项文字） ──
        st.markdown("**📌 请选择您认为合适的科目方向：**")

        # 构建选项
        options = []
        for r in recommendations:
            if r["type"] == "expense":
                label = f"推荐入账方向：{r['account']}（推荐）"
            elif r["type"] == "capital":
                label = f"推荐入账方向：{r['account']}"
            else:
                label = f"{r['account']}（{r['note']}）"
            options.append(label)

        # 默认选中第一个
        selected = st.radio(
            "选择科目方向",
            options=options,
            key="capitalization_choice",
            index=0,
        )

        # 从选中项提取科目名
        selected_account = selected.split("：")[-1].split("（")[0].strip() if "：" in selected else selected.split("（")[0]

        # 存入 session_state 供后续使用
        st.session_state["manual_account_selected"] = selected_account
        st.session_state["capitalization_verdict"] = verdict

        # ── 确认按钮 ──
        if st.button("✅ 确认选择此科目方向", key="confirm_capitalization", type="primary"):
            st.session_state["capitalization_confirmed"] = True
            st.session_state["voucher_confirmed"] = True  # 跳过后续的"确认并生成凭证"按钮
            st.rerun()  # 立即 rerun，让页面重新执行并跳过弹窗
            return False

        return True  # 需要手动干预（用户还没确认）

    return False
