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

    # ─── 特殊业务：自产产品发福利（必须放在所有固定资产规则之前） ──
    # 自产产品发福利涉及视同销售，需要做多笔分录，由 app.py 特殊处理
    {
        "keywords": ["自产", "自产产品", "自产商品", "产品发福利", "自产电脑发福利"],
        "debit": "__MULTI_ENTRY__:mock_data:31",  # 特殊标记：指向 mock_data id=31 的多分录数据
        "credit": "__MULTI_ENTRY__:mock_data:31",
        "debit_amount": 0,
        "credit_amount": 0,
        "description": "自产产品发放给员工作为福利（视同销售，需做多笔分录）",
        "warning": "自产产品发福利视同销售，需确认增值税销项税额；同时结转库存商品成本。",
        "_multi_entry": True,
        "_mock_id": 31,
    },

    # ─── 维修类（必须放在固定资产之前，防止"维修电脑"误匹配到固定资产） ──
    {
        "keywords": ["维修", "修理", "修缮", "维修费", "修理费"],
        "debit": "管理费用-维修费",
        "credit": "银行存款",
        "description": "日常维修维护费用",
        "warning": "大额维修支出（超过原值50%）建议确认是否属于固定资产改良支出，应资本化处理。",
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

    # ─── 所有者权益类 ──────────────────────────────────
    {
        "keywords": ["股东投资", "投资款", "注入资本", "注册资本", "实收资本", "注资"],
        "debit": "银行存款",
        "credit": "实收资本",
        "description": "股东投入资本",
        "warning": "股东投资款需出具验资报告，超出注册资本部分应计入资本公积。",
    },
    {
        "keywords": ["溢价", "资本溢价", "股本溢价", "溢价投资"],
        "debit": "银行存款",
        "credit": "资本公积-资本溢价",
        "description": "股东溢价投资形成的资本公积",
        "warning": "资本溢价不得用于弥补亏损，可用于转增资本。",
    },

    # ─── 负债类 ────────────────────────────────────────
    {
        "keywords": ["短期借款", "银行贷款", "借入", "向银行借款", "贷款"],
        "debit": "银行存款",
        "credit": "短期借款",
        "description": "向银行借入短期借款",
        "warning": "短期借款期限一般在1年以内，需按期计提利息。",
    },
    {
        "keywords": ["长期借款", "长期贷款", "长期银行贷款"],
        "debit": "银行存款",
        "credit": "长期借款",
        "description": "向银行借入长期借款",
        "warning": "长期借款期限超过1年，利息支出可能需资本化处理。",
    },
    {
        "keywords": ["计提工资", "工资计提", "计提本月工资", "计提薪酬", "计提员工工资", "计提本月员工工资", "计提工资总额", "计提员工薪酬", "计提 工资"],
        "debit": "管理费用-工资",
        "credit": "应付职工薪酬-工资",
        "description": "计提本月员工工资",
        "warning": "工资计提需与实发数核对，差异做调整分录。",
    },
    {
        "keywords": ["计提社保", "社保计提", "计提公积金", "计提五险一金"],
        "debit": "管理费用-社保公积金",
        "credit": "应付职工薪酬-社保公积金",
        "description": "计提单位承担的社保和公积金",
        "warning": "单位承担部分可税前扣除，个人部分从工资代扣。",
    },

    # ─── 成本类 ────────────────────────────────────────
    {
        "keywords": ["计提折旧", "折旧计提", "生产设备折旧", "设备折旧", "计提生产设备折旧", "计提 折旧"],
        "debit": "制造费用-折旧费",
        "credit": "累计折旧",
        "description": "计提生产设备折旧（计入制造费用）",
        "warning": "生产设备折旧计入制造费用，最终分配至产品成本。折旧方法一经确定不得随意变更。",
    },
    {
        "keywords": ["完工产品", "完工成本", "产品成本结转", "生产成本结转"],
        "debit": "库存商品",
        "credit": "生产成本",
        "description": "结转完工产品成本",
        "warning": "完工产品成本结转需附成本计算单，确认料工费分配合理。",
    },

    # ─── 税费类 ────────────────────────────────────────
    {
        "keywords": ["交税", "缴税", "增值税", "所得税", "附加税", "印花税", "税费"],
        "debit": "应交税费",
        "credit": "银行存款",
        "description": "缴纳税费",
        "warning": "请确认各项税费的申报期限，避免逾期产生滞纳金。",
    },
    {
        "keywords": ["城建税", "教育费附加", "城市维护建设税", "计提附加税"],
        "debit": "税金及附加",
        "credit": "应交税费-应交城建税及教育费附加",
        "description": "计提城市维护建设税及教育费附加",
        "warning": "城建税税率7%（城市）或5%（县城），教育费附加3%，地方教育附加2%。",
    },

    # ─── 进阶复杂场景（多分录，必须放在通用规则之前）─────
    # Q2: 股东旧机器入股 → 必须在「机器/设备」通用规则之前
    {
        "keywords": ["机器入股", "设备入股", "旧机器入股", "旧设备入股", "非货币出资", "实物出资", "评估入股", "机器设备入股"],
        "debit": "固定资产-机器设备",
        "credit": "实收资本",
        "description": "股东以旧机器设备评估入股",
        "warning": "股东以非货币资产出资需经评估作价并出具验资报告，不得高估或低估。",
    },
    # Q1: 支付已抵扣专票广告费 → 必须在「广告」通用规则之前
    {
        "keywords": ["进项税额转出", "进项转出", "冲回进项税", "已抵扣专票", "已取得专票", "认证抵扣", "不合规发票", "发票不合规", "专票并认证"],
        "debit": "__MULTI_ENTRY__:mock_data:40",
        "credit": "__MULTI_ENTRY__:mock_data:40",
        "description": "支付已抵扣专票费用，冲回进项税额（多分录）",
        "warning": "不合规发票对应的进项税额不得抵扣，已抵扣的需做进项税额转出处理。",
        "_multi_entry": True,
        "_mock_id": 40,
    },
    # Q3: 提现 + 现金盘盈
    {
        "keywords": ["提取现金", "提现", "现金盘盈", "盘盈", "现金多了", "现金溢余", "库存现金多了", "现金盘点溢余"],
        "debit": "__MULTI_ENTRY__:mock_data:42",
        "credit": "__MULTI_ENTRY__:mock_data:42",
        "description": "提取现金备用 + 现金盘点盘盈（多分录）",
        "warning": "现金盘盈先计入待处理财产损溢，查明原因经批准后转营业外收入。",
        "_multi_entry": True,
        "_mock_id": 42,
    },
    # Q5: 固定资产报废清理
    {
        "keywords": ["设备报废", "固定资产报废", "报废设备", "报废清理", "固定资产清理", "清理费", "残料收入", "残料变卖", "设备清理"],
        "debit": "__MULTI_ENTRY__:mock_data:44",
        "credit": "__MULTI_ENTRY__:mock_data:44",
        "description": "固定资产报废清理（多分录：转入清理→支付清理费→残料收入→结转损益）",
        "warning": "固定资产报废需经管理层审批，净损失计入营业外支出，税前扣除需专项申报。",
        "_multi_entry": True,
        "_mock_id": 44,
    },
    # Q6: 替员工垫付个税
    {
        "keywords": ["垫付个税", "代垫个税", "垫付个人所得税", "代垫个人所得税", "扣回个税", "个税扣回"],
        "debit": "__MULTI_ENTRY__:mock_data:45",
        "credit": "__MULTI_ENTRY__:mock_data:45",
        "description": "替员工垫付个人所得税，下月从工资扣回（多分录）",
        "warning": "企业垫付员工个税属于代垫款性质，不得直接计入费用，应通过其他应收款核算。",
        "_multi_entry": True,
        "_mock_id": 45,
    },
    # Q7: 购买理财 + 收到分红
    {
        "keywords": ["理财分红", "收到分红", "理财产品分红", "持有期间收到", "不保本理财分红"],
        "debit": "__MULTI_ENTRY__:mock_data:46",
        "credit": "__MULTI_ENTRY__:mock_data:46",
        "description": "购买不保本理财产品并收到持有期间分红（多分录）",
        "warning": "不保本理财属于交易性金融资产；持有期间收益确认为投资收益，非利息收入。",
        "_multi_entry": True,
        "_mock_id": 46,
    },
    # Q8: 红冲暂估入库
    {
        "keywords": ["红冲暂估", "暂估红冲", "冲暂估", "暂估冲回", "暂估入库红冲", "红字冲销暂估", "暂估入库收到发票"],
        "debit": "__MULTI_ENTRY__:mock_data:47",
        "credit": "__MULTI_ENTRY__:mock_data:47",
        "description": "红冲上月暂估入库，按发票实际金额正式入账（多分录）",
        "warning": "暂估入库应在次月初红冲，收到发票后按实际金额入账并确认进项税额。",
        "_multi_entry": True,
        "_mock_id": 47,
    },
    # 购买理财产品（单分录）
    {
        "keywords": ["购买理财", "理财产品", "不保本理财", "购入理财", "买理财"],
        "debit": "交易性金融资产",
        "credit": "银行存款",
        "description": "购买不保本银行理财产品",
        "warning": "不保本理财产品应分类为交易性金融资产，按公允价值计量且变动计入当期损益。",
    },
    # Q4: 商业折扣销售
    {
        "keywords": ["商业折扣", "红字发票", "折扣销售", "销售折扣", "打折销售", "折扣金额"],
        "debit": "银行存款",
        "credit": "主营业务收入 / 应交税费-应交增值税(销项税额)",
        "description": "商品销售给予商业折扣，按折扣后金额确认收入",
        "warning": "商业折扣按折扣后金额确认收入：不含税收入=实际收款÷1.13，销项税额=不含税收入×13%。",
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
        "keywords": ["软件", "软件费", "系统", "系统费", "SaaS", "云服务", "会员"],
        "debit": "管理费用-软件服务费",
        "credit": "银行存款",
        "description": "软件订阅、SaaS服务、会员费等",
        "warning": None,
    },

    # ═══════════════════════════════════════════════════
    # 二期扩展规则（对应 mock_data id=48~98）
    # ═══════════════════════════════════════════════════

    # ── 往来款项 ──
    {"keywords": ["支付 货款", "支付 欠款", "付 供应商", "支付 供应商款", "付 货款", "支付前欠"], "debit": "应付账款", "credit": "银行存款", "description": "支付前欠供应商货款", "warning": "支付应付账款不涉及损益，仅影响资产负债项目。"},
    {"keywords": ["采购 退货", "原材料 退货", "商品 退货", "进货 退回", "质量 退货", "退货 采购"], "debit": "应付账款", "credit": "原材料", "description": "采购退货冲减应付账款和存货", "warning": "退货需取得红字发票或退货单，同时冲减进项税额。"},
    {"keywords": ["盘盈", "存货盘盈", "材料盘盈", "盘点多了", "盘点溢余", "库存多了"], "debit": "原材料", "credit": "营业外收入", "description": "存货盘点盘盈", "warning": "存货盘盈先通过待处理财产损溢归集，批准后冲减管理费用。"},
    {"keywords": ["盘亏", "存货盘亏", "库存盘亏", "盘点少了", "盘点亏损", "材料少了"], "debit": "营业外支出", "credit": "库存商品", "description": "存货盘点盘亏", "warning": "管理不善造成的盘亏进项税额需转出；自然灾害造成的无需转出。"},
    {"keywords": ["预付", "预付货款", "预付账款", "预付供应商", "预付款项"], "debit": "预付账款", "credit": "银行存款", "description": "预付供应商货款", "warning": "预付款项在未收到货物或服务前属于资产，收到后再冲减预付账款。"},
    {"keywords": ["销售 退回", "客户 退货", "退货 退款", "销货 退回", "退货 退钱", "销售退货 退款"], "debit": "主营业务收入", "credit": "银行存款", "description": "销售退回冲减收入", "warning": "销售退回需开具红字发票，同时冲减销项税额并转回已结转成本。"},
    {"keywords": ["现金折扣", "提前付款", "付款优惠", "早付折扣"], "debit": "财务费用-现金折扣", "credit": "应收账款", "description": "客户提前付款给予现金折扣", "warning": "现金折扣计入财务费用，不得冲减销售收入。"},

    # ── 坏账 ──
    {"keywords": ["计提坏账", "计提坏账准备", "坏账计提", "坏账准备计提", "应收坏账"], "debit": "资产减值损失", "credit": "坏账准备", "description": "计提坏账准备", "warning": "坏账准备计提比例需符合企业会计政策，税前扣除需符合税法条件。"},
    {"keywords": ["坏账核销", "坏账损失", "实际坏账", "确认坏账", "无法收回", "账款收不回", "收不回来"], "debit": "坏账准备", "credit": "应收账款", "description": "实际发生坏账核销应收账款", "warning": "实际核销坏账需取得充分证据（如债务人破产、注销等）。"},

    # ── 薪酬社保 ──
    {"keywords": ["计提社保", "社保计提", "计提公积金", "计提五险一金", "单位社保", "单位承担社保", "计提单位社保"], "debit": "管理费用-社保公积金", "credit": "应付职工薪酬-社保公积金", "description": "计提单位承担的社保和公积金", "warning": "单位承担的社保公积金可税前扣除。"},
    {"keywords": ["计提工会经费", "工会经费", "工会经费计提"], "debit": "管理费用-工会经费", "credit": "应付职工薪酬-工会经费", "description": "计提工会经费", "warning": "工会经费按工资总额2%计提，40%上缴上级工会。"},
    {"keywords": ["外购礼品", "礼品发员工", "买礼品", "节日礼品", "外购福利", "购买礼品"], "debit": "应付职工薪酬-职工福利费", "credit": "银行存款", "description": "外购商品发放员工福利", "warning": "外购商品发福利进项税额不得抵扣（需转出）。"},
    {"keywords": ["备用金", "借支", "员工借款", "借出差费", "预支差旅费"], "debit": "其他应收款-备用金", "credit": "银行存款", "description": "员工借支备用金", "warning": "备用金实行定额管理制度，报销时凭发票冲销其他应收款。"},

    # ── 税费 ──
    {"keywords": ["未交增值税", "转出未交增值税", "结转增值税", "增值税结转", "月末增值税"], "debit": "应交税费-应交增值税(转出未交增值税)", "credit": "应交税费-未交增值税", "description": "月末结转未交增值税", "warning": "月末需将应交增值税贷方余额转入未交增值税明细科目。"},
    {"keywords": ["管理不善", "非正常损失", "毁损进项", "损失转出", "原材料毁损", "存货毁损"], "debit": "营业外支出", "credit": "应交税费-应交增值税(进项税额转出)", "description": "非正常损失进项税额转出", "warning": "非正常损失的进项税额不得抵扣。"},
    {"keywords": ["缴纳印花税", "印花税", "交印花税", "申报印花税"], "debit": "税金及附加", "credit": "银行存款", "description": "缴纳印花税", "warning": "印花税直接计入税金及附加，无需通过应交税费科目计提。"},
    {"keywords": ["扣缴个税", "缴纳个税", "交个人所得税", "个税申报", "代扣代缴个税", "缴个税"], "debit": "应交税费-应交个人所得税", "credit": "银行存款", "description": "代扣代缴员工个人所得税", "warning": "个税由企业代扣代缴，申报截止日为次月15日。"},
    {"keywords": ["房产税", "土地使用税", "计提房产税", "房产税计提"], "debit": "税金及附加", "credit": "应交税费-应交房产税", "description": "计提房产税和土地使用税", "warning": "房产税按房产原值70%的1.2%或租金收入的12%计算。"},

    # ── 固定资产扩展 ──
    {"keywords": ["固定资产盘亏", "设备盘亏", "机器盘亏", "资产盘亏"], "debit": "营业外支出-盘亏损失", "credit": "固定资产-机器设备", "description": "固定资产盘亏", "warning": "固定资产盘亏需先转入待处理财产损溢，批准后计入营业外支出。"},
    {"keywords": ["计提减值", "减值准备", "固定资产减值", "资产减值", "设备减值"], "debit": "资产减值损失", "credit": "固定资产减值准备", "description": "计提固定资产减值准备", "warning": "固定资产减值损失一经确认不得转回。"},
    {"keywords": ["出售 设备", "出售 固定资产", "变卖 设备", "卖掉 设备", "卖旧 设备", "卖 机器", "出售 机器"], "debit": "银行存款", "credit": "固定资产清理", "description": "出售旧设备取得价款", "warning": "出售固定资产需先转入固定资产清理科目。"},
    {"keywords": ["装修", "装修费", "办公装修", "店铺装修", "场地装修", "装修支出", "租入装修"], "debit": "长期待摊费用-装修费", "credit": "银行存款", "description": "经营租入固定资产改良支出", "warning": "经营租入固定资产改良支出计入长期待摊费用，在剩余租赁期内摊销。"},

    # ── 无形资产 ──
    {"keywords": ["购入专利", "购买专利", "专利权", "购买软件著作权", "购入商标", "购买商标"], "debit": "无形资产-专利权", "credit": "银行存款", "description": "购入无形资产（专利权等）", "warning": "外购无形资产按实际成本入账，包括购买价款和相关税费。"},
    {"keywords": ["无形资产摊销", "摊销无形资产", "专利摊销", "计提摊销"], "debit": "管理费用-无形资产摊销", "credit": "累计摊销", "description": "计提无形资产摊销", "warning": "使用寿命有限的无形资产需按期摊销。"},
    {"keywords": ["研发支出", "研发费用", "研究开发", "研发投入", "研发活动"], "debit": "管理费用-研发费用", "credit": "银行存款", "description": "研发支出费用化处理", "warning": "研究阶段支出及不满足资本化条件的开发支出全部计入当期损益。"},

    # ── 借款与利息 ──
    {"keywords": ["计提 利息", "计提 借款 利息", "利息 计提", "预提 利息", "短期借款 利息 计提", "借款利息 计提"], "debit": "财务费用-利息支出", "credit": "应付利息", "description": "计提短期借款利息", "warning": "短期借款利息按期计提，实际支付时冲减应付利息。"},
    {"keywords": ["支付 利息", "付 利息", "还 利息", "支付 借款 利息", "付 银行 利息"], "debit": "应付利息", "credit": "银行存款", "description": "支付已计提的借款利息", "warning": "利息支出需取得银行利息回单作为原始凭证。"},
    {"keywords": ["资本化 利息", "在建工程 利息", "工程 利息", "利息 资本化", "建设期 利息", "符合 资本化", "符合 资本化 条件", "长期借款 资本化", "长期借款 利息 资本化"], "debit": "在建工程", "credit": "应付利息", "description": "计提符合资本化条件的借款利息", "warning": "购建固定资产的借款利息在资产达到预定可使用状态前应资本化。"},
    {"keywords": ["归还 借款", "还 贷款", "归还 本金", "偿还 借款", "归还 银行 贷款", "还 短期 借款"], "debit": "短期借款", "credit": "银行存款", "description": "归还短期借款本金", "warning": "归还借款本金不涉及损益，仅影响资产负债项目。"},
    {"keywords": ["银行承兑汇票", "开承兑", "承兑汇票", "签发汇票", "开出汇票"], "debit": "原材料", "credit": "应付票据", "description": "用银行承兑汇票支付采购款", "warning": "银行承兑汇票需缴纳一定比例的保证金，到期无条件支付。"},

    # ── 收入与成本 ──
    {"keywords": ["结转成本", "结转主营业务成本", "结转销售成本", "成本结转", "结转已销"], "debit": "主营业务成本", "credit": "库存商品", "description": "结转已销商品主营业务成本", "warning": "主营业务成本需与主营业务收入配比。"},
    {"keywords": ["废料", "出售废料", "卖废料", "废品收入", "废料收入", "边角料"], "debit": "银行存款", "credit": "其他业务收入", "description": "出售生产废料取得收入", "warning": "废料出售收入属于其他业务收入，需计提增值税销项税额。"},
    {"keywords": ["收到押金", "收押金", "收取押金", "包装物押金", "保证金收入"], "debit": "银行存款", "credit": "其他应付款-押金", "description": "收到客户押金或保证金", "warning": "收取的押金属于负债，退还时冲减；逾期不退转为营业外收入。"},
    {"keywords": ["退还押金", "退押金", "返还押金", "退回保证金"], "debit": "其他应付款-押金", "credit": "银行存款", "description": "退还客户押金", "warning": "退还押金时确认押金收据已收回。"},
    {"keywords": ["没收押金", "押金不退", "逾期未退", "押金转收入"], "debit": "其他应付款-押金", "credit": "营业外收入", "description": "逾期未退押金转为营业外收入", "warning": "逾期未退还的押金需确认收入并计提增值税销项税额。"},

    # ── 所有者权益 ──
    {"keywords": ["提取盈余公积", "提取法定盈余公积", "计提盈余公积", "盈余公积计提"], "debit": "利润分配-提取法定盈余公积", "credit": "盈余公积-法定盈余公积", "description": "提取法定盈余公积", "warning": "法定盈余公积累计额达到注册资本50%后可不再提取。"},
    {"keywords": ["宣告分红", "宣告股利", "分配股利", "宣告分红", "股东大会分红", "宣告分配"], "debit": "利润分配-应付现金股利", "credit": "应付股利", "description": "宣告分配现金股利", "warning": "股利宣告日确认负债，实际支付时冲减应付股利。"},
    {"keywords": ["支付 股利", "付 股利", "发 股利", "分红 款", "支付 分红", "股东 分红", "支付 现金 股利"], "debit": "应付股利", "credit": "银行存款", "description": "实际支付股东现金股利", "warning": "支付股利需代扣代缴个人所得税（股息红利20%）。"},
    {"keywords": ["资本公积转增", "转增资本", "资本公积转资本", "转增注册资本"], "debit": "资本公积-资本溢价", "credit": "实收资本", "description": "资本公积转增注册资本", "warning": "资本公积转增资本需办理工商变更登记。"},
    {"keywords": ["政府补助", "政府补贴", "财政补贴", "产业扶持", "扶持资金", "补助款"], "debit": "银行存款", "credit": "营业外收入", "description": "收到政府补助款", "warning": "与收益相关的政府补助计入当期损益；与资产相关的确认为递延收益分期转入。"},

    # ── 金融资产 ──
    {"keywords": ["公允价值上升", "公允价值上涨", "公允价值增加", "股价上涨", "金融资产升值"], "debit": "交易性金融资产-公允价值变动", "credit": "公允价值变动损益", "description": "交易性金融资产公允价值上升", "warning": "公允价值变动损益属于未实现损益，不影响当期应税所得。"},
    {"keywords": ["出售理财", "卖掉理财", "赎回理财", "卖出交易性金融资产", "出售金融资产"], "debit": "银行存款", "credit": "交易性金融资产", "description": "出售交易性金融资产取得价款", "warning": "出售时同时将持有期间公允价值变动损益结转至投资收益。"},
    {"keywords": ["收到汇票", "收到承兑汇票", "收承兑", "客户给汇票", "收银行承兑"], "debit": "应收票据", "credit": "应收账款", "description": "收到客户银行承兑汇票", "warning": "应收票据按面值入账，贴现或到期收款时冲减。"},
    {"keywords": ["票据贴现", "汇票贴现", "承兑贴现", "贴现", "贴现银行"], "debit": "银行存款", "credit": "短期借款-票据贴现", "description": "银行承兑汇票贴现", "warning": "附追索权的票据贴现视为质押借款，贴现息计入财务费用。"},

    # ── 期末结转 ──
    {"keywords": ["结转收入", "结转主营业务收入", "收入结转本年利润", "结转损益收入"], "debit": "主营业务收入", "credit": "本年利润", "description": "月末结转收入类科目至本年利润", "warning": "月末将所有收入类科目余额结转至本年利润贷方。"},
    {"keywords": ["结转成本费用", "结转主营业务成本", "成本结转本年利润", "结转费用"], "debit": "本年利润", "credit": "主营业务成本", "description": "月末结转成本费用至本年利润", "warning": "月末将所有成本费用类科目余额结转至本年利润借方。"},
    {"keywords": ["结转管理费用", "管理费用结转", "结转期间费用"], "debit": "本年利润", "credit": "管理费用", "description": "月末结转管理费用至本年利润", "warning": "管理费用为期间费用，月末全额转入本年利润，无余额。"},
    {"keywords": ["结转本年利润", "年末结转", "本年利润结转", "转入未分配利润", "利润结转"], "debit": "本年利润", "credit": "利润分配-未分配利润", "description": "年末结转本年利润至未分配利润", "warning": "年末本年利润科目无余额，全部转入利润分配。"},
    {"keywords": ["摊销装修费", "装修费摊销", "长期待摊摊销", "摊销长期待摊"], "debit": "管理费用-装修费摊销", "credit": "长期待摊费用-装修费", "description": "摊销经营租入固定资产改良支出", "warning": "长期待摊费用在受益期内按月摊销，摊销期不短于3年。"},
    {"keywords": ["支付承兑", "兑付承兑", "承兑到期", "承兑付款", "汇票到期付款"], "debit": "应付票据", "credit": "银行存款", "description": "支付到期银行承兑汇票", "warning": "应付票据到期需确保银行存款余额充足，避免逾期产生罚息。"},
]


