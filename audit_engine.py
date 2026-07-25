"""
智能审计引擎 —— 自动校验会计分录的合规性
为每笔凭证生成：风险等级 + 审计说明 + 合规建议
"""
from mock_data import ACCOUNT_CHART


def get_account_nature(account_name: str) -> str:
    """获取科目性质（借/贷），支持明细科目"""
    base = account_name.split("-")[0]
    for key, info in ACCOUNT_CHART.items():
        if account_name.startswith(key) or base == key:
            return info["nature"]
    return "未知"


def get_account_category(account_name: str) -> str:
    """获取科目分类"""
    base = account_name.split("-")[0]
    for key, info in ACCOUNT_CHART.items():
        if account_name.startswith(key) or base == key:
            return info["category"]
    return "未知"


# ═══════════════════════════════════════════════
# 审计规则数据库
# ═══════════════════════════════════════════════

# 科目互斥：不应同时出现的科目对
ACCOUNT_CONFLICTS = [
    (["管理费用", "销售费用"], ["在建工程"], "费用化 vs 资本化",
     "费用科目与在建工程同时出现，可能存在资本化/费用化混淆，请确认该支出是否应计入资产成本。"),
    (["管理费用-业务招待费"], ["主营业务成本"], "招待费 vs 成本",
     "业务招待费属于期间费用，不应计入主营业务成本。"),
    (["管理费用-工资"], ["生产成本-直接人工"], "工资归集冲突",
     "同一笔工资不应同时计入管理费用和生产成本，请按员工所属部门分别归集。"),
    (["固定资产"], ["管理费用-办公费"], "资本化 vs 费用化",
     "固定资产与办公费同时出现，可能存在将应费用化的小额支出错误资本化的风险（单价<5000元应费用化）。"),
    (["累计折旧"], ["固定资产"], "正常配对",
     None),  # 不冲突，正常配对
]

# 方向约束：借/贷必须符合科目性质
DIRECTION_RULES = {
    "资产类": {"normal_dr": "增加", "normal_cr": "减少", "abnormal_warning": "资产类科目正常应在借方增加，贷方出现可能表示处置/折旧/减值，请确认。"},
    "负债类": {"normal_dr": "减少", "normal_cr": "增加", "abnormal_warning": "负债类科目正常应在贷方增加，借方出现表示偿还债务，请确认。"},
    "所有者权益类": {"normal_dr": "减少", "normal_cr": "增加", "abnormal_warning": "权益类科目正常在贷方，借方出现可能表示减资或亏损。"},
    "成本类": {"normal_dr": "增加", "normal_cr": "减少", "abnormal_warning": "成本类科目正常在借方归集，贷方一般为结转。"},
    "损益类": {"normal_dr": "费用增加", "normal_cr": "收入增加", "abnormal_warning": "收入类科目在贷方，费用类在借方。"},
}

# 税务风险知识库
TAX_RISK_RULES = [
    {
        "keywords": ["业务招待费"],
        "risk": "企业所得税汇算清缴时，业务招待费按实际发生额的60%扣除，最高不超过当年销售收入的5‰。",
        "severity": "medium",
    },
    {
        "keywords": ["广告费", "业务宣传费"],
        "risk": "广告费和业务宣传费不超过当年销售收入15%的部分准予扣除，超过部分可结转以后年度扣除。",
        "severity": "medium",
    },
    {
        "keywords": ["职工福利费"],
        "risk": "职工福利费不超过工资薪金总额14%的部分准予税前扣除，超出部分需纳税调增。",
        "severity": "medium",
    },
    {
        "keywords": ["职工教育经费"],
        "risk": "职工教育经费不超过工资薪金总额8%的部分准予税前扣除，超过部分准予结转。",
        "severity": "medium",
    },
    {
        "keywords": ["工会经费"],
        "risk": "工会经费按工资总额2%计提，需取得工会专用收据方可税前扣除。",
        "severity": "low",
    },
    {
        "keywords": ["捐赠", "公益性捐赠"],
        "risk": "公益性捐赠不超过年度利润总额12%的部分准予税前扣除，超过部分可结转3年。",
        "severity": "medium",
    },
    {
        "keywords": ["研发费用", "研发支出"],
        "risk": "符合条件的研发费用可享受加计扣除政策（制造业100%，其他行业75%）。请确认研发项目是否符合加计扣除条件。",
        "severity": "high",
    },
    {
        "keywords": ["固定资产", "500万"],
        "risk": "单价不超过500万元的设备器具可一次性税前扣除（2027年底前）。",
        "severity": "low",
    },
    {
        "keywords": ["坏账准备", "信用减值损失"],
        "risk": "坏账准备计提需符合税法规定的条件方可税前扣除，一般需实际发生损失才能扣除。",
        "severity": "medium",
    },
    {
        "keywords": ["存货跌价准备", "资产减值损失"],
        "risk": "存货跌价准备在计提时不得税前扣除，需做纳税调增；实际损失发生时方可扣除。",
        "severity": "medium",
    },
    {
        "keywords": ["辞退福利", "经济补偿"],
        "risk": "辞退福利在满足条件时一次性计入当期损益，企业所得税处理需关注合理性。",
        "severity": "low",
    },
    {
        "keywords": ["佣金", "手续费 支出"],
        "risk": "佣金支出不超过服务收入5%的部分准予税前扣除（保险企业为18%）。",
        "severity": "medium",
    },
]

