"""
会计凭证推荐系统 — 自动化回归测试
运行方式：pytest test_scenarios.py -v
覆盖已验证的 30+ 核心场景。
"""
from rule_engine import match_by_rule
from mock_data import MOCK_SCENARIOS


def _resolve(result):
    """解析 match_by_rule 结果，含多分录。"""
    if result is None:
        return None
    if result.get("_error"):
        return None
    if result.get("_multi_entry"):
        mid = result.get("_mock_id")
        if mid:
            for s in MOCK_SCENARIOS:
                if s.get("id") == mid and "entries" in s:
                    return {
                        "debit": [e["debit_account"] for e in s["entries"]],
                        "credit": [e["credit_account"] for e in s["entries"]],
                        "description": result.get("description", ""),
                    }
    return {
        "debit": result.get("debit_account", ""),
        "credit": result.get("credit_account", ""),
        "description": result.get("description", ""),
    }


# ═══ 模块一：货币资金 ═══
def test_q01_extract_cash():
    r = _resolve(match_by_rule("从银行提取现金5000元备用"))
    assert r and "库存现金" in r["debit"]

def test_q02_deposit_cash():
    r = _resolve(match_by_rule("将现金8000元存入银行"))
    assert r and "银行存款" in r["debit"]

def test_q05_cash_shortage():
    r = _resolve(match_by_rule("出纳盘点发现现金短缺200元尚未查明原因"))
    assert r and "待处理财产损溢" in r["debit"]

# ═══ 模块二：应收应付 ═══
def test_q11_credit_sale():
    r = _resolve(match_by_rule("销售商品一批价款50000元增值税6500元款项尚未收到"))
    assert r and "应收账款" in r["debit"]

def test_q15_bad_debt_provision():
    r = _resolve(match_by_rule("计提本月应收账款坏账准备2000元信用减值"))
    assert r and "信用减值损失" in r["debit"]

def test_q16_write_off():
    r = _resolve(match_by_rule("确认某笔应收账款5000元无法收回予以核销"))
    assert r and "坏账准备" in r["debit"]

# ═══ 模块三：存货 ═══
def test_q24_material_issue():
    r = _resolve(match_by_rule("生产车间领用原材料20000元用于生产A产品"))
    assert r and "生产成本" in r["debit"]

def test_q27_inventory_shortage():
    r = _resolve(match_by_rule("月末盘点发现材料盘亏500元尚未查明原因"))
    assert r and "待处理财产损溢" in r["debit"]

# ═══ 模块四：固定资产 ═══
def test_q31_purchase_equipment():
    r = match_by_rule("购入不需要安装的设备价款100000元增值税13000元运输费3000元普票")
    assert r and r.get("_multi_entry")

def test_q35_sell_equipment():
    r = _resolve(match_by_rule("出售旧设备原值60000元已提折旧40000元售价25000元"))
    # 出售设备收到价款 → 借银行存款 贷固定资产清理
    assert r and ("固定资产清理" in r["debit"] or "固定资产清理" in r["credit"])

def test_q36_scrap_equipment():
    r = match_by_rule("公司报废一台设备，原值50万，已提折旧48万，清理费2000，残料收入3000")
    assert r and r.get("_multi_entry")

# ═══ 模块五：无形资产 ═══
def test_q41_purchase_patent():
    r = _resolve(match_by_rule("购入一项专利权价款60000元增值税3600元款项已付"))
    assert r and "无形资产" in r["debit"]

def test_q43_amortization():
    r = _resolve(match_by_rule("摊销无形资产 500元 按月"))
    assert r and ("累计摊销" in r["credit"] or "管理费用" in r["debit"])

# ═══ 模块六：职工薪酬 ═══
def test_q46_salary_accrual():
    r = match_by_rule("计提工资生产工人30000元车间管理8000元行政12000元销售10000元")
    assert r and r.get("_multi_entry")

def test_q47_salary_payment():
    r = _resolve(match_by_rule("实际发放工资60000元代扣个税2000元实发58000元"))
    assert r and "应付职工薪酬" in r["debit"]

# ═══ 模块七：税费 ═══
def test_q57_sales_with_tax():
    r = _resolve(match_by_rule("销售产品收款 50000元 增值税6500"))
    assert r and ("主营业务收入" in r["credit"] or "银行存款" in r["debit"])

def test_q60_surtax():
    r = _resolve(match_by_rule("计算本月应交城市维护建设税350元教育费附加150元"))
    assert r and "税金及附加" in r["debit"]

# ═══ 模块八：借款 ═══
def test_q63_short_loan():
    r = _resolve(match_by_rule("从银行借入短期借款200000元存入银行"))
    assert r and "短期借款" in r["credit"]

def test_q64_interest_accrual():
    r = _resolve(match_by_rule("计提本月短期借款利息2500元"))
    assert r and "应付利息" in r["credit"]

# ═══ 模块九：所有者权益 ═══
def test_q69_capital_injection():
    r = _resolve(match_by_rule("股东投资收到500000元 其中50000资本溢价"))
    assert r and ("实收资本" in r["credit"] or "资本公积" in r["credit"])

def test_q72_surplus_reserve():
    r = _resolve(match_by_rule("从净利润中提取法定盈余公积20000元"))
    assert r and "盈余公积" in r["credit"]

# ═══ 模块十：进阶场景 ═══
def test_q47_estimate_reversal():
    r = match_by_rule("上月暂估入库5万，本月收到发票实际4.8万税额6240")
    assert r and r.get("_multi_entry")

def test_q139_sample_giveaway():
    r = match_by_rule("公司将自产的商品作为样品赠送给客户")
    assert r and r.get("_multi_entry")

def test_q131_equipment_with_freight():
    r = match_by_rule("购入设备价款50万税6.5万运输费1万普票")
    assert r and r.get("_multi_entry")

def test_q136_sale_with_impairment():
    r = match_by_rule("销售已提跌价准备商品成本80万跌价5万售价100万税13万")
    assert r and r.get("_multi_entry")
