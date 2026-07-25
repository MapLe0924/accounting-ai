"""
模拟业务场景数据 —— 高频日常会计业务场景 + 会计科目大全
每个场景包含：业务描述、推荐借方科目、推荐贷方科目、借方金额、贷方金额、校验提示

会计科目分类说明：
  - 资产类：1xxx    货币资金、应收账款、存货、固定资产等
  - 负债类：2xxx    短期借款、应付账款、应付职工薪酬、应交税费等
  - 所有者权益类：3xxx  实收资本、资本公积、盈余公积、未分配利润
  - 成本类：4xxx    生产成本、制造费用
  - 损益类：5xxx/6xxx  主营业务收入、主营业务成本、管理费用、销售费用等
"""

# ─── 会计科目大全（五大类基础科目映射） ─────────────────────
ACCOUNT_CHART = {
    # ── 资产类 ──
    "货币资金": {"code": "1001", "category": "资产类", "nature": "借"},
    "银行存款": {"code": "1002", "category": "资产类", "nature": "借"},
    "应收账款": {"code": "1122", "category": "资产类", "nature": "借"},
    "预付账款": {"code": "1123", "category": "资产类", "nature": "借"},
    "其他应收款": {"code": "1221", "category": "资产类", "nature": "借"},
    "原材料": {"code": "1403", "category": "资产类", "nature": "借"},
    "库存商品": {"code": "1405", "category": "资产类", "nature": "借"},
    "周转材料": {"code": "1411", "category": "资产类", "nature": "借"},
    "固定资产": {"code": "1601", "category": "资产类", "nature": "借"},
    "累计折旧": {"code": "1602", "category": "资产类", "nature": "贷"},
    "无形资产": {"code": "1701", "category": "资产类", "nature": "借"},
    "累计摊销": {"code": "1702", "category": "资产类", "nature": "贷"},
    "库存现金": {"code": "1001", "category": "资产类", "nature": "借"},
    "交易性金融资产": {"code": "1101", "category": "资产类", "nature": "借"},
    "应收票据": {"code": "1121", "category": "资产类", "nature": "借"},
    "坏账准备": {"code": "1231", "category": "资产类", "nature": "贷"},
    "固定资产清理": {"code": "1606", "category": "资产类", "nature": "借"},
    "长期待摊费用": {"code": "1801", "category": "资产类", "nature": "借"},
    # ── 负债类 ──
    "短期借款": {"code": "2001", "category": "负债类", "nature": "贷"},
    "应付账款": {"code": "2202", "category": "负债类", "nature": "贷"},
    "预收账款": {"code": "2203", "category": "负债类", "nature": "贷"},
    "应付职工薪酬": {"code": "2211", "category": "负债类", "nature": "贷"},
    "应交税费": {"code": "2221", "category": "负债类", "nature": "贷"},
    "其他应付款": {"code": "2241", "category": "负债类", "nature": "贷"},
    "应付票据": {"code": "2201", "category": "负债类", "nature": "贷"},
    "应付股利": {"code": "2232", "category": "负债类", "nature": "贷"},
    "应付利息": {"code": "2231", "category": "负债类", "nature": "贷"},
    "递延收益": {"code": "2401", "category": "负债类", "nature": "贷"},
    "长期借款": {"code": "2501", "category": "负债类", "nature": "贷"},
    # ── 所有者权益类 ──
    "实收资本": {"code": "4001", "category": "所有者权益类", "nature": "贷"},
    "资本公积": {"code": "4002", "category": "所有者权益类", "nature": "贷"},
    "盈余公积": {"code": "4101", "category": "所有者权益类", "nature": "贷"},
    "未分配利润": {"code": "4104", "category": "所有者权益类", "nature": "贷"},
    "本年利润": {"code": "4103", "category": "所有者权益类", "nature": "贷"},
    "利润分配": {"code": "4104", "category": "所有者权益类", "nature": "贷"},
    # ── 成本类 ──
    "生产成本": {"code": "5001", "category": "成本类", "nature": "借"},
    "制造费用": {"code": "5101", "category": "成本类", "nature": "借"},
    "研发支出": {"code": "5301", "category": "成本类", "nature": "借"},
    # ── 损益类 ──
    "主营业务收入": {"code": "6001", "category": "损益类", "nature": "贷"},
    "主营业务成本": {"code": "6401", "category": "损益类", "nature": "借"},
    "税金及附加": {"code": "6403", "category": "损益类", "nature": "借"},
    "销售费用": {"code": "6601", "category": "损益类", "nature": "借"},
    "管理费用": {"code": "6602", "category": "损益类", "nature": "借"},
    "财务费用": {"code": "6603", "category": "损益类", "nature": "借"},
    "所得税费用": {"code": "6801", "category": "损益类", "nature": "借"},
    "营业外收入": {"code": "6301", "category": "损益类", "nature": "贷"},
    "营业外支出": {"code": "6711", "category": "损益类", "nature": "借"},
    "投资收益": {"code": "6111", "category": "损益类", "nature": "贷"},
    "其他业务收入": {"code": "6051", "category": "损益类", "nature": "贷"},
    "其他业务成本": {"code": "6402", "category": "损益类", "nature": "借"},
    "资产减值损失": {"code": "6701", "category": "损益类", "nature": "借"},
    "公允价值变动损益": {"code": "6101", "category": "损益类", "nature": "贷"},
    "以前年度损益调整": {"code": "6901", "category": "损益类", "nature": "贷"},
}


def get_account_category(account_name: str) -> str:
    """根据科目名称返回所属大类（资产类/负债类/所有者权益类/成本类/损益类）"""
    # 先尝试精确匹配
    if account_name in ACCOUNT_CHART:
        return ACCOUNT_CHART[account_name]["category"]
    # 再尝试前缀匹配（如"管理费用-办公费"属于"管理费用"→损益类）
    for key, info in ACCOUNT_CHART.items():
        if account_name.startswith(key):
            return info["category"]
    return "未知"


