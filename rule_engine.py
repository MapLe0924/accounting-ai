"""
会计科目映射规则库（规则引擎）
包含 20+ 条常见业务场景的精确匹配规则。
每条规则包含：
  - keywords:     触发关键词列表（命中任意一个即匹配）
  - debit:        借方科目
  - credit:       贷方科目
  - description:  适用场景备注（展示给用户看）
  - warning:      专家校验提示（可选）
"""

RULE_DATABASE = [
    # ─── 管理费用类 ────────────────────────────────────
    {
        "keywords": ["请客", "吃饭", "招待", "餐饮", "业务招待", "宴请", "餐费"],
        "debit": "管理费用-业务招待费",
        "credit": "银行存款",
        "description": "业务招待费（餐饮、宴请客户等）",
        "warning": "业务招待费企业所得税汇算清缴时按实际发生额的60%扣除，最高不超过当年销售(营业)收入的5‰。",
    },
    {
        "keywords": ["办公用品", "文具", "打印纸", "笔", "墨盒", "硒鼓", "办公耗材"],
        "debit": "管理费用-办公费",
        "credit": "银行存款",
        "description": "日常办公用品采购",
        "warning": None,
    },
    {
        "keywords": ["差旅", "出差", "交通", "住宿", "机票", "火车票", "高铁", "打车", "出租车", "差旅费"],
        "debit": "管理费用-差旅费",
        "credit": "银行存款",
        "description": "员工出差产生的交通、住宿等费用",
        "warning": "差旅费需附有完整的出差申请单、行程单及发票，否则企业所得税前可能无法扣除。",
    },
    {
        "keywords": ["房租", "租金", "租赁", "办公室租", "房屋租赁", "租房"],
        "debit": "管理费用-租赁费",
        "credit": "银行存款",
        "description": "办公室房租支出",
        "warning": "金额超过5000元，建议确认是否属于长期待摊费用！",
    },
    {
        "keywords": ["水电", "水电费", "物业", "物业费", "电费", "水费"],
        "debit": "管理费用-水电费",
        "credit": "银行存款",
        "description": "办公场所水电物业费",
        "warning": None,
    },
    {
        "keywords": ["快递", "邮寄", "邮费", "快递费", "物流"],
        "debit": "管理费用-快递费",
        "credit": "银行存款",
        "description": "快递邮寄费用",
        "warning": None,
    },
    {
        "keywords": ["培训", "培训费", "教育", "职工教育", "进修"],
        "debit": "管理费用-职工教育经费",
        "credit": "银行存款",
        "description": "员工培训、进修等教育经费",
        "warning": "职工教育经费不超过工资薪金总额8%的部分准予税前扣除，超过部分准予结转以后纳税年度扣除。",
    },
    {
        "keywords": ["招聘", "招聘费", "猎头", "人才", "招聘服务"],
        "debit": "管理费用-招聘费",
        "credit": "银行存款",
        "description": "员工招聘相关费用",
        "warning": None,
    },
    {
        "keywords": ["咨询", "咨询费", "审计", "审计费", "律师", "律师费", "顾问", "顾问费"],
        "debit": "管理费用-中介服务费",
        "credit": "银行存款",
        "description": "审计、法律、咨询等中介服务费用",
        "warning": None,
    },
    {
        "keywords": ["会议", "会议费", "研讨会", "论坛"],
        "debit": "管理费用-会议费",
        "credit": "银行存款",
        "description": "举办或参加各类会议的费用",
        "warning": "会议费需附有会议通知、签到表等证明材料，否则可能被认定为业务招待费。",
    },

    # ─── 固定资产类 ────────────────────────────────────
    {
        "keywords": ["电脑", "笔记本", "台式机", "服务器", "显示器"],
        "debit": "固定资产-电子设备",
        "credit": "银行存款",
        "description": "购买电子设备（电脑等）",
        "warning": "电子设备折旧年限一般为3年，残值率5%。",
    },
    {
        "keywords": ["空调", "冰箱", "洗衣机", "家电", "电器"],
        "debit": "固定资产-电子设备",
        "credit": "银行存款",
        "description": "购买家用电器类固定资产",
        "warning": "单价超过5000元的电器建议计入固定资产按月折旧。",
    },
    {
        "keywords": ["办公桌", "办公椅", "文件柜", "家具", "办公家具", "沙发"],
        "debit": "固定资产-办公家具",
        "credit": "银行存款",
        "description": "购买办公家具",
        "warning": "办公家具折旧年限一般为5年。",
    },
    {
        "keywords": ["汽车", "车辆", "轿车", "货车", "机动车", "购车"],
        "debit": "固定资产-运输设备",
        "credit": "银行存款",
        "description": "购买运输车辆",
        "warning": "车辆折旧年限一般为4年。车辆购置税应计入固定资产原值。",
    },
    {
        "keywords": ["机器", "设备", "生产设备", "机床", "仪器"],
        "debit": "固定资产-机器设备",
        "credit": "银行存款",
        "description": "购买生产用机器设备",
        "warning": "机器设备折旧年限一般为10年。",
    },

    # ─── 薪酬类 ────────────────────────────────────────
    {
        "keywords": ["工资", "薪酬", "薪资", "奖金", "工资发放", "发工资", "工资表"],
        "debit": "应付职工薪酬-工资",
        "credit": "银行存款",
        "description": "发放员工工资",
        "warning": "大额工资发放，请确认已代扣代缴个人所得税！",
    },
    {
        "keywords": ["社保", "五险", "养老保险", "医疗保险", "失业保险", "公积金", "住房公积金"],
        "debit": "应付职工薪酬-社保公积金",
        "credit": "银行存款",
        "description": "缴纳员工社保和住房公积金",
        "warning": "社保和公积金单位承担部分可税前扣除，个人承担部分需从工资中代扣。",
    },
    {
        "keywords": ["福利", "福利费", "过节", "节日福利", "体检", "员工福利"],
        "debit": "应付职工薪酬-职工福利费",
        "credit": "银行存款",
        "description": "员工福利支出（过节费、体检等）",
        "warning": "职工福利费不超过工资薪金总额14%的部分准予税前扣除。",
    },

    # ─── 销售费用类 ────────────────────────────────────
    {
        "keywords": ["广告", "推广", "宣传", "营销", "广告费", "推广费", "宣传费"],
        "debit": "销售费用-广告费",
        "credit": "银行存款",
        "description": "广告宣传推广费用",
        "warning": "广告费和业务宣传费不超过当年销售(营业)收入15%的部分准予扣除，超过部分准予结转以后纳税年度扣除。",
    },
    {
        "keywords": ["运输", "运费", "物流费", "配送", "送货"],
        "debit": "销售费用-运输费",
        "credit": "银行存款",
        "description": "销售商品产生的运输费用",
        "warning": None,
    },
    {
        "keywords": ["招待客户", "客户招待", "商务宴请"],
        "debit": "销售费用-业务招待费",
        "credit": "银行存款",
        "description": "销售部门的客户招待费用",
        "warning": "业务招待费按发生额的60%扣除，最高不超过当年销售收入的5‰。",
    },

    # ─── 采购与应付类 ──────────────────────────────────
    {
        "keywords": ["原材料", "材料", "采购材料", "进货", "买材料", "采购原料"],
        "debit": "原材料",
        "credit": "应付账款",
        "description": "采购生产用原材料",
        "warning": None,
    },
    {
        "keywords": ["库存商品", "商品", "采购商品", "进货商品", "买货"],
        "debit": "库存商品",
        "credit": "应付账款",
        "description": "采购商品用于销售",
        "warning": None,
    },
    {
        "keywords": ["包装", "包装物", "包装箱", "包装盒"],
        "debit": "周转材料-包装物",
        "credit": "银行存款",
        "description": "购买包装物",
        "warning": None,
    },

    # ─── 收款类 ────────────────────────────────────────
    {
        "keywords": ["货款", "收到货款", "收款", "回款", "客户付款", "收到钱", "收货款"],
        "debit": "银行存款",
        "credit": "应收账款",
        "description": "收到客户支付的货款",
        "warning": None,
    },
    {
        "keywords": ["预收款", "预收", "定金", "订金", "预付款"],
        "debit": "银行存款",
        "credit": "预收账款",
        "description": "收到客户预付的款项",
        "warning": "预收款项在未确认收入前属于负债，不能确认为收入。",
    },

    # ─── 税费类 ────────────────────────────────────────
    {
        "keywords": ["交税", "缴税", "增值税", "所得税", "附加税", "印花税", "税费"],
        "debit": "应交税费",
        "credit": "银行存款",
        "description": "缴纳税费",
        "warning": "请确认各项税费的申报期限，避免逾期产生滞纳金。",
    },

    # ─── 其他类 ────────────────────────────────────────
    {
        "keywords": ["捐赠", "捐款", "赞助", "公益"],
        "debit": "营业外支出-捐赠支出",
        "credit": "银行存款",
        "description": "公益性捐赠支出",
        "warning": "公益性捐赠不超过年度利润总额12%的部分准予税前扣除。",
    },
    {
        "keywords": ["罚款", "罚金", "违约金", "赔偿", "滞纳金"],
        "debit": "营业外支出-罚款支出",
        "credit": "银行存款",
        "description": "罚款、违约金等支出",
        "warning": "行政罚款不得在企业所得税前扣除，需做纳税调增。",
    },
    {
        "keywords": ["利息", "银行手续费", "手续费", "转账费", "账户管理费"],
        "debit": "财务费用-手续费",
        "credit": "银行存款",
        "description": "银行手续费或利息支出",
        "warning": None,
    },
    {
        "keywords": ["维修", "修理", "修缮", "维修费", "修理费"],
        "debit": "管理费用-维修费",
        "credit": "银行存款",
        "description": "日常维修维护费用",
        "warning": "大额维修支出（超过原值50%）建议确认是否属于固定资产改良支出，应资本化处理。",
    },
    {
        "keywords": ["软件", "软件费", "系统", "系统费", "SaaS", "云服务", "会员"],
        "debit": "管理费用-软件服务费",
        "credit": "银行存款",
        "description": "软件订阅、SaaS服务、会员费等",
        "warning": None,
    },
]


