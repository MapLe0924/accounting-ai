"""
模拟业务场景数据 —— 高频日常会计业务场景 + 会计科目大全
支持从 scenarios.json 加载场景（可自定义编辑），JSON 缺失时回退到内置数据。
"""

import json
import os

# ─── JSON 场景加载器 ────────────────────────────────────
def _load_scenarios():
    """优先从 scenarios.json 加载，缺失则返回 None"""
    json_path = os.path.join(os.path.dirname(__file__), "scenarios.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return None

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
    "待处理财产损溢": {"code": "1901", "category": "资产类", "nature": "借"},
    "固定资产清理": {"code": "1606", "category": "资产类", "nature": "借"},
    "长期待摊费用": {"code": "1801", "category": "资产类", "nature": "借"},
    "存货跌价准备": {"code": "1471", "category": "资产类", "nature": "贷"},
    "发出商品": {"code": "1406", "category": "资产类", "nature": "借"},
    "递延所得税资产": {"code": "1811", "category": "资产类", "nature": "借"},
    "长期股权投资": {"code": "1511", "category": "资产类", "nature": "借"},
    "债权投资": {"code": "1501", "category": "资产类", "nature": "借"},
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
    "长期应付款": {"code": "2701", "category": "负债类", "nature": "贷"},
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
    "信用减值损失": {"code": "6702", "category": "损益类", "nature": "借"},
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


# ─── 内置场景（scenarios.json 缺失时使用）──────────────
_BUILTIN_SCENARIOS = [
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
        "warning": "现金盘盈必须先通过「待处理财产损溢」过渡，批准后方可转入营业外收入。",
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
                "credit_account": "待处理财产损溢-待处理流动资产损溢",
                "debit_amount": 100.00,
                "credit_amount": 100.00,
                "description": "现金盘点溢余，先转入待处理财产损溢（批准前）",
                "tax_note": "盘盈必须先过待处理财产损溢，不得直接计入营业外收入。",
            },
            {
                "debit_account": "待处理财产损溢-待处理流动资产损溢",
                "credit_account": "营业外收入",
                "debit_amount": 100.00,
                "credit_amount": 100.00,
                "description": "盘盈批准后（无法查明原因），从待处理财产损溢转入营业外收入",
                "tax_note": "现金盘盈转入营业外收入后需缴纳企业所得税。",
            },
        ],
        "debit_account": "库存现金 / 待处理财产损溢",
        "credit_account": "银行存款 / 待处理财产损溢 / 营业外收入",
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
                "debit_account": "累计折旧",
                "credit_account": "固定资产-机器设备",
                "debit_amount": 480000.00,
                "credit_amount": 480000.00,
                "description": "①冲销已计提的累计折旧",
                "tax_note": "将累计折旧科目余额清零。",
            },
            {
                "debit_account": "固定资产清理",
                "credit_account": "固定资产-机器设备",
                "debit_amount": 20000.00,
                "credit_amount": 20000.00,
                "description": "①设备账面净值转入清理（原值50万 - 已提折旧48万）",
                "tax_note": "账面净值 = 500,000 - 480,000 = 20,000元。",
            },
            {
                "debit_account": "固定资产清理",
                "credit_account": "银行存款",
                "debit_amount": 2000.00,
                "credit_amount": 2000.00,
                "description": "②支付设备清理拆卸费用",
                "tax_note": None,
            },
            {
                "debit_account": "银行存款",
                "credit_account": "固定资产清理",
                "debit_amount": 3000.00,
                "credit_amount": 3000.00,
                "description": "③残料出售取得变价收入",
                "tax_note": None,
            },
            {
                "debit_account": "营业外支出-处置非流动资产损失",
                "credit_account": "固定资产清理",
                "debit_amount": 19000.00,
                "credit_amount": 19000.00,
                "description": "④结转报废净损失（20,000+2,000-3,000=19,000）",
                "tax_note": "净损失 = 账面价值20,000 + 清理费2,000 - 残料收入3,000 = 19,000元。",
            },
        ],
        "debit_account": "累计折旧 / 固定资产清理 / 营业外支出",
        "credit_account": "固定资产-机器设备 / 银行存款 / 固定资产清理",
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

    # ═══════════════════════════════════════════════════
    # 三期补漏场景（99-128）：推向 95% 覆盖率
    # ═══════════════════════════════════════════════════

    # ─── 费用报销补漏（99-105）─────────────────────────
    {
        "id": 99,
        "description": "支付本月办公室电话费和网络费600元",
        "debit_account": "管理费用-通讯费",
        "credit_account": "银行存款",
        "debit_amount": 600.00,
        "credit_amount": 600.00,
        "warning": "通讯费需取得运营商开具的发票方可税前扣除。",
    },
    {
        "id": 100,
        "description": "报销员工出差期间的加油费和停车费400元",
        "debit_account": "管理费用-车辆费",
        "credit_account": "银行存款",
        "debit_amount": 400.00,
        "credit_amount": 400.00,
        "warning": "私车公用需签订租车协议，否则相关费用不得税前扣除。",
    },
    {
        "id": 101,
        "description": "支付一年期财产综合保险费1.2万元",
        "debit_account": "管理费用-保险费",
        "credit_account": "银行存款",
        "debit_amount": 12000.00,
        "credit_amount": 12000.00,
        "warning": "跨年度的保险费应分期摊销，不得一次性全额税前扣除。",
    },
    {
        "id": 102,
        "description": "支付公司宣传册和名片印刷费1500元",
        "debit_account": "管理费用-印刷费",
        "credit_account": "银行存款",
        "debit_amount": 1500.00,
        "credit_amount": 1500.00,
        "warning": "印刷费金额较大且用于特定项目时，应考虑资本化。",
    },
    {
        "id": 103,
        "description": "购买车间工人劳保用品（手套、安全帽）2000元",
        "debit_account": "制造费用-劳动保护费",
        "credit_account": "银行存款",
        "debit_amount": 2000.00,
        "credit_amount": 2000.00,
        "warning": "劳动保护费与职工福利费需严格区分，前者可全额税前扣除。",
    },
    {
        "id": 104,
        "description": "低值易耗品（办公桌椅单价低于5000元）一次摊销800元",
        "debit_account": "管理费用-低值易耗品摊销",
        "credit_account": "周转材料",
        "debit_amount": 800.00,
        "credit_amount": 800.00,
        "warning": "单价低于5000元的器具可一次摊销，无需列入固定资产。",
    },
    {
        "id": 105,
        "description": "支付公司大门和围墙修缮费3000元",
        "debit_account": "管理费用-维修费",
        "credit_account": "银行存款",
        "debit_amount": 3000.00,
        "credit_amount": 3000.00,
        "warning": "日常修缮计入管理费用，大修（超原值50%）应资本化。",
    },

    # ─── 存货与成本补漏（106-109）────────────────────
    {
        "id": 106,
        "description": "生产车间领用原材料2.5万元投入生产",
        "debit_account": "生产成本-直接材料",
        "credit_account": "原材料",
        "debit_amount": 25000.00,
        "credit_amount": 25000.00,
        "warning": "材料领用需附领料单，按实际成本或计划成本计价。",
    },
    {
        "id": 107,
        "description": "计提存货跌价准备8000元（可变现净值低于成本）",
        "debit_account": "资产减值损失",
        "credit_account": "存货跌价准备",
        "debit_amount": 8000.00,
        "credit_amount": 8000.00,
        "warning": "存货跌价准备在价值回升时可在原计提范围内转回。",
    },
    {
        "id": 108,
        "description": "周转材料（包装箱）报废，账面价值300元",
        "debit_account": "管理费用",
        "credit_account": "周转材料",
        "debit_amount": 300.00,
        "credit_amount": 300.00,
        "warning": "周转材料报废净损失计入当期损益。",
    },
    {
        "id": 109,
        "description": "车间领用的低值易耗品五五摊销法，首次摊销500元",
        "debit_account": "制造费用",
        "credit_account": "周转材料-低值易耗品摊销",
        "debit_amount": 500.00,
        "credit_amount": 500.00,
        "warning": "五五摊销法：领用时摊销50%，报废时摊销剩余50%。",
    },

    # ─── 薪酬社保补漏（110-112）─────────────────────
    {
        "id": 110,
        "description": "支付员工技能培训机构的职工教育经费5000元",
        "debit_account": "应付职工薪酬-职工教育经费",
        "credit_account": "银行存款",
        "debit_amount": 5000.00,
        "credit_amount": 5000.00,
        "warning": "职工教育经费不超过工资总额8%的部分可税前扣除，超出可结转。",
    },
    {
        "id": 111,
        "description": "支付本月应上缴的工会经费800元",
        "debit_account": "应付职工薪酬-工会经费",
        "credit_account": "银行存款",
        "debit_amount": 800.00,
        "credit_amount": 800.00,
        "warning": "工会经费按工资总额2%计提，上缴后凭工会专用收据税前扣除。",
    },
    {
        "id": 112,
        "description": "因公司裁员支付员工经济补偿金3万元",
        "debit_account": "管理费用-辞退福利",
        "credit_account": "应付职工薪酬-辞退福利",
        "debit_amount": 30000.00,
        "credit_amount": 30000.00,
        "warning": "辞退福利在满足条件时一次性计入当期损益，不得分期确认。",
    },

    # ─── 销售收款补漏（113-114）────────────────────
    {
        "id": 113,
        "description": "预收客户货款5万元，本期交付商品确认收入",
        "debit_account": "预收账款",
        "credit_account": "主营业务收入",
        "debit_amount": 50000.00,
        "credit_amount": 50000.00,
        "warning": "预收账款在商品交付或服务完成时才能确认收入。",
    },
    {
        "id": 114,
        "description": "委托代销商品发出，成本价4万元",
        "debit_account": "发出商品",
        "credit_account": "库存商品",
        "debit_amount": 40000.00,
        "credit_amount": 40000.00,
        "warning": "委托代销在收到代销清单前不得确认收入，发出商品仍属企业存货。",
    },

    # ─── 税费补漏（115-117）───────────────────────
    {
        "id": 115,
        "description": "季度预缴企业所得税1.5万元",
        "debit_account": "应交税费-应交所得税",
        "credit_account": "银行存款",
        "debit_amount": 15000.00,
        "credit_amount": 15000.00,
        "warning": "企业所得税按季度预缴，次年5月31日前完成年度汇算清缴。",
    },
    {
        "id": 116,
        "description": "收到税务机关退还的增值税留抵税额2万元",
        "debit_account": "银行存款",
        "credit_account": "应交税费-应交增值税(进项税额转出)",
        "debit_amount": 20000.00,
        "credit_amount": 20000.00,
        "warning": "留抵退税直接冲减留抵税额，不确认为当期收益。",
    },
    {
        "id": 117,
        "description": "确认递延所得税资产5000元（可抵扣暂时性差异）",
        "debit_account": "递延所得税资产",
        "credit_account": "所得税费用",
        "debit_amount": 5000.00,
        "credit_amount": 5000.00,
        "warning": "递延所得税资产的确认需以很可能取得未来应纳税所得额为限。",
    },

    # ─── 固定资产补漏（118）──────────────────────
    {
        "id": 118,
        "description": "以融资租赁方式租入一台设备，最低租赁付款额现值30万元",
        "debit_account": "固定资产-融资租入固定资产",
        "credit_account": "长期应付款-应付融资租赁款",
        "debit_amount": 300000.00,
        "credit_amount": 300000.00,
        "warning": "融资租入固定资产视同自有资产计提折旧，按现值与公允价孰低入账。",
    },

    # ─── 无形资产补漏（119-120）────────────────────
    {
        "id": 119,
        "description": "内部研发项目完成，满足资本化条件的开发支出8万元转入无形资产",
        "debit_account": "无形资产",
        "credit_account": "研发支出-资本化支出",
        "debit_amount": 80000.00,
        "credit_amount": 80000.00,
        "warning": "仅开发阶段满足资本化条件的支出可转入无形资产，研究阶段全部费用化。",
    },
    {
        "id": 120,
        "description": "出售一项非专利技术，账面价值5万，售价8万",
        "debit_account": "银行存款",
        "credit_account": "无形资产",
        "debit_amount": 80000.00,
        "credit_amount": 50000.00,
        "warning": "出售无形资产净收益计入资产处置损益，需计提增值税（税率6%）。",
    },

    # ─── 投资理财补漏（121-123）───────────────────
    {
        "id": 121,
        "description": "购入某上市公司5%股权作为长期股权投资，价款50万（无重大影响）",
        "debit_account": "长期股权投资",
        "credit_account": "银行存款",
        "debit_amount": 500000.00,
        "credit_amount": 500000.00,
        "warning": "持股比例低于20%且无重大影响的，按成本法或公允价值计量。",
    },
    {
        "id": 122,
        "description": "已核销的坏账又收回8000元",
        "debit_account": "银行存款",
        "credit_account": "坏账准备",
        "debit_amount": 8000.00,
        "credit_amount": 8000.00,
        "warning": "已核销坏账收回时先恢复应收账款再收款，或直接增加坏账准备。",
    },
    {
        "id": 123,
        "description": "购入三年期国债10万元，拟持有至到期",
        "debit_account": "债权投资",
        "credit_account": "银行存款",
        "debit_amount": 100000.00,
        "credit_amount": 100000.00,
        "warning": "持有至到期投资按摊余成本计量，国债利息收入免征企业所得税。",
    },

    # ─── 借款补漏（124）─────────────────────
    {
        "id": 124,
        "description": "外币短期借款因汇率变动产生汇兑损失2000元",
        "debit_account": "财务费用-汇兑损益",
        "credit_account": "短期借款",
        "debit_amount": 2000.00,
        "credit_amount": 2000.00,
        "warning": "外币货币性项目在资产负债表日按即期汇率折算，差额计入汇兑损益。",
    },

    # ─── 期末结转补漏（125-127）───────────────────
    {
        "id": 125,
        "description": "月末结转销售费用3万元至本年利润",
        "debit_account": "本年利润",
        "credit_account": "销售费用",
        "debit_amount": 30000.00,
        "credit_amount": 30000.00,
        "warning": "销售费用为期间费用，月末全额转入本年利润，无余额。",
    },
    {
        "id": 126,
        "description": "月末结转财务费用2000元至本年利润",
        "debit_account": "本年利润",
        "credit_account": "财务费用",
        "debit_amount": 2000.00,
        "credit_amount": 2000.00,
        "warning": "如财务费用为贷方余额（利息收入大于支出），则做相反分录。",
    },
    {
        "id": 127,
        "description": "年末确认当期所得税费用，结转至本年利润",
        "debit_account": "本年利润",
        "credit_account": "所得税费用",
        "debit_amount": 35000.00,
        "credit_amount": 35000.00,
        "warning": "所得税费用结转后本年利润余额即为净利润。",
    },

    # ─── 所有者权益与特殊业务（128-130）─────────────
    {
        "id": 128,
        "description": "经批准用盈余公积弥补以前年度亏损2万元",
        "debit_account": "盈余公积",
        "credit_account": "利润分配-盈余公积补亏",
        "debit_amount": 20000.00,
        "credit_amount": 20000.00,
        "warning": "盈余公积补亏需经董事会或股东大会批准，补亏后盈余公积不得低于注册资本的25%。",
    },
    {
        "id": 129,
        "description": "宣告发放股票股利，按面值计算3万元",
        "debit_account": "利润分配-转作股本的股利",
        "credit_account": "实收资本",
        "debit_amount": 30000.00,
        "credit_amount": 30000.00,
        "warning": "股票股利不涉及现金流出，仅影响所有者权益内部结构。",
    },
    {
        "id": 130,
        "description": "发现上年少计提折旧5000元，进行前期差错更正",
        "debit_account": "以前年度损益调整",
        "credit_account": "累计折旧",
        "debit_amount": 5000.00,
        "credit_amount": 5000.00,
        "warning": "不重要的前期差错直接调整当期；重要的需追溯重述比较财务报表。",
    },

    # ═══════════════════════════════════════════════════
    # 四期复杂进阶场景（131-138）
    # ═══════════════════════════════════════════════════

    # Q1: 购入设备含运费（普票不可抵扣，计入原值）
    {
        "id": 131,
        "description": "购入设备一台，价款50万元，增值税6.5万元，另支付运输费1万元（普票不可抵扣），款项均以银行存款支付",
        "warning": "运输费取得普通发票不可抵扣进项税，应计入固定资产原值（50万+1万=51万）。",
        "entries": [
            {
                "debit_account": "固定资产-机器设备",
                "credit_account": "银行存款",
                "debit_amount": 510000.00,
                "credit_amount": 575000.00,
                "description": "设备原值=价款50万+运费1万=51万",
                "tax_note": "同时借记：应交税费-应交增值税(进项税额) 65,000元。",
            },
        ],
        "debit_account": "固定资产-机器设备 / 应交税费-应交增值税(进项税额)",
        "credit_account": "银行存款",
        "debit_amount": 575000.00,
        "credit_amount": 575000.00,
    },

    # Q2: 计提工资（分部门归集）
    {
        "id": 132,
        "description": "计提本月工资：生产工人20万元，车间管理人员5万元，行政管理人员8万元，销售人员6万元",
        "warning": "车间管理人员工资计入「制造费用」而非「管理费用」，生产工人工资计入「生产成本」。",
        "entries": [
            {
                "debit_account": "生产成本-直接人工",
                "credit_account": "应付职工薪酬-工资",
                "debit_amount": 200000.00,
                "credit_amount": 200000.00,
                "description": "生产工人工资计入生产成本",
                "tax_note": None,
            },
            {
                "debit_account": "制造费用-工资",
                "credit_account": "应付职工薪酬-工资",
                "debit_amount": 50000.00,
                "credit_amount": 50000.00,
                "description": "车间管理人员工资计入制造费用（非管理费用！）",
                "tax_note": "制造费用最终分配至产品成本。",
            },
            {
                "debit_account": "管理费用-工资",
                "credit_account": "应付职工薪酬-工资",
                "debit_amount": 80000.00,
                "credit_amount": 80000.00,
                "description": "行政管理人员工资计入管理费用",
                "tax_note": None,
            },
            {
                "debit_account": "销售费用-工资",
                "credit_account": "应付职工薪酬-工资",
                "debit_amount": 60000.00,
                "credit_amount": 60000.00,
                "description": "销售人员工资计入销售费用",
                "tax_note": None,
            },
        ],
        "debit_account": "生产成本 / 制造费用 / 管理费用 / 销售费用",
        "credit_account": "应付职工薪酬-工资",
        "debit_amount": 390000.00,
        "credit_amount": 390000.00,
    },

    # Q3: 销售折让（只冲收入，不冲成本）
    {
        "id": 133,
        "description": "上月销售商品货款10万元，因质量问题给予10%销售折让，已开具红字增值税专用发票",
        "warning": "销售折让只冲减收入，不涉及退货故不冲减成本。折让金额=10万×10%=1万元，销项税=1万×13%=1300元。",
        "entries": [
            {
                "debit_account": "主营业务收入",
                "credit_account": "应收账款",
                "debit_amount": 10000.00,
                "credit_amount": 11300.00,
                "description": "销售折让冲减收入1万元（10万×10%）",
                "tax_note": "同时借记：应交税费-应交增值税(销项税额) 1,300元（10,000×13%）。不涉及库存商品和主营业务成本！",
            },
        ],
        "debit_account": "主营业务收入 / 应交税费-应交增值税(销项税额)",
        "credit_account": "应收账款",
        "debit_amount": 11300.00,
        "credit_amount": 11300.00,
    },

    # Q4: 预付保险费 + 月末摊销
    {
        "id": 134,
        "description": "预付明年全年财产保险费2.4万元，当月月末摊销本月应负担的保险费",
        "warning": "支付时先通过「预付账款」核算，不得一次性计入当期费用。每月摊销额=24,000÷12=2,000元。",
        "entries": [
            {
                "debit_account": "预付账款",
                "credit_account": "银行存款",
                "debit_amount": 24000.00,
                "credit_amount": 24000.00,
                "description": "①支付全年保险费，先计入预付账款",
                "tax_note": "预付账款属于资产，在受益期内逐月摊销。",
            },
            {
                "debit_account": "管理费用-保险费",
                "credit_account": "预付账款",
                "debit_amount": 2000.00,
                "credit_amount": 2000.00,
                "description": "②月末摊销当月保险费（24,000÷12=2,000）",
                "tax_note": "每月摊销额=24,000÷12=2,000元。",
            },
        ],
        "debit_account": "预付账款 / 管理费用-保险费",
        "credit_account": "银行存款 / 预付账款",
        "debit_amount": 24000.00,
        "credit_amount": 24000.00,
    },

    # Q5: 短期借款 + 按月计提付息
    {
        "id": 135,
        "description": "向银行借入短期借款30万元，年利率6%，按月计提并支付利息",
        "warning": "按月付息时需先计提（权责发生制），再支付。月利息=300,000×6%÷12=1,500元。",
        "entries": [
            {
                "debit_account": "银行存款",
                "credit_account": "短期借款",
                "debit_amount": 300000.00,
                "credit_amount": 300000.00,
                "description": "①借入短期借款30万元",
                "tax_note": None,
            },
            {
                "debit_account": "财务费用-利息支出",
                "credit_account": "应付利息",
                "debit_amount": 1500.00,
                "credit_amount": 1500.00,
                "description": "②月末计提本月利息（300,000×6%÷12=1,500）",
                "tax_note": "权责发生制：利息需按期计提，不能支付时直接计入财务费用。",
            },
            {
                "debit_account": "应付利息",
                "credit_account": "银行存款",
                "debit_amount": 1500.00,
                "credit_amount": 1500.00,
                "description": "③支付本月借款利息",
                "tax_note": "支付时冲减已计提的应付利息。",
            },
        ],
        "debit_account": "银行存款 / 财务费用-利息支出 / 应付利息",
        "credit_account": "短期借款 / 应付利息 / 银行存款",
        "debit_amount": 303000.00,
        "credit_amount": 303000.00,
    },

    # Q6: 销售已计提跌价准备的商品
    {
        "id": 136,
        "description": "销售一批商品，售价100万元，增值税13万元，该批商品成本80万元，已计提存货跌价准备5万元",
        "warning": "结转成本时需同时转销存货跌价准备，主营业务成本=80万-5万=75万，不是80万。",
        "entries": [
            {
                "debit_account": "银行存款",
                "credit_account": "主营业务收入",
                "debit_amount": 1130000.00,
                "credit_amount": 1000000.00,
                "description": "①确认销售收入（售价100万+增值税13万）",
                "tax_note": "同时贷记：应交税费-应交增值税(销项税额) 130,000元。",
            },
            {
                "debit_account": "主营业务成本",
                "credit_account": "库存商品",
                "debit_amount": 750000.00,
                "credit_amount": 800000.00,
                "description": "②结转成本并转销跌价准备（80万-5万=75万）",
                "tax_note": "同时借记：存货跌价准备 50,000元。主营业务成本=800,000-50,000=750,000元。",
            },
        ],
        "debit_account": "银行存款 / 主营业务成本 / 存货跌价准备",
        "credit_account": "主营业务收入 / 应交税费-应交增值税(销项税额) / 库存商品",
        "debit_amount": 1130000.00,
        "credit_amount": 1130000.00,
    },

    # Q7: 计提坏账（新准则信用减值损失）+ 核销
    {
        "id": 137,
        "description": "应收账款余额50万元，按5%计提坏账准备，次月确认其中2.5万元无法收回予以核销",
        "warning": "新准则下坏账计提借方为「信用减值损失」，核销时只转销坏账准备不涉及损益。",
        "entries": [
            {
                "debit_account": "信用减值损失-计提坏账准备",
                "credit_account": "坏账准备",
                "debit_amount": 25000.00,
                "credit_amount": 25000.00,
                "description": "①计提坏账准备（50万×5%=25,000）",
                "tax_note": "新准则使用「信用减值损失」，不再使用「资产减值损失」。",
            },
            {
                "debit_account": "坏账准备",
                "credit_account": "应收账款",
                "debit_amount": 25000.00,
                "credit_amount": 25000.00,
                "description": "②确认实际坏账，核销应收账款",
                "tax_note": "核销时不涉及损益科目，仅冲销坏账准备和应收账款。",
            },
        ],
        "debit_account": "信用减值损失 / 坏账准备",
        "credit_account": "坏账准备 / 应收账款",
        "debit_amount": 25000.00,
        "credit_amount": 25000.00,
    },

    # Q8: 提取盈余公积 + 宣告股利
    {
        "id": 138,
        "description": "本年净利润100万元，提取法定盈余公积10%、任意盈余公积5%，宣告分配现金股利20万元",
        "warning": "法定与任意盈余公积需分开计提（明细科目不同），宣告股利贷方为「应付股利」。",
        "entries": [
            {
                "debit_account": "利润分配-提取法定盈余公积",
                "credit_account": "盈余公积-法定盈余公积",
                "debit_amount": 100000.00,
                "credit_amount": 100000.00,
                "description": "①提取法定盈余公积（100万×10%=10万）",
                "tax_note": "法定盈余公积累计额达注册资本50%后可不再提取。",
            },
            {
                "debit_account": "利润分配-提取任意盈余公积",
                "credit_account": "盈余公积-任意盈余公积",
                "debit_amount": 50000.00,
                "credit_amount": 50000.00,
                "description": "②提取任意盈余公积（100万×5%=5万）",
                "tax_note": "任意盈余公积提取比例由股东大会决定。",
            },
            {
                "debit_account": "利润分配-应付现金股利或利润",
                "credit_account": "应付股利",
                "debit_amount": 200000.00,
                "credit_amount": 200000.00,
                "description": "③宣告分配现金股利20万元",
                "tax_note": "贷方为「应付股利」，不是「应付账款」或「其他应付款」。",
            },
        ],
        "debit_account": "利润分配",
        "credit_account": "盈余公积 / 应付股利",
        "debit_amount": 350000.00,
        "credit_amount": 350000.00,
    },

    # ═══════════════════════════════════════════════════
    # 样品赠送（自产产品赠送客户，视同销售但不确认收入）
    # ═══════════════════════════════════════════════════
    {
        "id": 139,
        "description": "将自产商品作为样品赠送给客户，成本8,000元，公允价值10,000元，增值税率13%",
        "warning": "样品赠送视同销售但不确认收入，成本+销项税直接计入销售费用。销项税=10,000×13%=1,300元。",
        "entries": [
            {
                "debit_account": "销售费用-样品费",
                "credit_account": "库存商品",
                "debit_amount": 9300.00,
                "credit_amount": 8000.00,
                "description": "样品赠送：按成本+销项税计入销售费用",
                "tax_note": "同时贷记：应交税费——应交增值税(销项税额) 1,300元（10,000×13%）。",
            },
        ],
        "debit_account": "销售费用-样品费",
        "credit_account": "库存商品 / 应交税费-应交增值税(销项税额)",
        "debit_amount": 9300.00,
        "credit_amount": 9300.00,
    },

    # ═══════════════════════════════════════════════════
    # 采购原材料含税赊购（id=140）
    # ═══════════════════════════════════════════════════
    {
        "id": 140,
        "description": "采购原材料一批，价款30,000元，增值税3,900元，货款尚未支付，材料已入库",
        "warning": "材料已入库但货款未付，应确认应付账款；进项税额凭专票抵扣。",
        "entries": [
            {
                "debit_account": "原材料",
                "credit_account": "应付账款",
                "debit_amount": 30000.00,
                "credit_amount": 30000.00,
                "description": "材料验收入库，按价款确认原材料",
                "tax_note": None,
            },
            {
                "debit_account": "应交税费-应交增值税(进项税额)",
                "credit_account": "应付账款",
                "debit_amount": 3900.00,
                "credit_amount": 3900.00,
                "description": "取得增值税专用发票，确认进项税额",
                "tax_note": "进项税额 = 30,000 × 13% = 3,900元，凭专票认证抵扣。",
            },
        ],
        "debit_account": "原材料 / 应交税费-应交增值税(进项税额)",
        "credit_account": "应付账款",
        "debit_amount": 33900.00,
        "credit_amount": 33900.00,
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

# ── 优先从 JSON 加载，回退到内置数据 ──
MOCK_SCENARIOS = _load_scenarios() or _BUILTIN_SCENARIOS


def find_scenario(user_input: str):
    """
    根据用户输入的自然语言，模糊匹配最相似的业务场景。
    如果匹配不到，返回 None。
    """
    keyword_map = [
        (["请客", "吃饭", "招待", "餐饮", "业务招待", "宴请", "餐费"], 1),
        (["办公用品", "文具", "打印纸", "笔", "墨盒", "硒鼓", "办公耗材"], 2),
        (["差旅", "出差", "交通", "住宿", "机票", "火车票", "高铁", "打车", "出租车"], 3),
        (["房租", "租金", "租赁", "办公室租", "房屋租赁", "租房"], 4),
        (["水电", "水电费", "物业", "物业费", "电费", "水费"], 5),
        (["快递", "邮寄", "邮费", "快递费", "物流"], 6),
        (["培训", "培训费", "教育", "职工教育", "进修"], 7),
        (["咨询", "咨询费", "审计", "审计费", "律师", "律师费", "顾问"], 8),
        (["会议", "会议费", "研讨会", "论坛"], 9),
        (["维修", "修理", "修缮", "维修费", "修理费"], 10),
        (["电脑", "笔记本", "台式机", "服务器", "显示器"], 11),
        (["办公桌", "办公椅", "文件柜", "家具", "办公家具", "沙发"], 12),
        (["机器", "设备", "生产设备", "机床", "仪器"], 13),
        (["汽车", "车辆", "轿车", "货车", "机动车", "购车"], 14),
        (["折旧", "计提折旧", "累计折旧"], 15),
        (["工资", "薪酬", "薪资", "奖金", "工资发放", "发工资", "工资表"], 16),
        (["社保", "五险", "养老保险", "医疗保险", "失业保险", "公积金", "住房公积金"], 17),
        (["福利", "福利费", "过节", "节日福利", "体检", "员工福利"], 18),
        (["计提工资", "工资计提"], 19),
        (["销售", "销售商品", "卖货", "出售", "销售收入", "主营业务收入"], 20),
        (["货款", "收到货款", "收款", "回款", "客户付款", "收到钱", "收货款"], 21),
        (["广告", "推广", "宣传", "营销", "广告费", "推广费", "宣传费"], 22),
        (["运输", "运费", "物流费", "配送", "送货"], 23),
        (["原材料", "材料", "采购材料", "进货", "买材料", "采购原料"], 24),
        (["库存商品", "商品", "采购商品", "进货商品", "买货"], 25),
        (["包装", "包装物", "包装箱", "包装盒"], 26),
        (["增值税", "交税", "缴税", "缴增值税"], 27),
        (["所得税", "企业所得税", "计提所得税"], 28),
        (["利息", "利息收入", "存款利息"], 29),
        (["手续费", "银行手续费", "转账费", "账户管理费"], 30),
        (["自产", "自产产品", "自产商品", "发给员工", "发放给员工", "作为福利", "产品发福利", "自产电脑发福利"], 31),
        (["股东投资", "投资款", "注入资本", "注册资本", "实收资本", "注资"], 32),
        (["溢价", "资本溢价", "股本溢价", "溢价投资"], 33),
        (["短期借款", "银行贷款", "借入", "借款", "向银行借款", "贷款"], 34),
        (["计提工资", "工资计提", "计提本月工资", "计提薪酬"], 35),
        (["计提折旧", "折旧计提", "生产设备折旧", "设备折旧", "计提生产设备折旧"], 36),
        (["完工产品", "完工成本", "结转成本", "产品成本结转", "生产成本结转"], 37),
        (["城建税", "教育费附加", "附加税", "城市维护建设税", "计提附加税"], 38),
        (["理财", "理财产品", "不保本", "购买理财", "交易性金融资产"], 39),
        (["冲回进项", "进项转出", "进项税额转出", "已抵扣专票", "不合规发票"], 40),
        (["旧机器", "机器入股", "旧设备入股", "非货币出资", "评估入股", "实物出资"], 41),
        (["提现", "提取现金", "盘盈", "现金盘盈", "库存现金盘盈", "现金溢余"], 42),
        (["折扣", "商业折扣", "打折", "实收", "含税销售", "销售折扣"], 43),
        (["报废", "设备报废", "固定资产清理", "清理费", "残料", "残料收入", "报废清理"], 44),
        (["垫付", "垫付个税", "代垫", "代垫个税", "扣回个税", "个税垫付"], 45),
        (["分红", "理财分红", "理财产品分红", "收到分红", "投资收益"], 46),
        (["红冲", "暂估入库", "暂估", "红字冲销", "冲暂估", "暂估冲回"], 47),
        (["支付货款", "支付欠款", "付货款", "支付供应商货款", "付供应商款"], 48),
        (["退货", "采购退货", "原材料退货", "商品退货", "进货退回"], 49),
        (["盘盈", "存货盘盈", "材料盘盈", "盘点多了", "盘点溢余"], 50),
        (["盘亏", "存货盘亏", "库存盘亏", "盘点少了", "盘点亏损"], 51),
        (["预付", "预付货款", "预付账款", "预付供应商", "预付款项"], 52),
        (["备用金", "借支", "员工借款", "借出差费", "预支差旅费"], 61),
        (["缴纳印花税", "印花税", "交印花税", "申报印花税"], 64),
        (["计提社保", "社保计提", "计提公积金", "单位承担社保"], 58),
        (["样品赠送", "样品赠送给客户", "作为样品赠送", "赠送样品"], 139),
    ]

    for keywords, scenario_id in keyword_map:
        for kw in keywords:
            if kw in user_input:
                # 按 id 查找（不受索引错位影响）
                for s in MOCK_SCENARIOS:
                    if s["id"] == scenario_id:
                        return s
                # 兜底：旧式索引
                if 0 <= scenario_id < len(MOCK_SCENARIOS):
                    return MOCK_SCENARIOS[scenario_id]

    return None