MOCK_SCENARIOS = [
    # ─── 费用报销类（1-10）────────────────────────────
    {
        "id": 1,
        "description": "昨天请客户吃饭花了800元",
        "debit_account": "管理费用-业务招待费",
        "credit_account": "银行存款",
        "debit_amount": 800.00,
        "credit_amount": 800.00,
        "warning": "业务招待费按发生额60%扣除，最高不超过年销售收入5‰。",
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
        "warning": "差旅费需附出差申请单、行程单及发票。",
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
        "description": "支付水电费1500元",
        "debit_account": "管理费用-水电费",
        "credit_account": "银行存款",
        "debit_amount": 1500.00,
        "credit_amount": 1500.00,
        "warning": None,
    },
    {
        "id": 6,
        "description": "支付快递费80元",
        "debit_account": "管理费用-快递费",
        "credit_account": "银行存款",
        "debit_amount": 80.00,
        "credit_amount": 80.00,
        "warning": None,
    },
    {
        "id": 7,
        "description": "支付员工培训费3000元",
        "debit_account": "管理费用-职工教育经费",
        "credit_account": "银行存款",
        "debit_amount": 3000.00,
        "credit_amount": 3000.00,
        "warning": "职工教育经费不超过工资总额8%的部分准予税前扣除。",
    },
    {
        "id": 8,
        "description": "支付审计咨询费10000元",
        "debit_account": "管理费用-中介服务费",
        "credit_account": "银行存款",
        "debit_amount": 10000.00,
        "credit_amount": 10000.00,
        "warning": None,
    },
    {
        "id": 9,
        "description": "支付会议费2000元",
        "debit_account": "管理费用-会议费",
        "credit_account": "银行存款",
        "debit_amount": 2000.00,
        "credit_amount": 2000.00,
        "warning": "会议费需附会议通知、签到表等证明材料。",
    },
    {
        "id": 10,
        "description": "支付办公室维修费800元",
        "debit_account": "管理费用-维修费",
        "credit_account": "银行存款",
        "debit_amount": 800.00,
        "credit_amount": 800.00,
        "warning": "大额维修（超过原值50%）应资本化处理。",
    },

    # ─── 固定资产类（11-15）───────────────────────────
    {
        "id": 11,
        "description": "购买一台电脑8000元",
        "debit_account": "固定资产-电子设备",
        "credit_account": "银行存款",
        "debit_amount": 8000.00,
        "credit_amount": 8000.00,
        "warning": "电子设备折旧年限一般为3年，残值率5%。",
    },
    {
        "id": 12,
        "description": "购买办公桌椅5000元",
        "debit_account": "固定资产-办公家具",
        "credit_account": "银行存款",
        "debit_amount": 5000.00,
        "credit_amount": 5000.00,
        "warning": "办公家具折旧年限一般为5年。",
    },
    {
        "id": 13,
        "description": "购买生产设备10万元",
        "debit_account": "固定资产-机器设备",
        "credit_account": "银行存款",
        "debit_amount": 100000.00,
        "credit_amount": 100000.00,
        "warning": "机器设备折旧年限一般为10年。",
    },
    {
        "id": 14,
        "description": "购买一辆运输货车15万元",
        "debit_account": "固定资产-运输设备",
        "credit_account": "银行存款",
        "debit_amount": 150000.00,
        "credit_amount": 150000.00,
        "warning": "车辆折旧年限一般为4年，购置税应计入原值。",
    },
    {
        "id": 15,
        "description": "计提本月固定资产折旧5000元",
        "debit_account": "管理费用-折旧费",
        "credit_account": "累计折旧",
        "debit_amount": 5000.00,
        "credit_amount": 5000.00,
        "warning": "折旧方法一经确定不得随意变更。",
    },

    # ─── 薪酬社保类（16-19）───────────────────────────
    {
        "id": 16,
        "description": "支付员工工资5万元",
        "debit_account": "应付职工薪酬-工资",
        "credit_account": "银行存款",
        "debit_amount": 50000.00,
        "credit_amount": 50000.00,
        "warning": "大额工资发放，请确认已代扣代缴个人所得税！",
    },
    {
        "id": 17,
        "description": "缴纳社保和公积金12000元",
        "debit_account": "应付职工薪酬-社保公积金",
        "credit_account": "银行存款",
        "debit_amount": 12000.00,
        "credit_amount": 12000.00,
        "warning": "单位承担部分可税前扣除，个人部分从工资代扣。",
    },
    {
        "id": 18,
        "description": "发放中秋节员工福利3000元",
        "debit_account": "应付职工薪酬-职工福利费",
        "credit_account": "银行存款",
        "debit_amount": 3000.00,
        "credit_amount": 3000.00,
        "warning": "职工福利费不超过工资总额14%的部分准予税前扣除。",
    },
    {
        "id": 19,
        "description": "计提本月职工工资6万元",
        "debit_account": "管理费用-工资",
        "credit_account": "应付职工薪酬-工资",
        "debit_amount": 60000.00,
        "credit_amount": 60000.00,
        "warning": "工资计提需与实发数核对，差异做调整分录。",
    },

    # ─── 销售与收款类（20-23）─────────────────────────
    {
        "id": 20,
        "description": "销售商品一批收到货款50000元",
        "debit_account": "银行存款",
        "credit_account": "主营业务收入",
        "debit_amount": 50000.00,
        "credit_amount": 50000.00,
        "warning": "确认收入的同时需计提增值税销项税额。",
    },
    {
        "id": 21,
        "description": "收到客户前欠货款15000元",
        "debit_account": "银行存款",
        "credit_account": "应收账款",
        "debit_amount": 15000.00,
        "credit_amount": 15000.00,
        "warning": None,
    },
    {
        "id": 22,
        "description": "支付广告推广费2500元",
        "debit_account": "销售费用-广告费",
        "credit_account": "银行存款",
        "debit_amount": 2500.00,
        "credit_amount": 2500.00,
        "warning": "广告费不超过年销售收入15%的部分准予扣除。",
    },
    {
        "id": 23,
        "description": "支付商品运输费800元",
        "debit_account": "销售费用-运输费",
        "credit_account": "银行存款",
        "debit_amount": 800.00,
        "credit_amount": 800.00,
        "warning": None,
    },

    # ─── 采购与存货类（24-26）─────────────────────────
    {
        "id": 24,
        "description": "购买原材料一批30000元",
        "debit_account": "原材料",
        "credit_account": "应付账款",
        "debit_amount": 30000.00,
        "credit_amount": 30000.00,
        "warning": "原材料入库需附入库单和质检单。",
    },
    {
        "id": 25,
        "description": "采购商品一批20000元入库",
        "debit_account": "库存商品",
        "credit_account": "应付账款",
        "debit_amount": 20000.00,
        "credit_amount": 20000.00,
        "warning": None,
    },
    {
        "id": 26,
        "description": "购买包装物500元",
        "debit_account": "周转材料-包装物",
        "credit_account": "银行存款",
        "debit_amount": 500.00,
        "credit_amount": 500.00,
        "warning": None,
    },

    # ─── 税费类（27-28）───────────────────────────────
    {
        "id": 27,
        "description": "缴纳本月增值税8000元",
        "debit_account": "应交税费-应交增值税",
        "credit_account": "银行存款",
        "debit_amount": 8000.00,
        "credit_amount": 8000.00,
        "warning": "增值税申报截止日为次月15日，逾期有滞纳金。",
    },
    {
        "id": 28,
        "description": "计提本月企业所得税5000元",
        "debit_account": "所得税费用",
        "credit_account": "应交税费-应交所得税",
        "debit_amount": 5000.00,
        "credit_amount": 5000.00,
        "warning": "企业所得税按季度预缴，年度汇算清缴。",
    },

    # ─── 其他类（29-30）───────────────────────────────
    {
        "id": 29,
        "description": "银行账户收到存款利息200元",
        "debit_account": "银行存款",
        "credit_account": "财务费用-利息收入",
        "debit_amount": 200.00,
        "credit_amount": 200.00,
        "warning": "利息收入应冲减财务费用，而非计入营业外收入。",
    },
    {
        "id": 30,
        "description": "支付银行转账手续费50元",
        "debit_account": "财务费用-手续费",
        "credit_account": "银行存款",
        "debit_amount": 50.00,
        "credit_amount": 50.00,
        "warning": None,
    },

    # ─── 所有者权益类（32-33）：股东投资与资本公积 ────
    {
        "id": 32,
        "description": "股东张三向公司注入投资款50万元",
        "debit_account": "银行存款",
        "credit_account": "实收资本",
        "debit_amount": 500000.00,
        "credit_amount": 500000.00,
        "warning": "股东投资款需出具验资报告，并在工商登记中体现。超出注册资本部分计入资本公积。",
    },
    {
        "id": 33,
        "description": "股东溢价投资，超出注册资本部分20万元",
        "debit_account": "银行存款",
        "credit_account": "资本公积-资本溢价",
        "debit_amount": 200000.00,
        "credit_amount": 200000.00,
        "warning": "资本溢价（股本溢价）不得用于弥补亏损，可用于转增资本。",
    },

    # ─── 负债类（34-36）：借款与计提 ──────────────────
    {
        "id": 34,
        "description": "向银行借入短期借款30万元",
        "debit_account": "银行存款",
        "credit_account": "短期借款",
        "debit_amount": 300000.00,
        "credit_amount": 300000.00,
        "warning": "短期借款期限一般在1年以内（含1年），需按期计提利息。",
    },
    {
        "id": 35,
        "description": "计提本月员工工资总额2万元",
        "debit_account": "管理费用-工资",
        "credit_account": "应付职工薪酬-工资",
        "debit_amount": 20000.00,
        "credit_amount": 20000.00,
        "warning": "工资计提需与实发数核对，差异做调整分录。",
    },
    {
        "id": 36,
        "description": "计提本月生产设备折旧1万元",
        "debit_account": "制造费用-折旧费",
        "credit_account": "累计折旧",
        "debit_amount": 10000.00,
        "credit_amount": 10000.00,
        "warning": "生产设备折旧计入制造费用，最终分配至产品成本。折旧方法一经确定不得随意变更。",
    },

    # ─── 成本类（37）：生产成本结转 ────────────────────
    {
        "id": 37,
        "description": "结转本月完工产品成本8万元",
        "debit_account": "库存商品",
        "credit_account": "生产成本",
        "debit_amount": 80000.00,
        "credit_amount": 80000.00,
        "warning": "完工产品成本结转需附成本计算单，确认料工费分配合理。",
    },

    # ─── 负债类（38）：计提税金 ────────────────────────
    {
        "id": 38,
        "description": "计提本月城市维护建设税及教育费附加1200元",
        "debit_account": "税金及附加",
        "credit_account": "应交税费-应交城建税及教育费附加",
        "debit_amount": 1200.00,
        "credit_amount": 1200.00,
        "warning": "城建税税率7%（城市）或5%（县城），教育费附加3%，地方教育附加2%。",
    },

    # ─── 任务一：购买理财产品（39）────────────────────
    {
        "id": 39,
        "description": "购买不保本银行理财产品100万元",
        "debit_account": "交易性金融资产",
        "credit_account": "银行存款",
        "debit_amount": 1000000.00,
        "credit_amount": 1000000.00,
        "warning": "不保本理财产品应分类为交易性金融资产，按公允价值计量且变动计入当期损益。",
    },

    # ─── 任务二：进阶复杂场景（40-47）─────────────────
    # 场景1：支付去年已抵扣专票的广告费，冲回进项税
    {
        "id": 40,
        "description": "支付去年已抵扣专票的广告费11300元（含税），因发票不合规需转出已抵扣进项税",
        "warning": "不合规发票对应的进项税额不得抵扣，已抵扣的需做进项税额转出处理。",
        "entries": [
            {
                "debit_account": "应付账款",
                "credit_account": "银行存款",
                "debit_amount": 11300.00,
                "credit_amount": 11300.00,
                "description": "支付去年广告费款项",
                "tax_note": None,
            },
            {
                "debit_account": "销售费用-广告费",
                "credit_account": "应交税费-应交增值税(进项税额转出)",
                "debit_amount": 1300.00,
                "credit_amount": 1300.00,
                "description": "不合规发票进项税额转出（11300÷1.13×13%=1300）",
                "tax_note": "进项税额转出 = 11,300 ÷ 1.13 × 13% = 1,300元",
            },
        ],
        "debit_account": "应付账款 / 销售费用-广告费",
        "credit_account": "银行存款 / 应交税费-应交增值税(进项税额转出)",
        "debit_amount": 11300.00,
        "credit_amount": 11300.00,
    },

    # 场景2：股东以旧机器入股
    {
        "id": 41,
        "description": "股东李四以旧机器设备入股，评估作价100万元",
        "debit_account": "固定资产-机器设备",
        "credit_account": "实收资本",
        "debit_amount": 1000000.00,
        "credit_amount": 1000000.00,
        "warning": "股东以非货币资产出资需经评估作价并出具验资报告，不得高估或低估。",
    },

    # 场景3：提取现金 + 盘盈
    {
        "id": 42,
        "description": "提取现金5万元备发工资，盘点时发现库存现金盘盈100元",
        "warning": "现金盘盈先计入待处理财产损溢，查明原因经批准后转营业外收入。",
        "entries": [
            {
                "debit_account": "库存现金",
                "credit_account": "银行存款",
                "debit_amount": 50000.00,
                "credit_amount": 50000.00,
                "description": "从银行提取现金备发工资",
                "tax_note": None,
            },
            {
                "debit_account": "库存现金",
                "credit_account": "营业外收入",
                "debit_amount": 100.00,
                "credit_amount": 100.00,
                "description": "现金盘点溢余，经批准转营业外收入",
                "tax_note": "现金盘盈需计入营业外收入，缴纳企业所得税。",
            },
        ],
        "debit_account": "库存现金",
        "credit_account": "银行存款 / 营业外收入",
        "debit_amount": 50100.00,
        "credit_amount": 50100.00,
    },

    # 场景4：销售商品含税113万，折扣实收111万
    {
        "id": 43,
        "description": "销售商品含税价113万元，因给予商业折扣实际收款111万元",
        "debit_account": "银行存款",
        "credit_account": "主营业务收入 / 应交税费-应交增值税(销项税额)",
        "debit_amount": 1110000.00,
        "credit_amount": 1110000.00,
        "warning": "商业折扣按折扣后金额确认收入：不含税收入=1,110,000÷1.13≈982,300.88元，销项税额≈127,699.12元。",
    },

    # 场景5：固定资产报废清理
    {
        "id": 44,
        "description": "报废一台旧设备，原值50万元、已计提折旧48万元，支付清理费2000元，残料出售收入3000元",
        "warning": "固定资产报废需经管理层审批，净损失计入营业外支出，税前扣除需专项申报。",
        "entries": [
            {
                "debit_account": "固定资产清理",
                "credit_account": "固定资产-机器设备",
                "debit_amount": 20000.00,
                "credit_amount": 500000.00,
                "description": "将设备转入清理（借：固定资产清理20,000，借：累计折旧480,000，贷：固定资产500,000）",
                "tax_note": "同时借记累计折旧480,000。",
            },
            {
                "debit_account": "固定资产清理",
                "credit_account": "银行存款",
                "debit_amount": 2000.00,
                "credit_amount": 2000.00,
                "description": "支付设备清理拆卸费用",
                "tax_note": None,
            },
            {
                "debit_account": "银行存款",
                "credit_account": "固定资产清理",
                "debit_amount": 3000.00,
                "credit_amount": 3000.00,
                "description": "残料出售取得变价收入",
                "tax_note": None,
            },
            {
                "debit_account": "营业外支出-处置非流动资产损失",
                "credit_account": "固定资产清理",
                "debit_amount": 19000.00,
                "credit_amount": 19000.00,
                "description": "结转报废净损失（20,000+2,000-3,000=19,000）",
                "tax_note": "净损失 = 账面价值20,000 + 清理费2,000 - 残料收入3,000 = 19,000元。",
            },
        ],
        "debit_account": "固定资产清理 / 营业外支出",
        "credit_account": "固定资产 / 银行存款 / 固定资产清理",
        "debit_amount": 500000.00,
        "credit_amount": 500000.00,
    },

    # 场景6：替员工垫付个税，下月从工资扣回
    {
        "id": 45,
        "description": "替员工垫付个人所得税12000元，下月从工资中扣回",
        "warning": "企业垫付员工个税属于代垫款性质，不得直接计入费用，应通过其他应收款核算。",
        "entries": [
            {
                "debit_account": "其他应收款-代垫个税",
                "credit_account": "银行存款",
                "debit_amount": 12000.00,
                "credit_amount": 12000.00,
                "description": "替员工垫付个人所得税",
                "tax_note": None,
            },
            {
                "debit_account": "应付职工薪酬-工资",
                "credit_account": "其他应收款-代垫个税",
                "debit_amount": 12000.00,
                "credit_amount": 12000.00,
                "description": "下月从员工工资中扣回代垫个税",
                "tax_note": "扣回时冲减应付职工薪酬，不影响当期损益。",
            },
        ],
        "debit_account": "其他应收款-代垫个税 / 应付职工薪酬-工资",
        "credit_account": "银行存款 / 其他应收款-代垫个税",
        "debit_amount": 12000.00,
        "credit_amount": 12000.00,
    },

    # 场景7：购买不保本理财 + 收到分红
    {
        "id": 46,
        "description": "购买不保本理财产品100万元，持有期间收到分红收益2万元",
        "warning": "不保本理财属于交易性金融资产；持有期间收益确认为投资收益，非利息收入。",
        "entries": [
            {
                "debit_account": "交易性金融资产",
                "credit_account": "银行存款",
                "debit_amount": 1000000.00,
                "credit_amount": 1000000.00,
                "description": "购入不保本银行理财产品",
                "tax_note": None,
            },
            {
                "debit_account": "银行存款",
                "credit_account": "投资收益",
                "debit_amount": 20000.00,
                "credit_amount": 20000.00,
                "description": "收到理财产品分红收益",
                "tax_note": "投资收益需并入应纳税所得额缴纳企业所得税。",
            },
        ],
        "debit_account": "交易性金融资产 / 银行存款",
        "credit_account": "银行存款 / 投资收益",
        "debit_amount": 1020000.00,
        "credit_amount": 1020000.00,
    },

    # 场景8：红冲上月暂估入库，收到发票按实际金额入账
    {
        "id": 47,
        "description": "红冲上月暂估入库原材料5万元，本月收到增值税专用发票，实际金额4.8万元、税额6240元",
        "warning": "暂估入库应在次月初红冲，收到发票后按实际金额入账并确认进项税额。",
        "entries": [
            {
                "debit_account": "原材料",
                "credit_account": "应付账款-暂估应付账款",
                "debit_amount": -50000.00,
                "credit_amount": -50000.00,
                "description": "红冲上月暂估入库（全额冲回）",
                "tax_note": "暂估入库不含进项税，红冲时全额原路冲回。",
            },
            {
                "debit_account": "原材料",
                "credit_account": "银行存款",
                "debit_amount": 48000.00,
                "credit_amount": 54240.00,
                "description": "按发票实际金额正式入账（原材料48,000 + 进项税6,240）",
                "tax_note": "同时借记：应交税费-应交增值税(进项税额) 6,240元（48,000×13%）。",
            },
        ],
        "debit_account": "原材料 / 应交税费-应交增值税(进项税额)",
        "credit_account": "应付账款-暂估应付账款 / 银行存款",
        "debit_amount": 54240.00,
        "credit_amount": 54240.00,
    },

    # ═══════════════════════════════════════════════════
    # 二期扩展场景（48-98）
    # ═══════════════════════════════════════════════════

    # ─── 往来款项（48-55）───────────────────────────
    {
        "id": 48,
        "description": "用银行存款支付前欠供应商货款3万元",
        "debit_account": "应付账款",
        "credit_account": "银行存款",
        "debit_amount": 30000.00,
        "credit_amount": 30000.00,
        "warning": "支付应付账款不涉及损益，仅影响资产负债项目。",
    },
    {
        "id": 49,
        "description": "采购的原材料因质量问题退货，金额8000元",
        "debit_account": "应付账款",
        "credit_account": "原材料",
        "debit_amount": 8000.00,
        "credit_amount": 8000.00,
        "warning": "退货需取得红字发票或退货单，同时冲减进项税额。",
    },
    {
        "id": 50,
        "description": "存货盘点发现原材料盘盈2000元",
        "debit_account": "原材料",
        "credit_account": "营业外收入",
        "debit_amount": 2000.00,
        "credit_amount": 2000.00,
        "warning": "存货盘盈先通过待处理财产损溢归集，批准后冲减管理费用。",
    },
    {
        "id": 51,
        "description": "存货盘点发现库存商品盘亏1500元",
        "debit_account": "营业外支出",
        "credit_account": "库存商品",
        "debit_amount": 1500.00,
        "credit_amount": 1500.00,
        "warning": "管理不善造成的盘亏进项税额需转出；自然灾害造成的无需转出。",
    },
    {
        "id": 52,
        "description": "预付供应商货款5万元",
        "debit_account": "预付账款",
        "credit_account": "银行存款",
        "debit_amount": 50000.00,
        "credit_amount": 50000.00,
        "warning": "预付款项在未收到货物或服务前属于资产，收到后再冲减预付账款。",
    },
    {
        "id": 53,
        "description": "收到供应商货物后将预付账款转入库存",
        "debit_account": "库存商品",
        "credit_account": "预付账款",
        "debit_amount": 50000.00,
        "credit_amount": 50000.00,
        "warning": "预付账款冲销时需附入库单及发票。",
    },
    {
        "id": 54,
        "description": "销售商品发生退货，退款8000元",
        "debit_account": "主营业务收入",
        "credit_account": "银行存款",
        "debit_amount": 8000.00,
        "credit_amount": 8000.00,
        "warning": "销售退回需开具红字发票，同时冲减销项税额并转回已结转成本。",
    },
    {
        "id": 55,
        "description": "客户提前付款，给予现金折扣500元",
        "debit_account": "财务费用-现金折扣",
        "credit_account": "应收账款",
        "debit_amount": 500.00,
        "credit_amount": 500.00,
        "warning": "现金折扣计入财务费用，不得冲减销售收入。",
    },

    # ─── 坏账（56-57）───────────────────────────────
    {
        "id": 56,
        "description": "按应收账款余额百分比法计提坏账准备2万元",
        "debit_account": "资产减值损失",
        "credit_account": "坏账准备",
        "debit_amount": 20000.00,
        "credit_amount": 20000.00,
        "warning": "坏账准备计提比例需符合企业会计政策，税前扣除需符合税法条件。",
    },
    {
        "id": 57,
        "description": "确认某客户应收账款1.5万元无法收回，实际发生坏账",
        "debit_account": "坏账准备",
        "credit_account": "应收账款",
        "debit_amount": 15000.00,
        "credit_amount": 15000.00,
        "warning": "实际核销坏账需取得充分证据（如债务人破产、注销等）。",
    },

    # ─── 薪酬社保扩展（58-61）─────────────────────────
    {
        "id": 58,
        "description": "计提本月单位承担的社保和公积金1.8万元",
        "debit_account": "管理费用-社保公积金",
        "credit_account": "应付职工薪酬-社保公积金",
        "debit_amount": 18000.00,
        "credit_amount": 18000.00,
        "warning": "单位承担的社保公积金可税前扣除，计提时按部门分别计入管理费用/销售费用/制造费用。",
    },
    {
        "id": 59,
        "description": "计提本月工会经费2000元（按工资总额2%）",
        "debit_account": "管理费用-工会经费",
        "credit_account": "应付职工薪酬-工会经费",
        "debit_amount": 2000.00,
        "credit_amount": 2000.00,
        "warning": "工会经费按工资总额2%计提，其中40%上缴上级工会，60%留企业工会使用。",
    },
    {
        "id": 60,
        "description": "外购一批节日礼品发放给员工，金额6000元",
        "debit_account": "应付职工薪酬-职工福利费",
        "credit_account": "银行存款",
        "debit_amount": 6000.00,
        "credit_amount": 6000.00,
        "warning": "外购商品发福利进项税额不得抵扣（需转出）；福利费不超过工资总额14%可税前扣除。",
    },
    {
        "id": 61,
        "description": "员工借支备用金3000元用于出差",
        "debit_account": "其他应收款-备用金",
        "credit_account": "银行存款",
        "debit_amount": 3000.00,
        "credit_amount": 3000.00,
        "warning": "备用金实行定额管理制度，报销时凭发票冲销其他应收款。",
    },

    # ─── 税费扩展（62-66）───────────────────────────
    {
        "id": 62,
        "description": "月末结转本月未交增值税1.3万元",
        "debit_account": "应交税费-应交增值税(转出未交增值税)",
        "credit_account": "应交税费-未交增值税",
        "debit_amount": 13000.00,
        "credit_amount": 13000.00,
        "warning": "月末需将应交增值税贷方余额转入未交增值税明细科目。",
    },
    {
        "id": 63,
        "description": "因管理不善导致原材料毁损，转出进项税额2600元",
        "debit_account": "营业外支出",
        "credit_account": "应交税费-应交增值税(进项税额转出)",
        "debit_amount": 2600.00,
        "credit_amount": 2600.00,
        "warning": "非正常损失的进项税额不得抵扣，需做进项税额转出处理。",
    },
    {
        "id": 64,
        "description": "缴纳印花税300元",
        "debit_account": "税金及附加",
        "credit_account": "银行存款",
        "debit_amount": 300.00,
        "credit_amount": 300.00,
        "warning": "印花税直接计入税金及附加，无需通过应交税费科目计提。",
    },
    {
        "id": 65,
        "description": "代扣代缴员工个人所得税8000元",
        "debit_account": "应交税费-应交个人所得税",
        "credit_account": "银行存款",
        "debit_amount": 8000.00,
        "credit_amount": 8000.00,
        "warning": "个税由企业代扣代缴，申报截止日为次月15日。",
    },
    {
        "id": 66,
        "description": "计提本季度房产税和土地使用税5000元",
        "debit_account": "税金及附加",
        "credit_account": "应交税费-应交房产税",
        "debit_amount": 5000.00,
        "credit_amount": 5000.00,
        "warning": "房产税按房产原值70%的1.2%或租金收入的12%计算。",
    },

    # ─── 固定资产扩展（67-70）────────────────────────
    {
        "id": 67,
        "description": "固定资产盘点发现一台设备盘亏，账面价值2万元",
        "debit_account": "营业外支出-盘亏损失",
        "credit_account": "固定资产-机器设备",
        "debit_amount": 20000.00,
        "credit_amount": 20000.00,
        "warning": "固定资产盘亏需先转入待处理财产损溢，批准后计入营业外支出。",
    },
    {
        "id": 68,
        "description": "对一台设备计提减值准备3万元",
        "debit_account": "资产减值损失",
        "credit_account": "固定资产减值准备",
        "debit_amount": 30000.00,
        "credit_amount": 30000.00,
        "warning": "固定资产减值损失一经确认不得转回（会计准则禁止）。",
    },
    {
        "id": 69,
        "description": "出售一台旧设备，原值8万已折旧6万，售价3万",
        "debit_account": "银行存款",
        "credit_account": "固定资产清理",
        "debit_amount": 30000.00,
        "credit_amount": 30000.00,
        "warning": "出售固定资产需先转入清理，净收益计入资产处置损益。",
    },
    {
        "id": 70,
        "description": "对租入的办公场地进行装修，支出12万元",
        "debit_account": "长期待摊费用-装修费",
        "credit_account": "银行存款",
        "debit_amount": 120000.00,
        "credit_amount": 120000.00,
        "warning": "经营租入固定资产改良支出计入长期待摊费用，在剩余租赁期内摊销。",
    },

    # ─── 无形资产（71-73）─────────────────────────
    {
        "id": 71,
        "description": "购入一项专利权，价款20万元",
        "debit_account": "无形资产-专利权",
        "credit_account": "银行存款",
        "debit_amount": 200000.00,
        "credit_amount": 200000.00,
        "warning": "外购无形资产按实际成本入账，包括购买价款和相关税费。",
    },
    {
        "id": 72,
        "description": "计提本月无形资产摊销3000元",
        "debit_account": "管理费用-无形资产摊销",
        "credit_account": "累计摊销",
        "debit_amount": 3000.00,
        "credit_amount": 3000.00,
        "warning": "使用寿命有限的无形资产需按期摊销，不确定寿命的不摊销但需减值测试。",
    },
    {
        "id": 73,
        "description": "发生研发支出5万元，不满足资本化条件",
        "debit_account": "管理费用-研发费用",
        "credit_account": "银行存款",
        "debit_amount": 50000.00,
        "credit_amount": 50000.00,
        "warning": "研究阶段支出及开发阶段不满足资本化条件的，全部计入当期损益。",
    },

    # ─── 借款与利息（74-78）───────────────────────
    {
        "id": 74,
        "description": "计提本月短期借款利息2500元",
        "debit_account": "财务费用-利息支出",
        "credit_account": "应付利息",
        "debit_amount": 2500.00,
        "credit_amount": 2500.00,
        "warning": "短期借款利息按期计提，实际支付时冲减应付利息。",
    },
    {
        "id": 75,
        "description": "支付本季度短期借款利息7500元",
        "debit_account": "应付利息",
        "credit_account": "银行存款",
        "debit_amount": 7500.00,
        "credit_amount": 7500.00,
        "warning": "利息支出需取得银行利息回单作为原始凭证。",
    },
    {
        "id": 76,
        "description": "计提本月长期借款利息8000元（符合资本化条件）",
        "debit_account": "在建工程",
        "credit_account": "应付利息",
        "debit_amount": 8000.00,
        "credit_amount": 8000.00,
        "warning": "购建固定资产的借款利息在资产达到预定可使用状态前应资本化。",
    },
    {
        "id": 77,
        "description": "归还到期的短期借款本金20万元",
        "debit_account": "短期借款",
        "credit_account": "银行存款",
        "debit_amount": 200000.00,
        "credit_amount": 200000.00,
        "warning": "归还借款本金不涉及损益，仅影响资产负债项目。",
    },
    {
        "id": 78,
        "description": "用银行承兑汇票支付原材料采购款10万元",
        "debit_account": "原材料",
        "credit_account": "应付票据",
        "debit_amount": 100000.00,
        "credit_amount": 100000.00,
        "warning": "银行承兑汇票需缴纳一定比例的保证金，到期无条件支付。",
    },

    # ─── 收入与成本（79-83）───────────────────────
    {
        "id": 79,
        "description": "结转本月已销商品的主营业务成本6万元",
        "debit_account": "主营业务成本",
        "credit_account": "库存商品",
        "debit_amount": 60000.00,
        "credit_amount": 60000.00,
        "warning": "主营业务成本需与主营业务收入配比，在确认收入的同一期间结转。",
    },
    {
        "id": 80,
        "description": "出售生产废料取得收入1500元",
        "debit_account": "银行存款",
        "credit_account": "其他业务收入",
        "debit_amount": 1500.00,
        "credit_amount": 1500.00,
        "warning": "废料出售收入属于其他业务收入，需计提增值税销项税额。",
    },
    {
        "id": 81,
        "description": "收到客户交来的包装物押金2000元",
        "debit_account": "银行存款",
        "credit_account": "其他应付款-押金",
        "debit_amount": 2000.00,
        "credit_amount": 2000.00,
        "warning": "收取的押金属于负债，退还时冲减其他应付款；逾期不退转为营业外收入。",
    },
    {
        "id": 82,
        "description": "退还客户包装物押金2000元",
        "debit_account": "其他应付款-押金",
        "credit_account": "银行存款",
        "debit_amount": 2000.00,
        "credit_amount": 2000.00,
        "warning": "退还押金时确认押金收据已收回。",
    },
    {
        "id": 83,
        "description": "客户逾期未退还包装物，没收押金2000元",
        "debit_account": "其他应付款-押金",
        "credit_account": "营业外收入",
        "debit_amount": 2000.00,
        "credit_amount": 2000.00,
        "warning": "逾期未退还的押金需确认收入并计提增值税销项税额。",
    },

    # ─── 所有者权益（84-88）───────────────────────
    {
        "id": 84,
        "description": "按净利润10%提取法定盈余公积3万元",
        "debit_account": "利润分配-提取法定盈余公积",
        "credit_account": "盈余公积-法定盈余公积",
        "debit_amount": 30000.00,
        "credit_amount": 30000.00,
        "warning": "法定盈余公积累计额达到注册资本50%后可不再提取。",
    },
    {
        "id": 85,
        "description": "股东大会宣告分配现金股利5万元",
        "debit_account": "利润分配-应付现金股利",
        "credit_account": "应付股利",
        "debit_amount": 50000.00,
        "credit_amount": 50000.00,
        "warning": "股利宣告日确认负债，实际支付时冲减应付股利。",
    },
    {
        "id": 86,
        "description": "实际支付股东现金股利5万元",
        "debit_account": "应付股利",
        "credit_account": "银行存款",
        "debit_amount": 50000.00,
        "credit_amount": 50000.00,
        "warning": "支付股利需代扣代缴个人所得税（股息红利20%）。",
    },
    {
        "id": 87,
        "description": "经批准将资本公积10万元转增注册资本",
        "debit_account": "资本公积-资本溢价",
        "credit_account": "实收资本",
        "debit_amount": 100000.00,
        "credit_amount": 100000.00,
        "warning": "资本公积转增资本需办理工商变更登记。",
    },
    {
        "id": 88,
        "description": "收到政府产业扶持补助款5万元",
        "debit_account": "银行存款",
        "credit_account": "营业外收入",
        "debit_amount": 50000.00,
        "credit_amount": 50000.00,
        "warning": "与收益相关的政府补助计入当期损益；与资产相关的确认为递延收益分期转入。",
    },

    # ─── 金融资产（89-92）───────────────────────
    {
        "id": 89,
        "description": "持有的交易性金融资产公允价值上升3万元",
        "debit_account": "交易性金融资产-公允价值变动",
        "credit_account": "公允价值变动损益",
        "debit_amount": 30000.00,
        "credit_amount": 30000.00,
        "warning": "公允价值变动损益属于未实现损益，不影响当期应税所得。",
    },
    {
        "id": 90,
        "description": "出售持有的交易性金融资产，取得价款105万（成本100万）",
        "debit_account": "银行存款",
        "credit_account": "交易性金融资产",
        "debit_amount": 1050000.00,
        "credit_amount": 1000000.00,
        "warning": "出售时同时将持有期间公允价值变动损益结转至投资收益。",
    },
    {
        "id": 91,
        "description": "收到客户交来银行承兑汇票一张，面值5万元",
        "debit_account": "应收票据",
        "credit_account": "应收账款",
        "debit_amount": 50000.00,
        "credit_amount": 50000.00,
        "warning": "应收票据按面值入账，贴现或到期收款时冲减。",
    },
    {
        "id": 92,
        "description": "将持有的银行承兑汇票5万元向银行贴现，取得4.9万元",
        "debit_account": "银行存款",
        "credit_account": "短期借款-票据贴现",
        "debit_amount": 49000.00,
        "credit_amount": 49000.00,
        "warning": "附追索权的票据贴现视为质押借款，贴现息计入财务费用。",
    },

    # ─── 期末结转（93-98）───────────────────────
    {
        "id": 93,
        "description": "月末结转本月主营业务收入30万元至本年利润",
        "debit_account": "主营业务收入",
        "credit_account": "本年利润",
        "debit_amount": 300000.00,
        "credit_amount": 300000.00,
        "warning": "月末将所有收入类科目余额结转至本年利润贷方。",
    },
    {
        "id": 94,
        "description": "月末结转本月主营业务成本20万元至本年利润",
        "debit_account": "本年利润",
        "credit_account": "主营业务成本",
        "debit_amount": 200000.00,
        "credit_amount": 200000.00,
        "warning": "月末将所有成本费用类科目余额结转至本年利润借方。",
    },
    {
        "id": 95,
        "description": "月末结转管理费用5万元至本年利润",
        "debit_account": "本年利润",
        "credit_account": "管理费用",
        "debit_amount": 50000.00,
        "credit_amount": 50000.00,
        "warning": "管理费用为期间费用，月末全额转入本年利润，无余额。",
    },
    {
        "id": 96,
        "description": "年末将本年利润贷方余额20万元转入未分配利润",
        "debit_account": "本年利润",
        "credit_account": "利润分配-未分配利润",
        "debit_amount": 200000.00,
        "credit_amount": 200000.00,
        "warning": "年末本年利润科目无余额，全部转入利润分配。",
    },
    {
        "id": 97,
        "description": "摊销本月经营租入固定资产改良支出3000元",
        "debit_account": "管理费用-装修费摊销",
        "credit_account": "长期待摊费用-装修费",
        "debit_amount": 3000.00,
        "credit_amount": 3000.00,
        "warning": "长期待摊费用在受益期内按月摊销，摊销期不短于3年。",
    },
    {
        "id": 98,
        "description": "支付银行承兑汇票到期款10万元",
        "debit_account": "应付票据",
        "credit_account": "银行存款",
        "debit_amount": 100000.00,
        "credit_amount": 100000.00,
        "warning": "应付票据到期需确保银行存款余额充足，避免逾期产生罚息。",
    },

    # ─── 特殊业务（31）：自产产品发福利 ────────────────
    # 注意：此场景涉及两笔分录，使用 entries 字段替代单条 debit/credit
    {
        "id": 31,
        "description": "公司把自产的一批电脑，作为福利发放给员工，成本5万元，市场售价6万元",
        "warning": "自产产品发福利视同销售，需确认增值税销项税额；同时结转库存商品成本。",
        # 多分录支持：entries 数组中的每条分录独立展示
        "entries": [
            {
                # 分录1：确认职工福利费（视同销售）
                "debit_account": "管理费用-职工福利费",
                "credit_account": "主营业务收入",
                "debit_amount": 67800.00,   # 6万 + 7800销项税（13%）
                "credit_amount": 60000.00,
                "description": "自产电脑发福利，视同销售确认收入",
                "tax_note": "销项税额 = 60,000 × 13% = 7,800元",
            },
            {
                # 分录2：计提销项税（单独列示）
                "debit_account": "管理费用-职工福利费",
                "credit_account": "应交税费-应交增值税(销项税额)",
                "debit_amount": 0.00,
                "credit_amount": 7800.00,
                "description": "自产电脑发福利，计提增值税销项税额",
                "tax_note": None,
            },
            {
                # 分录3：结转库存商品成本
                "debit_account": "主营业务成本",
                "credit_account": "库存商品",
                "debit_amount": 50000.00,
                "credit_amount": 50000.00,
                "description": "结转自产电脑成本",
                "tax_note": None,
            },
        ],
        # 兼容旧字段（用于场景表格展示，取第一条分录的数据）
        "debit_account": "管理费用-职工福利费",
        "credit_account": "主营业务收入 / 应交税费-应交增值税(销项税额) / 库存商品",
        "debit_amount": 67800.00,
        "credit_amount": 60000.00,
    },
]


