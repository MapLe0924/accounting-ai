"""
智能会计凭证推荐系统 —— Streamlit 单页面 Web 应用
运行方式：streamlit run app.py
"""

import streamlit as st
from mock_data import MOCK_SCENARIOS, find_scenario

# ─── 页面配置 ───────────────────────────────────────────────
st.set_page_config(
    page_title="智能会计凭证推荐系统",
    page_icon="📒",
    layout="centered",
)

# ─── 自定义 CSS（干净清爽风格） ─────────────────────────────
st.markdown(
    """
<style>
    .main { padding: 1rem 2rem; }
    .stApp { background-color: #f8f9fa; }
    h1 { color: #1a1a2e; font-weight: 600; }
    .subtitle { color: #6c757d; font-size: 0.95rem; margin-bottom: 1.5rem; }
    .voucher-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin: 1rem 0;
    }
    .voucher-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1a1a2e;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e9ecef;
    }
    .debit-row { color: #d6336c; }
    .credit-row { color: #0d6efd; }
    .amount-cell { font-weight: 600; font-family: 'Courier New', monospace; }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffc107;
        border-left: 4px solid #ffc107;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
    }
    .warning-box .icon { font-size: 1.3rem; margin-right: 0.5rem; }
    .footer { text-align: center; color: #adb5bd; font-size: 0.8rem; margin-top: 3rem; }
    .example-btn {
        background: white;
        border: 1px solid #dee2e6;
        border-radius: 20px;
        padding: 0.3rem 0.8rem;
        font-size: 0.8rem;
        color: #495057;
        cursor: pointer;
        margin: 0.2rem;
        display: inline-block;
    }
    .example-btn:hover { background: #e9ecef; }
</style>
""",
    unsafe_allow_html=True,
)

# ─── 页面标题 ───────────────────────────────────────────────
st.markdown("<h1>📒 智能会计凭证推荐系统</h1>", unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">输入一段业务描述，AI 自动推荐会计科目分录</p>',
    unsafe_allow_html=True,
)

# ─── 示例场景快速入口 ──────────────────────────────────────
st.markdown("**💡 试试输入这些场景：**")
cols = st.columns(5)
examples = [
    "昨天请客户吃饭花了800元",
    "购买办公用品花了500元",
    "员工出差报销差旅费1200元",
    "支付办公室房租6000元",
    "购买一台电脑8000元",
]
for i, example in enumerate(examples):
    with cols[i]:
        if st.button(example, key=f"example_{i}", use_container_width=True):
            st.session_state["user_input"] = example

# ─── 输入区域 ───────────────────────────────────────────────
user_input = st.text_area(
    "📝 请输入业务描述",
    value=st.session_state.get("user_input", ""),
    placeholder="例如：昨天请客户吃饭花了800元",
    height=100,
    label_visibility="collapsed",
)

# ─── 推荐按钮 ───────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    recommend_clicked = st.button(
        "✨ 智能推荐凭证",
        type="primary",
        use_container_width=True,
    )

# ─── 处理推荐逻辑 ───────────────────────────────────────────
if recommend_clicked:
    if not user_input.strip():
        st.warning("⚠️ 请先输入业务描述再点击推荐！")
    else:
        result = find_scenario(user_input.strip())

        if result is None:
            st.error(
                "😅 抱歉，暂未匹配到合适的业务场景。"
                "请尝试输入更常见的业务描述，如「请客吃饭」「买办公用品」「出差」等。"
            )
        else:
            # ── 凭证推荐结果卡片 ──
            st.markdown(
                '<div class="voucher-card">'
                '<div class="voucher-title">📋 推荐会计分录</div>',
                unsafe_allow_html=True,
            )

            # 表格展示
            col_left, col_right = st.columns([1, 1])
            with col_left:
                st.markdown("**借方**")
                st.markdown(
                    f'<p class="debit-row" style="font-size:1.1rem;">'
                    f'📌 {result["debit_account"]}</p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<p class="amount-cell debit-row" style="font-size:1.3rem;">'
                    f'¥ {result["debit_amount"]:,.2f}</p>',
                    unsafe_allow_html=True,
                )

            with col_right:
                st.markdown("**贷方**")
                st.markdown(
                    f'<p class="credit-row" style="font-size:1.1rem;">'
                    f'📌 {result["credit_account"]}</p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<p class="amount-cell credit-row" style="font-size:1.3rem;">'
                    f'¥ {result["credit_amount"]:,.2f}</p>',
                    unsafe_allow_html=True,
                )

            # 分隔线
            st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)

            # 完整分录表格
            st.markdown("**📊 完整分录**")
            voucher_data = [
                {
                    "方向": "借",
                    "科目": result["debit_account"],
                    "金额": f'¥ {result["debit_amount"]:,.2f}',
                },
                {
                    "方向": "贷",
                    "科目": result["credit_account"],
                    "金额": f'¥ {result["credit_amount"]:,.2f}',
                },
            ]
            st.dataframe(
                voucher_data,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "方向": st.column_config.TextColumn("方向", width="small"),
                    "科目": st.column_config.TextColumn("会计科目", width="large"),
                    "金额": st.column_config.TextColumn("金额", width="medium"),
                },
            )

            st.markdown("</div>", unsafe_allow_html=True)

            # ── 专家校验区域 ──
            st.markdown("---")
            st.markdown("### 🔍 专家校验")

            # 通用校验规则
            warnings = []

            # 规则1：业务招待费超过2000元
            if "业务招待" in result["debit_account"] and result["debit_amount"] > 2000:
                warnings.append(
                    "⚠️ 业务招待费金额超过2000元，请确认是否真实合理，"
                    "企业所得税汇算清缴时需按60%限额扣除（最高不超过当年销售收入的5‰）。"
                )

            # 规则2：单笔金额超过2000元且含"固定资产"关键词
            if result["debit_amount"] > 2000 and "固定资产" not in result["debit_account"]:
                if "电脑" in str(user_input) or "设备" in str(user_input) or "机器" in str(user_input):
                    warnings.append(
                        "⚠️ 金额超过2000元且属于设备类支出，建议确认是否应计入「固定资产」并按月计提折旧！"
                    )

            # 规则3：场景自带的校验提示
            if result["warning"]:
                warnings.append(f"⚠️ {result['warning']}")

            if warnings:
                for w in warnings:
                    st.markdown(
                        f'<div class="warning-box">'
                        f'<span class="icon">⚠️</span> {w}'
                        f"</div>",
                        unsafe_allow_html=True,
                    )
            else:
                st.success("✅ 经初步校验，该笔业务分录合理，未发现明显税会差异。")

            # ── 业务场景参考 ──
            with st.expander("📖 查看所有支持的业务场景（共10个）"):
                for scenario in MOCK_SCENARIOS:
                    st.markdown(
                        f"**{scenario['id']}. {scenario['description']}**  \n"
                        f"借：{scenario['debit_account']}  "
                        f"¥{scenario['debit_amount']:,.2f}  |  "
                        f"贷：{scenario['credit_account']}  "
                        f"¥{scenario['credit_amount']:,.2f}"
                    )
                    if scenario["warning"]:
                        st.caption(f"💡 校验提示：{scenario['warning']}")
                    st.markdown("---")

# ─── 页脚 ───────────────────────────────────────────────────
st.markdown(
    '<div class="footer">'
    "📒 智能会计凭证推荐系统 · 仅供学习参考，实际做账请以会计准则为准"
    "</div>",
    unsafe_allow_html=True,
)