def match_by_rule(user_input: str):
    """
    精确规则匹配：遍历规则库，如果用户输入包含任意关键词，返回匹配的规则结果。
    返回格式：{debit_account, credit_account, debit_amount, credit_amount, description, warning, source}
    金额从输入中智能提取，提取不到则使用默认值。
    """
    import re

    # 从输入中提取金额
    amount = _extract_amount(user_input)

    for rule in RULE_DATABASE:
        for kw in rule["keywords"]:
            if kw in user_input:
                return {
                    "debit_account": rule["debit"],
                    "credit_account": rule["credit"],
                    "debit_amount": amount,
                    "credit_amount": amount,
                    "description": rule["description"],
                    "warning": rule["warning"],
                    "source": "rule",  # 标记来源为规则库
                }

    return None


def _extract_amount(text: str) -> float:
    """
    从文本中提取金额数字。
    支持格式：800元、800.00、800 元、8000、5万、5万元
    """
    import re

    # 先尝试匹配"X万"或"X万元"
    m = re.search(r"(\d+(?:\.\d+)?)\s*万\s*元?", text)
    if m:
        return float(m.group(1)) * 10000

    # 匹配普通金额：XXX元、XXX.XX元、XXX 元
    m = re.search(r"(\d+(?:\.\d{1,2})?)\s*元", text)
    if m:
        return float(m.group(1))

    # 匹配纯数字（末尾或独立数字）
    m = re.search(r"(?:花了|支付|缴纳|付款|金额[为是]?|共|总计|合计)\s*(\d+(?:\.\d{1,2})?)", text)
    if m:
        return float(m.group(1))

    # 匹配任何数字
    m = re.search(r"(\d+(?:\.\d{1,2})?)", text)
    if m:
        return float(m.group(1))

    # 默认金额
    return 1000.00
