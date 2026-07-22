"""
模拟业务场景数据 —— 10 个常见的日常会计业务场景
每个场景包含：业务描述、推荐借方科目、推荐贷方科目、借方金额、贷方金额、校验提示
"""

MOCK_SCENARIOS = [
    {
        "id": 1,
        "description": "昨天请客户吃饭花了800元",
        "debit_account": "管理费用-业务招待费",
        "credit_account": "银行存款",
        "debit_amount": 800.00,
        "credit_amount": 800.00,
        "warning": None,
    },
    {
        "id": 2,
        "description": "购买办公用品花了500元",
        "debit_account": "管理费用-办公费",
        "credit_account": "银行存款",
        "debit_amount": 500.00,
        "credit_amount": 500.00,
        "warning": None,
    },
    {
        "id": 3,
        "description": "员工出差报销差旅费1200元",
        "debit_account": "管理费用-差旅费",
        "credit_account": "银行存款",
        "debit_amount": 1200.00,
        "credit_amount": 1200.00,
        "warning": None,
    },
    {
        "id": 4,
        "description": "支付办公室房租6000元",
        "debit_account": "管理费用-租赁费",
        "credit_account": "银行存款",
        "debit_amount": 6000.00,
        "credit_amount": 6000.00,
        "warning": "金额超过5000元，建议确认是否属于长期待摊费用！",
    },
    {
        "id": 5,
        "description": "购买一台电脑8000元",
        "debit_account": "固定资产-电子设备",
        "credit_account": "银行存款",
        "debit_amount": 8000.00,
        "credit_amount": 8000.00,
        "warning": None,
    },
    {
        "id": 6,
        "description": "支付员工工资5万元",
        "debit_account": "应付职工薪酬-工资",
        "credit_account": "银行存款",
        "debit_amount": 50000.00,
        "credit_amount": 50000.00,
        "warning": "大额工资发放，请确认已代扣代缴个人所得税！",
    },
    {
        "id": 7,
        "description": "收到客户货款15000元",
        "debit_account": "银行存款",
        "credit_account": "应收账款",
        "debit_amount": 15000.00,
        "credit_amount": 15000.00,
        "warning": None,
    },
    {
        "id": 8,
        "description": "支付水电费1500元",
        "debit_account": "管理费用-水电费",
        "credit_account": "银行存款",
        "debit_amount": 1500.00,
        "credit_amount": 1500.00,
        "warning": None,
    },
    {
        "id": 9,
        "description": "购买原材料一批30000元",
        "debit_account": "原材料",
        "credit_account": "应付账款",
        "debit_amount": 30000.00,
        "credit_amount": 30000.00,
        "warning": None,
    },
    {
        "id": 10,
        "description": "支付广告推广费2500元",
        "debit_account": "销售费用-广告费",
        "credit_account": "银行存款",
        "debit_amount": 2500.00,
        "credit_amount": 2500.00,
        "warning": "金额超过2000元，建议确认是否需要分期摊销！",
    },
]


def find_scenario(user_input: str):
    """
    根据用户输入的自然语言，模糊匹配最相似的业务场景。
    如果匹配不到，返回 None。
    """
    # 关键词匹配规则
    keyword_map = [
        (["请客", "吃饭", "招待", "餐饮", "业务招待"], 0),
        (["办公用品", "文具", "打印纸", "笔"], 1),
        (["差旅", "出差", "交通", "住宿", "机票", "火车"], 2),
        (["房租", "租金", "租赁", "办公室租"], 3),
        (["电脑", "笔记本", "台式机", "设备", "固定资产"], 4),
        (["工资", "薪酬", "薪资", "奖金", "工资发放"], 5),
        (["货款", "收到", "收款", "回款", "客户付款"], 6),
        (["水电", "水电费", "物业"], 7),
        (["原材料", "材料", "采购材料", "进货"], 8),
        (["广告", "推广", "宣传", "营销"], 9),
    ]

    for keywords, scenario_id in keyword_map:
        for kw in keywords:
            if kw in user_input:
                return MOCK_SCENARIOS[scenario_id]

    return None
