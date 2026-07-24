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

    # ── 4. 什么都没命中 → unknown ──
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

    elif verdict == "ambiguous" or verdict == "unknown":
        # ── 黄色提示框 ──
        st.markdown(
            f'<div class="warning-box" style="background:#fff3cd; border-color:#ffc107;">'
            f'<span style="font-size:1.1rem; font-weight:600;">🔶 会计常识预检</span><br>'
            f'{message}'
            f"</div>",
            unsafe_allow_html=True,
        )

        # ── 推荐科目选择 ──
        st.markdown("**📌 请选择您认为合适的科目方向：**")

        # 构建选项
        options = []
        for r in recommendations:
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
        selected_account = selected.split("（")[0] if "（" in selected else selected

        # 存入 session_state 供后续使用
        st.session_state["manual_account_selected"] = selected_account
        st.session_state["capitalization_verdict"] = verdict

        # ── 确认按钮 ──
        if st.button("✅ 确认选择此科目方向", key="confirm_capitalization", type="primary"):
            st.session_state["capitalization_confirmed"] = True
            st.success(f"✅ 已确认选择：{selected_account}")
            return False  # 用户已确认，可以继续

        return True  # 需要手动干预（用户还没确认）

    return False