# 金额合理性规则
AMOUNT_RULES = [
    {
        "check": lambda d, c, amt: any("累计折旧" in x for x in [d, c]) and any("固定资产" in x for x in [d, c]),
        "rule": "折旧/固定资产配对出现，金额合理",
        "severity": "info",
    },
    {
        "check": lambda d, c, amt: ("减值" in d or "减值" in c) and amt > 1000000,
        "rule": "大额减值（>100万），建议确认减值测试依据是否充分",
        "severity": "high",
    },
    {
        "check": lambda d, c, amt: ("业务招待" in d or "业务招待" in c) and amt > 2000,
        "rule": "单笔招待费>2000元，建议确认招待事由及人员",
        "severity": "low",
    },
]


# ═══════════════════════════════════════════════
# 审计主函数
# ═══════════════════════════════════════════════

def audit_voucher(debit: str, credit: str, amount: float, description: str = "", source: str = "rule") -> dict:
    """
    对一笔会计分录进行全面审计。
    返回: { "risk_level": "high/medium/low/safe", "findings": [...], "tax_risks": [...], "confidence": 0-100 }
    """
    findings = []
    tax_risks = []

    # ── 1. 方向合规性检查 ──
    debit_nature = get_account_nature(debit)
    credit_nature = get_account_nature(credit)
    debit_cat = get_account_category(debit)
    credit_cat = get_account_category(credit)

    if debit_nature == "贷" and "折旧" not in debit and "摊销" not in debit and "准备" not in debit:
        findings.append({
            "type": "方向异常",
            "severity": "medium",
            "message": f"「{debit}」科目性质为贷方，出现在借方可能异常。贷方科目通常表示负债/权益/收入增加。",
            "suggestion": "请确认该科目确实应该在借方。",
        })

    if credit_nature == "借" and "折旧" not in credit and "摊销" not in credit and "准备" not in credit:
        findings.append({
            "type": "方向异常",
            "severity": "medium",
            "message": f"「{credit}」科目性质为借方，出现在贷方可能异常。借方科目通常表示资产/费用增加。",
            "suggestion": "请确认该科目确实应该在贷方。",
        })

    # ── 2. 科目互斥检查 ──
    for dr_keywords, cr_keywords, conflict_type, msg in ACCOUNT_CONFLICTS:
        if msg is None:
            continue
        dr_match = any(kw in debit for kw in dr_keywords)
        cr_match = any(kw in credit for kw in cr_keywords)
        if dr_match and cr_match:
            findings.append({
                "type": f"科目冲突：{conflict_type}",
                "severity": "high",
                "message": msg,
                "suggestion": "建议逐笔核对每项支出的性质，确保费用化/资本化分类正确。",
            })

    # ── 3. 税务风险扫描 ──
    combined = debit + credit + description
    for rule in TAX_RISK_RULES:
        if any(kw in combined for kw in rule["keywords"]):
            tax_risks.append({
                "type": f"税务风险：{rule['keywords'][0]}",
                "severity": rule["severity"],
                "message": rule["risk"],
            })

    # ── 4. 金额合理性 ──
    for rule in AMOUNT_RULES:
        if rule["check"](debit, credit, amount):
            if rule["severity"] != "info":
                findings.append({
                    "type": "金额异常",
                    "severity": rule["severity"],
                    "message": rule["rule"],
                })

    # ── 5. 置信度评分 ──
    confidence = 95 if source == "rule" else 70 if source == "scenario" else 60
    total_issues = len(findings) + len(tax_risks)
    if total_issues > 0:
        confidence = max(50, confidence - total_issues * 5)

    # ── 6. 风险等级 ──
    severities = [f["severity"] for f in findings] + [t["severity"] for t in tax_risks]
    if "high" in severities:
        risk_level = "high"
    elif "medium" in severities:
        risk_level = "medium"
    elif "low" in severities:
        risk_level = "low"
    else:
        risk_level = "safe"

    return {
        "risk_level": risk_level,
        "confidence": confidence,
        "findings": findings,
        "tax_risks": tax_risks,
        "debit_nature": debit_nature,
        "credit_nature": credit_nature,
        "debit_category": debit_cat,
        "credit_category": credit_cat,
    }