import signal


# ─── 无意义助词（清洗用） ──────────────────────────────────
STOP_WORDS = ["对", "进行", "了", "的", "把", "被", "让", "给", "在", "从", "向", "将", "以", "与", "和", "或", "及", "并", "而"]


def _clean_text(text: str) -> str:
    """剥离无意义助词，只保留核心业务关键词"""
    for w in STOP_WORDS:
        text = text.replace(w, "")
    return text


def _match_quick(text: str):
    """
    快速匹配：遍历规则库，按关键词长度降序匹配（最长关键词优先），
    确保"计提工资"不会被"工资"先抢走。
    支持两种关键词格式：
    - 普通字符串：kw in text（子串匹配）
    - 包含空格的多词组合：拆分为多个词，要求 ALL 出现在 text 中
    对清洗后的文本和原始文本都做匹配，提高长句子的命中率。
    """
    amount = _extract_amount(text)

    # 收集所有命中的 (关键词长度, 规则, 关键词)
    hits = []

    for rule in RULE_DATABASE:
        for kw in rule["keywords"]:
            # 支持多词组合（用空格分隔，要求全部出现）
            if " " in kw:
                parts = [p.strip() for p in kw.split() if p.strip()]
                if len(parts) > 1 and all(p in text for p in parts):
                    hits.append((len(kw), rule, kw))
            else:
                if kw in text:
                    hits.append((len(kw), rule, kw))

    if not hits:
        return None

    # 按关键词长度降序排列（最长匹配优先）
    hits.sort(key=lambda x: x[0], reverse=True)

    best_rule = hits[0][1]
    result = {
        "debit_account": best_rule["debit"],
        "credit_account": best_rule["credit"],
        "debit_amount": amount,
        "credit_amount": amount,
        "description": best_rule["description"],
        "warning": best_rule["warning"],
        "source": "rule",
    }
    # 传递多分录标记（自产产品发福利等特殊业务）
    if best_rule.get("_multi_entry"):
        result["_multi_entry"] = True
        result["_mock_id"] = best_rule.get("_mock_id")
    return result