def find_scenario(user_input: str):
    """
    根据用户输入的自然语言，模糊匹配最相似的业务场景。
    如果匹配不到，返回 None。
    """
    keyword_map = [
        (["请客", "吃饭", "招待", "餐饮", "业务招待", "宴请", "餐费"], 0),
        (["办公用品", "文具", "打印纸", "笔", "墨盒", "硒鼓", "办公耗材"], 1),
        (["差旅", "出差", "交通", "住宿", "机票", "火车票", "高铁", "打车", "出租车"], 2),
        (["房租", "租金", "租赁", "办公室租", "房屋租赁", "租房"], 3),
        (["水电", "水电费", "物业", "物业费", "电费", "水费"], 4),
        (["快递", "邮寄", "邮费", "快递费", "物流"], 5),
        (["培训", "培训费", "教育", "职工教育", "进修"], 6),
        (["咨询", "咨询费", "审计", "审计费", "律师", "律师费", "顾问"], 7),
        (["会议", "会议费", "研讨会", "论坛"], 8),
        (["维修", "修理", "修缮", "维修费", "修理费"], 9),
        (["电脑", "笔记本", "台式机", "服务器", "显示器"], 10),
        (["办公桌", "办公椅", "文件柜", "家具", "办公家具", "沙发"], 11),
        (["机器", "设备", "生产设备", "机床", "仪器"], 12),
        (["汽车", "车辆", "轿车", "货车", "机动车", "购车"], 13),
        (["折旧", "计提折旧", "累计折旧"], 14),
        (["工资", "薪酬", "薪资", "奖金", "工资发放", "发工资", "工资表"], 15),
        (["社保", "五险", "养老保险", "医疗保险", "失业保险", "公积金", "住房公积金"], 16),
        (["福利", "福利费", "过节", "节日福利", "体检", "员工福利"], 17),
        (["计提工资", "工资计提"], 18),
        (["销售", "销售商品", "卖货", "出售", "销售收入", "主营业务收入"], 19),
        (["货款", "收到货款", "收款", "回款", "客户付款", "收到钱", "收货款"], 20),
        (["广告", "推广", "宣传", "营销", "广告费", "推广费", "宣传费"], 21),
        (["运输", "运费", "物流费", "配送", "送货"], 22),
        (["原材料", "材料", "采购材料", "进货", "买材料", "采购原料"], 23),
        (["库存商品", "商品", "采购商品", "进货商品", "买货"], 24),
        (["包装", "包装物", "包装箱", "包装盒"], 25),
        (["增值税", "交税", "缴税", "缴增值税"], 26),
        (["所得税", "企业所得税", "计提所得税"], 27),
        (["利息", "利息收入", "存款利息"], 28),
        (["手续费", "银行手续费", "转账费", "账户管理费"], 29),
        (["自产", "自产产品", "自产商品", "发给员工", "发放给员工", "作为福利", "产品发福利", "自产电脑发福利"], 30),  # id=31
        # ── 所有者权益类 ──
        (["股东投资", "投资款", "注入资本", "注册资本", "实收资本", "注资"], 31),  # id=32
        (["溢价", "资本溢价", "股本溢价", "溢价投资"], 32),  # id=33
        # ── 负债类 ──
        (["短期借款", "银行贷款", "借入", "借款", "向银行借款", "贷款"], 33),  # id=34
        (["计提工资", "工资计提", "计提本月工资", "计提薪酬"], 34),  # id=35
        (["计提折旧", "折旧计提", "生产设备折旧", "设备折旧", "计提生产设备折旧"], 35),  # id=36
        # ── 成本类 ──
        (["完工产品", "完工成本", "结转成本", "产品成本结转", "生产成本结转"], 36),  # id=37
        # ── 税费类 ──
        (["城建税", "教育费附加", "附加税", "城市维护建设税", "计提附加税"], 37),  # id=38
        # ── 进阶场景 ──
        (["理财", "理财产品", "不保本", "购买理财", "交易性金融资产", "购入理财", "买理财"], 38),  # id=39
        (["冲回进项", "进项转出", "进项税额转出", "已抵扣专票", "不合规发票", "已取得专票", "认证抵扣", "专票并认证", "发票不合规", "进项税转出"], 39),  # id=40
        (["旧机器", "机器入股", "旧设备入股", "非货币出资", "评估入股", "实物出资", "机器设备入股", "旧机器设备", "设备入股", "机器设备"], 40),  # id=41
        (["提现", "提取现金", "盘盈", "现金盘盈", "库存现金盘盈", "现金溢余", "现金多了", "库存现金多了", "提现备用"], 41),  # id=42
        (["折扣", "商业折扣", "打折", "实收", "含税销售", "销售折扣", "红字发票", "折扣金额", "折扣销售"], 42),  # id=43
        (["报废", "设备报废", "固定资产清理", "清理费", "残料", "残料收入", "报废清理", "变卖收入", "设备清理", "转入清理"], 43),  # id=44
        (["垫付", "垫付个税", "代垫", "代垫个税", "扣回个税", "个税垫付", "扣回", "垫付个人所得税", "代垫个人所得税", "从工资扣回", "从工资中扣回"], 44),  # id=45
        (["分红", "理财分红", "理财产品分红", "收到分红", "投资收益", "持有期间", "不保本理财分红"], 45),  # id=46
        (["红冲", "暂估入库", "暂估", "红字冲销", "冲暂估", "暂估冲回", "暂估入库红冲", "红冲暂估", "收到发票实际"], 46),  # id=47
        # ── 二期扩展 ──
        (["支付货款", "支付欠款", "付货款", "支付供应商货款", "付供应商款"], 47),  # id=48
        (["退货", "采购退货", "原材料退货", "商品退货", "进货退回", "质量退货"], 48),  # id=49
        (["盘盈", "存货盘盈", "材料盘盈", "盘点多了", "盘点溢余", "库存多了"], 49),  # id=50
        (["盘亏", "存货盘亏", "库存盘亏", "盘点少了", "盘点亏损", "材料少了"], 50),  # id=51
        (["预付", "预付货款", "预付账款", "预付供应商", "预付款项"], 51),  # id=52
        (["预付转入", "预付冲销", "预付账款转库存", "收到货物冲预付"], 52),  # id=53
        (["销售退回", "客户退货", "退货退款", "销货退回", "退货退钱"], 53),  # id=54
        (["现金折扣", "提前付款", "付款优惠", "早付折扣"], 54),  # id=55
        (["计提坏账", "计提坏账准备", "坏账计提", "坏账准备计提", "应收坏账"], 55),  # id=56
        (["坏账核销", "坏账损失", "实际坏账", "确认坏账", "无法收回", "账款收不回", "收不回来"], 56),  # id=57
        (["计提社保", "社保计提", "计提公积金", "计提五险一金", "单位社保", "单位承担社保", "计提单位社保"], 57),  # id=58
        (["计提工会经费", "工会经费", "工会经费计提"], 58),  # id=59
        (["外购礼品", "礼品发员工", "买礼品", "节日礼品", "外购福利", "购买礼品"], 59),  # id=60
        (["备用金", "借支", "员工借款", "借出差费", "预支差旅费"], 60),  # id=61
        (["未交增值税", "转出未交增值税", "结转增值税", "增值税结转", "月末增值税"], 61),  # id=62
        (["管理不善", "非正常损失", "毁损进项", "损失转出", "原材料毁损", "存货毁损"], 62),  # id=63
        (["缴纳印花税", "印花税", "交印花税", "申报印花税"], 63),  # id=64
        (["扣缴个税", "缴纳个税", "交个人所得税", "个税申报", "代扣代缴个税", "缴个税"], 64),  # id=65
        (["房产税", "土地使用税", "计提房产税", "房产税计提"], 65),  # id=66
        (["固定资产盘亏", "设备盘亏", "机器盘亏", "资产盘亏"], 66),  # id=67
        (["计提减值", "减值准备", "固定资产减值", "资产减值", "设备减值"], 67),  # id=68
        (["出售设备", "出售固定资产", "变卖设备", "卖掉设备", "卖旧设备", "卖机器"], 68),  # id=69
        (["装修", "装修费", "办公装修", "店铺装修", "场地装修", "装修支出", "租入装修"], 69),  # id=70
        (["购入专利", "购买专利", "专利权", "购买软件著作权", "购入商标", "购买商标"], 70),  # id=71
        (["无形资产摊销", "摊销无形资产", "专利摊销", "计提摊销"], 71),  # id=72
        (["研发支出", "研发费用", "研究开发", "研发投入", "研发活动"], 72),  # id=73
        (["计提利息", "计提借款利息", "利息计提", "预提利息", "短期借款利息计提"], 73),  # id=74
        (["支付利息", "付利息", "还利息", "支付借款利息", "付银行利息"], 74),  # id=75
        (["资本化利息", "在建工程利息", "工程利息", "利息资本化", "建设期利息"], 75),  # id=76
        (["归还借款", "还贷款", "归还本金", "偿还借款", "归还银行贷款", "还短期借款"], 76),  # id=77
        (["银行承兑汇票", "开承兑", "承兑汇票", "签发汇票", "开出汇票"], 77),  # id=78
        (["结转成本", "结转主营业务成本", "结转销售成本", "成本结转", "结转已销"], 78),  # id=79
        (["废料", "出售废料", "卖废料", "废品收入", "废料收入", "边角料"], 79),  # id=80
        (["收到押金", "收押金", "收取押金", "包装物押金", "保证金收入"], 80),  # id=81
        (["退还押金", "退押金", "返还押金", "退回保证金"], 81),  # id=82
        (["没收押金", "押金不退", "逾期未退", "押金转收入"], 82),  # id=83
        (["提取盈余公积", "提取法定盈余公积", "计提盈余公积", "盈余公积计提"], 83),  # id=84
        (["宣告分红", "宣告股利", "分配股利", "宣告分红", "股东大会分红", "宣告分配"], 84),  # id=85
        (["支付股利", "付股利", "发股利", "分红款", "支付分红", "股东分红"], 85),  # id=86
        (["资本公积转增", "转增资本", "资本公积转资本", "转增注册资本"], 86),  # id=87
        (["政府补助", "政府补贴", "财政补贴", "产业扶持", "扶持资金", "补助款"], 87),  # id=88
        (["公允价值上升", "公允价值上涨", "公允价值增加", "股价上涨", "金融资产升值"], 88),  # id=89
        (["出售理财", "卖掉理财", "赎回理财", "卖出交易性金融资产", "出售金融资产"], 89),  # id=90
        (["收到汇票", "收到承兑汇票", "收承兑", "客户给汇票", "收银行承兑"], 90),  # id=91
        (["票据贴现", "汇票贴现", "承兑贴现", "贴现", "贴现银行"], 91),  # id=92
        (["结转收入", "结转主营业务收入", "收入结转本年利润", "结转损益收入"], 92),  # id=93
        (["结转成本费用", "结转主营业务成本", "成本结转本年利润", "结转费用"], 93),  # id=94
        (["结转管理费用", "管理费用结转", "结转期间费用"], 94),  # id=95
        (["结转本年利润", "年末结转", "本年利润结转", "转入未分配利润", "利润结转"], 95),  # id=96
        (["摊销装修费", "装修费摊销", "长期待摊摊销", "摊销长期待摊"], 96),  # id=97
        (["支付承兑", "兑付承兑", "承兑到期", "承兑付款", "汇票到期付款"], 97),  # id=98
    ]

    for keywords, scenario_id in keyword_map:
        for kw in keywords:
            if kw in user_input:
                return MOCK_SCENARIOS[scenario_id]

    return None