class TimeoutError(Exception):
    """自定义超时异常"""
    pass


def _timeout_handler(signum, frame):
    raise TimeoutError("匹配超时")


# ─── 中文 + 英文标点符号集合 ──────────────────────────────
import string
PUNCTUATION = set(string.punctuation) | set("，。、；：？！""''（）【】《》—…·～　")


def _strip_punctuation(text: str) -> str:
    """去掉所有中英文标点符号，返回纯文字"""
    return "".join(ch for ch in text if ch not in PUNCTUATION)


def _scenario_to_result(scenario: dict):
    """
    将 mock_data 场景数据转换为匹配结果格式。
    支持单分录和多分录（entries）场景。
    """
    amount = scenario.get("debit_amount", 0)
    result = {
        "debit_account": scenario["debit_account"],
        "credit_account": scenario["credit_account"],
        "debit_amount": amount,
        "credit_amount": scenario.get("credit_amount", amount),
        "description": scenario["description"],
        "warning": scenario.get("warning"),
        "source": "scenario",
    }
    if "entries" in scenario:
        result["_multi_entry"] = True
        result["_mock_id"] = scenario["id"]
        result["_entries"] = scenario["entries"]
    return result


def match_by_rule(user_input: str):
    """
    精确规则匹配（带标点过滤 + 分词清洗 + mock_data 回退 + 超时保护）：
    1. 先去掉所有中英文标点符号
    2. 剥离无意义助词，提取核心关键词
    3. 对原始文本和清洗后文本分别做快速匹配（RULE_DATABASE）
    4. 规则库未命中 → 回退到 mock_data.find_scenario（场景关键词匹配）
    5. 超过 3 秒自动放弃，返回 None
    """
    import re

    # ── 第 0 步：去掉所有标点符号 ──
    raw = user_input
    user_input = _strip_punctuation(user_input)

    # ── 设置 3 秒超时 ──
    try:
        signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(3)
    except Exception:
        pass  # Windows 不支持 SIGALRM，忽略

    try:
        # 0.5. 标点过滤后只剩无效内容 → 返回特殊标记
        cleaned = _clean_text(user_input).strip()
        if len(cleaned) <= 2:
            signal.alarm(0)
            return {"_error": "empty_input"}

        # 1. 先对去标点后的文本匹配 RULE_DATABASE
        result = _match_quick(user_input)
        if result is not None:
            signal.alarm(0)
            return result

        # 2. 清洗后再次匹配 RULE_DATABASE（处理长句子）
        if cleaned != user_input:
            result = _match_quick(cleaned)
            if result is not None:
                signal.alarm(0)
                return result

        # 3. 如果清洗后文本较长，尝试按常见分隔符拆分后逐段匹配
        if len(cleaned) > 10:
            for sep in ["，", ",", "。", "；", ";", "、"]:
                parts = [p.strip() for p in cleaned.split(sep) if p.strip()]
                if len(parts) > 1:
                    for part in parts:
                        result = _match_quick(part)
                        if result is not None:
                            signal.alarm(0)
                            return result
                    break  # 只尝试第一种有效分隔符

        # 4. RULE_DATABASE 未命中 → 回退到 mock_data.find_scenario
        from mock_data import find_scenario
        scenario = find_scenario(user_input)
        if scenario is None and cleaned != user_input:
            scenario = find_scenario(cleaned)
        if scenario is not None:
            signal.alarm(0)
            return _scenario_to_result(scenario)

        signal.alarm(0)
        return None

    except TimeoutError:
        signal.alarm(0)
        return None  # 超时返回 None，由 app.py 展示友好提示
    except Exception:
        signal.alarm(0)
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
