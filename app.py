"""
智能会计凭证推荐系统 —— Streamlit 单页面 Web 应用
运行方式：streamlit run app.py
"""

import streamlit as st
import json
import urllib.request
import urllib.error
from mock_data import MOCK_SCENARIOS
from rule_engine import match_by_rule, RULE_DATABASE
from accounting_common_sense import (
    check_capitalization,
    render_capitalization_ui,
)

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
    .manual-entry-section {
        background: #f0f4f8;
        border: 1px solid #dde7f0;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
    }
    .manual-entry-banner {
        font-size: 1.05rem;
        color: #1a1a2e;
        margin-bottom: 0.3rem;
    }
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
    '<p class="subtitle">输入业务描述，系统自动匹配 130+ 会计场景，未命中则调用 AI 智能推荐</p>',
    unsafe_allow_html=True,
)

# ─── 侧边栏：历史记录 + 场景搜索 ──────────────────────────
with st.sidebar:
    st.markdown("### 🕐 最近查询")
    if "query_history" not in st.session_state:
        st.session_state["query_history"] = []

    if st.session_state["query_history"]:
        for h in reversed(st.session_state["query_history"][-8:]):
            if st.button(f"📌 {h[:30]}...", key=f"hist_{hash(h)}", width="stretch"):
                st.session_state["user_input"] = h
                st.session_state["recommend_triggered"] = True
                st.session_state["recommend_text"] = h
                st.rerun()
        if st.button("🗑️ 清空历史", width="stretch"):
            st.session_state["query_history"] = []
            st.rerun()
    else:
        st.caption("暂无查询记录")

    st.markdown("---")
    st.markdown("### 🔍 场景搜索")
    search_kw = st.text_input("搜索关键词", placeholder="如：折旧、理财、报废...", label_visibility="collapsed")
    if search_kw:
        from mock_data import MOCK_SCENARIOS
        found = [s for s in MOCK_SCENARIOS if search_kw in s["description"]]
        if found:
            for s in found[:6]:
                if st.button(f"📄 {s['description'][:28]}", key=f"search_{s['id']}", width="stretch"):
                    st.session_state["user_input"] = s["description"]
                    st.session_state["recommend_triggered"] = True
                    st.session_state["recommend_text"] = s["description"]
                    st.rerun()
        else:
            st.caption("未找到匹配场景")

# ─── 示例场景快速入口 ──────────────────────────────────────
st.markdown("**💡 高频场景一键体验：**")
cols = st.columns(3)
examples = [
    "购买办公用品花了500元",
    "支付办公室房租6000元",
    "计提本月员工工资总额2万元",
]
for i, example in enumerate(examples):
    with cols[i]:
        if st.button(example, key=f"example_{i}", width="stretch"):
            st.session_state["user_input"] = example

cols2 = st.columns(3)
examples2 = [
    "公司报废一台设备，原值50万已提折旧48万，清理费2000残料收入3000",
    "股东以一台旧的机器设备入股，作价100万",
    "上月暂估入库5万，本月收到发票实际4.8万税额6240",
]
for i, example in enumerate(examples2):
    with cols2[i]:
        if st.button(example, key=f"example2_{i}", width="stretch"):
            st.session_state["user_input"] = example

# ─── 输入区域 ───────────────────────────────────────────────
user_input = st.text_area(
    "📝 请输入业务描述",
    value=st.session_state.get("user_input", ""),
    placeholder="请输入业务描述（例如：购买办公桌椅2000元；支付第三季度房租）。如果您的描述较复杂，请在描述中包含「进项税」「固定资产」「待摊」等财税关键词，系统将智能匹配科目。",
    height=100,
    label_visibility="collapsed",
)

# ─── 推荐按钮 ───────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    recommend_clicked = st.button(
        "✨ 智能推荐凭证",
        type="primary",
        width="stretch",
    )

# ─── AI 调用函数（大模型兜底匹配） ──────────────────────────

def call_ai_for_recommendation(user_text: str):
    """
    当规则库匹配不到时，调用大模型 API 进行智能模糊匹配。
    优先级：DeepSeek（免费API）→ Ollama（本地）→ OpenAI 兼容接口。
    """
    system_prompt = (
        "你是一位经验丰富的会计专家。请根据用户输入的业务描述，"
        "推荐最合适的会计分录（借方科目、贷方科目、金额）。"
        "请严格按照以下 JSON 格式返回，不要包含其他文字：\n"
        '{"debit_account":"借方科目","credit_account":"贷方科目",'
        '"amount":数字金额,"description":"业务说明","warning":"校验提示或无"}'
    )

    def _parse_response(content):
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        result = json.loads(content)
        return {
            "debit_account": result["debit_account"],
            "credit_account": result["credit_account"],
            "debit_amount": float(result["amount"]),
            "credit_amount": float(result["amount"]),
            "description": result.get("description", ""),
            "warning": result.get("warning"),
            "source": "ai",
        }

    def _call_api(url, payload, headers):
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                      headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))

    # ── 1. DeepSeek API（免费额度，无需本地部署）──
    try:
        payload = {"model": "deepseek-chat", "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"业务描述：{user_text}"},
        ], "temperature": 0.1, "stream": False}
        body = _call_api("https://api.deepseek.com/v1/chat/completions", payload,
                         {"Content-Type": "application/json",
                          "Authorization": f"Bearer {st.secrets.get('DEEPSEEK_API_KEY', '')}"})
        return _parse_response(body["choices"][0]["message"]["content"].strip())
    except Exception:
        pass

    # ── 2. 本地 Ollama ──
    try:
        body = _call_api("http://localhost:11434/api/chat",
                         {"model": "qwen2.5:7b", "messages": [
                             {"role": "system", "content": system_prompt},
                             {"role": "user", "content": f"业务描述：{user_text}"},
                         ], "temperature": 0.1, "stream": False},
                         {"Content-Type": "application/json"})
        return _parse_response(body["message"]["content"].strip())
    except Exception:
        pass

    # ── 3. OpenAI 兼容接口 ──
    try:
        api_key = st.secrets.get("OPENAI_API_KEY", "")
        if not api_key:
            return None
        body = _call_api("https://api.openai.com/v1/chat/completions",
                         {"model": "gpt-3.5-turbo", "messages": [
                             {"role": "system", "content": system_prompt},
                             {"role": "user", "content": f"业务描述：{user_text}"},
                         ], "temperature": 0.1},
                         {"Content-Type": "application/json",
                          "Authorization": f"Bearer {api_key}"})
        return _parse_response(body["choices"][0]["message"]["content"].strip())
    except Exception:
        return None


# ─── 展示推荐结果（通用函数） ──────────────────────────────

def display_voucher_result(result, user_input: str, verdict_result: dict = None):
    """
    展示凭证推荐结果卡片、表格、校验区域。
    支持单条分录（dict）和多条分录（dict with _multi_entry=True）。
    """

    # ── 判断是否为多分录 ──
    is_multi = isinstance(result, dict) and result.get("_multi_entry")
    is_ai = not is_multi and result.get("source") == "ai"

    # ── 根据预检结果动态设置置信度 ──
    if is_multi:
        confidence_badge = (
            '<span style="'
            "display:inline-block; background:#d4edda; color:#155724; "
            "border:1px solid #c3e6cb; border-radius:20px; "
            "padding:0.3rem 1rem; font-size:0.85rem; font-weight:600; "
            "margin-bottom:0.8rem;"
            '">✅ 规则库精准匹配（置信度 95%）</span>'
        )
    elif verdict_result:
        v = verdict_result["verdict"]
        c = verdict_result["confidence"]
        if not is_ai and ((v == "expense" and c == "high") or (v == "capital" and c == "high")):
            confidence_badge = (
                '<span style="'
                "display:inline-block; background:#d4edda; color:#155724; "
                "border:1px solid #c3e6cb; border-radius:20px; "
                "padding:0.3rem 1rem; font-size:0.85rem; font-weight:600; "
                "margin-bottom:0.8rem;"
                '">✅ 规则库精准匹配（置信度 95%）</span>'
            )
        elif not is_ai:
            confidence_badge = (
                '<span style="'
                "display:inline-block; background:#fff3cd; color:#856404; "
                "border:1px solid #ffc107; border-radius:20px; "
                "padding:0.3rem 1rem; font-size:0.85rem; font-weight:600; "
                "margin-bottom:0.8rem;"
                '">⚠️ 规则库匹配（置信度 60%，请人工复核）</span>'
            )
        else:
            confidence_badge = (
                '<span style="'
                "display:inline-block; background:#fff3cd; color:#856404; "
                "border:1px solid #ffc107; border-radius:20px; "
                "padding:0.3rem 1rem; font-size:0.85rem; font-weight:600; "
                "margin-bottom:0.8rem;"
                '">⚠️ AI 智能推荐（置信度 70%，请人工复核）</span>'
            )
    else:
        if not is_ai:
            confidence_badge = (
                '<span style="'
                "display:inline-block; background:#d4edda; color:#155724; "
                "border:1px solid #c3e6cb; border-radius:20px; "
                "padding:0.3rem 1rem; font-size:0.85rem; font-weight:600; "
                "margin-bottom:0.8rem;"
                '">✅ 规则库精准匹配（置信度 95%）</span>'
            )
        else:
            confidence_badge = (
                '<span style="'
                "display:inline-block; background:#fff3cd; color:#856404; "
                "border:1px solid #ffc107; border-radius:20px; "
                "padding:0.3rem 1rem; font-size:0.85rem; font-weight:600; "
                "margin-bottom:0.8rem;"
                '">⚠️ AI 智能推荐（置信度 70%，请人工复核）</span>'
            )

    # ── 凭证推荐结果卡片 ──
    st.markdown(
        '<div class="voucher-card">'
        f'{confidence_badge}'
        '<div class="voucher-title">📋 推荐会计分录</div>',
        unsafe_allow_html=True,
    )

    if is_ai:
        st.warning("🤖 此为 AI 推荐结果，请人工复核确认后再做账！")

    # ── 多分录展示（自产产品发福利等） ──
    if is_multi:
        entries = result["_entries"]
        # 逐条展示每笔分录
        for idx, entry in enumerate(entries, 1):
            st.markdown(f"**第 {idx} 笔分录：{entry['description']}**")
            col_left, col_right = st.columns([1, 1])
            with col_left:
                st.markdown("**借方**")
                amt = entry.get("debit_amount", 0)
                if amt and amt > 0:
                    st.markdown(
                        f'<p class="debit-row" style="font-size:1.1rem;">'
                        f'📌 {entry["debit_account"]}</p>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<p class="amount-cell debit-row" style="font-size:1.3rem;">'
                        f'¥ {amt:,.2f}</p>',
                        unsafe_allow_html=True,
                    )
            with col_right:
                st.markdown("**贷方**")
                amt = entry.get("credit_amount", 0)
                if amt and amt > 0:
                    st.markdown(
                        f'<p class="credit-row" style="font-size:1.1rem;">'
                        f'📌 {entry["credit_account"]}</p>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<p class="amount-cell credit-row" style="font-size:1.3rem;">'
                        f'¥ {amt:,.2f}</p>',
                        unsafe_allow_html=True,
                    )
            if entry.get("tax_note"):
                st.caption(f"💡 {entry['tax_note']}")
            if idx < len(entries):
                st.markdown("<hr style='margin: 0.5rem 0; opacity:0.3;'>", unsafe_allow_html=True)

        # 多分录的完整分录汇总表
        st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)
        st.markdown("**📊 完整分录汇总**")
        voucher_data = []
        for entry in entries:
            d_amt = entry.get("debit_amount", 0)
            c_amt = entry.get("credit_amount", 0)
            if d_amt and d_amt > 0:
                voucher_data.append({
                    "方向": "借",
                    "科目": entry["debit_account"],
                    "金额": f'¥ {d_amt:,.2f}',
                    "说明": entry["description"],
                })
            if c_amt and c_amt > 0:
                voucher_data.append({
                    "方向": "贷",
                    "科目": entry["credit_account"],
                    "金额": f'¥ {c_amt:,.2f}',
                    "说明": entry["description"],
                })
        st.dataframe(
            voucher_data,
            width="stretch",
            hide_index=True,
            column_config={
                "方向": st.column_config.TextColumn("方向", width="small"),
                "科目": st.column_config.TextColumn("会计科目", width="large"),
                "金额": st.column_config.TextColumn("金额", width="medium"),
                "说明": st.column_config.TextColumn("业务说明", width="large"),
            },
        )

    else:
        # ── 单条分录展示（原有逻辑） ──
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
            width="stretch",
            hide_index=True,
            column_config={
                "方向": st.column_config.TextColumn("方向", width="small"),
                "科目": st.column_config.TextColumn("会计科目", width="large"),
                "金额": st.column_config.TextColumn("金额", width="medium"),
            },
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ── 智能审计区域 ──
    st.markdown("---")
    st.markdown("### 🔍 智能审计")

    from audit_engine import audit_voucher

    audit_results = []
    if is_multi:
        for e in result.get("_entries", []):
            d = e.get("debit_account", "")
            c = e.get("credit_account", "")
            amt = max(e.get("debit_amount", 0), e.get("credit_amount", 0))
            audit_results.append(audit_voucher(d, c, amt, e.get("description", ""), result.get("source", "rule")))
    else:
        audit_results.append(audit_voucher(
            result["debit_account"], result["credit_account"],
            result.get("debit_amount", 0), "", result.get("source", "rule")
        ))

    # 汇总风险等级
    all_risk = [a["risk_level"] for a in audit_results]
    if "high" in all_risk:
        risk_badge = "🔴 高风险"
        risk_color = "#dc3545"
    elif "medium" in all_risk:
        risk_badge = "🟡 中风险"
        risk_color = "#ffc107"
    elif "low" in all_risk:
        risk_badge = "🟢 低风险"
        risk_color = "#28a745"
    else:
        risk_badge = "✅ 无风险"
        risk_color = "#28a745"

    avg_conf = sum(a["confidence"] for a in audit_results) // len(audit_results)
    st.markdown(f"**风险等级：**<span style='color:{risk_color};font-weight:600;font-size:1.1rem;'>{risk_badge}</span>　|　**置信度：**{avg_conf}%　|　**审计轨迹：**{len(audit_results)}笔分录已校验", unsafe_allow_html=True)

    # 展示审计发现
    all_findings = []
    all_tax = []
    for a in audit_results:
        all_findings.extend(a["findings"])
        all_tax.extend(a["tax_risks"])

    if all_findings:
        st.markdown("#### ⚠️ 合规发现")
        for f in all_findings:
            sev_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(f["severity"], "ℹ️")
            st.markdown(
                f'<div class="warning-box">'
                f'{sev_icon} <strong>{f["type"]}</strong><br>'
                f'{f["message"]}<br>'
                f'<small>💡 {f["suggestion"]}</small>'
                f"</div>",
                unsafe_allow_html=True,
            )

    if all_tax:
        st.markdown("#### 📋 税务风险提示")
        for t in all_tax:
            sev_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(t["severity"], "ℹ️")
            st.markdown(
                f'<div class="warning-box" style="border-left-color:#0dcaf0;">'
                f'{sev_icon} <strong>{t["type"]}</strong><br>'
                f'{t["message"]}'
                f"</div>",
                unsafe_allow_html=True,
            )

    if not all_findings and not all_tax:
        st.success("✅ 智能审计通过，该笔分录科目选择、借贷方向、金额均符合会计准则，未发现税会差异。")

    # ── 导出按钮 ──
    st.markdown("---")
    exp_col1, exp_col2 = st.columns([1, 4])
    with exp_col1:
        voucher_text = _build_voucher_text(result, user_input, is_multi)
        st.download_button(
            "📥 导出分录",
            data=voucher_text,
            file_name="会计分录.txt",
            mime="text/plain",
            width="stretch",
        )


def _build_voucher_text(result, user_input: str, is_multi: bool) -> str:
    """构建可导出的分录文本"""
    lines = ["=" * 50, "  智能会计凭证推荐系统 - 会计分录", "=" * 50, ""]
    lines.append(f"业务描述：{user_input}")
    lines.append("")
    if is_multi:
        for i, e in enumerate(result.get("_entries", []), 1):
            lines.append(f"第{i}笔：{e['description']}")
            if e.get("debit_amount", 0) > 0:
                lines.append(f"  借：{e['debit_account']}  ¥{e['debit_amount']:,.2f}")
            if e.get("credit_amount", 0) > 0:
                lines.append(f"  贷：{e['credit_account']}  ¥{e['credit_amount']:,.2f}")
            if e.get("tax_note"):
                lines.append(f"  注：{e['tax_note']}")
            lines.append("")
    else:
        lines.append(f"借：{result['debit_account']}  ¥{result['debit_amount']:,.2f}")
        lines.append(f"贷：{result['credit_account']}  ¥{result['credit_amount']:,.2f}")
    if result.get("warning"):
        lines.append(f"\n⚠️ 校验提示：{result['warning']}")
    lines.append(f"\n{'=' * 50}")
    return "\n".join(lines)


# ─── 展示预设场景表格（辅助函数） ──────────────────────────

def _show_scenario_table():
    """展示所有预设业务场景的参考表格"""
    with st.expander("📖 查看所有预设业务场景（共{}个）".format(
        len(RULE_DATABASE) + len(MOCK_SCENARIOS)
    ), expanded=True):
        all_scenarios = []
        seen = set()
        for s in MOCK_SCENARIOS:
            key = (s["debit_account"], s["credit_account"])
            if key not in seen:
                seen.add(key)
                all_scenarios.append({
                    "description": s["description"],
                    "debit": s["debit_account"],
                    "credit": s["credit_account"],
                    "debit_amount": s["debit_amount"],
                    "credit_amount": s["credit_amount"],
                    "warning": s["warning"],
                    "source": "演示数据",
                })
        for r in RULE_DATABASE:
            # 跳过多分录特殊标记规则（如自产产品发福利），避免显示原始标记字符串
            if r.get("_multi_entry"):
                continue
            key = (r["debit"], r["credit"])
            if key not in seen:
                seen.add(key)
                all_scenarios.append({
                    "description": r["description"],
                    "debit": r["debit"],
                    "credit": r["credit"],
                    "debit_amount": None,
                    "credit_amount": None,
                    "warning": r["warning"],
                    "source": "规则库",
                })

        table_data = []
        for i, s in enumerate(all_scenarios, 1):
            amount_str = (
                f"¥{s['debit_amount']:,.2f}" if s["debit_amount"] else "—"
            )
            table_data.append({
                "序号": i,
                "业务描述": s["description"],
                "借方科目": s["debit"],
                "贷方科目": s["credit"],
                "金额": amount_str,
                "校验提示": s["warning"] or "无",
            })

        st.dataframe(
            table_data,
            width="stretch",
            hide_index=True,
            column_config={
                "序号": st.column_config.NumberColumn("序号", width="small"),
                "业务描述": st.column_config.TextColumn("业务描述", width="large"),
                "借方科目": st.column_config.TextColumn("借方科目", width="medium"),
                "贷方科目": st.column_config.TextColumn("贷方科目", width="medium"),
                "金额": st.column_config.TextColumn("金额", width="small"),
                "校验提示": st.column_config.TextColumn("校验提示", width="large"),
            },
        )


# ── 用 session_state 记住用户触发了推荐 ──
if recommend_clicked:
    st.session_state["recommend_triggered"] = True
    st.session_state["recommend_text"] = user_input.strip()
    # 记录到查询历史
    text = user_input.strip()
    if text and text not in st.session_state.get("query_history", []):
        st.session_state["query_history"] = st.session_state.get("query_history", []) + [text]
    # 清除展示标记，让新的推荐可以正常展示
    st.session_state["_displayed_in_this_run"] = False

# ─── 辅助函数：执行匹配并生成凭证结果 ──────────────────────

def _run_matching(text: str, verdict_result: dict):
    """
    执行规则匹配/AI兜底，返回凭证结果。
    返回值可以是：
      - dict（单条分录，含 debit_account/credit_account 等）
      - list[dict]（多条分录，如自产产品发福利）
      - None（匹配失败）
    """
    # ── 第一层：规则库精确匹配（带标点过滤 + 超时保护） ──
    import time as _time
    _t0 = _time.time()
    result = match_by_rule(text)
    _elapsed = _time.time() - _t0

    # 标点过滤后输入为空
    if isinstance(result, dict) and result.get("_error") == "empty_input":
        return {"_error": "empty_input"}

    if result is not None:
        # ── 检查是否是多分录标记（自产产品发福利等特殊业务） ──
        if result.get("_multi_entry"):
            # 优先使用结果中已携带的 _entries（来自 _scenario_to_result）
            if result.get("_entries"):
                return {
                    "_multi_entry": True,
                    "_entries": result["_entries"],
                    "description": result["description"],
                    "warning": result.get("warning"),
                    "source": result.get("source", "rule"),
                }

            # 否则通过 _mock_id 从 MOCK_SCENARIOS 查找
            mock_id = result.get("_mock_id")
            if mock_id is not None:
                from mock_data import MOCK_SCENARIOS
                for scenario in MOCK_SCENARIOS:
                    if scenario.get("id") == mock_id and "entries" in scenario:
                        entries = scenario["entries"]
                        return {
                            "_multi_entry": True,
                            "_entries": entries,
                            "description": result["description"],
                            "warning": result.get("warning"),
                            "source": result.get("source", "rule"),
                        }
            # 多分录标记存在但未找到 entries → 降级为单分录展示
            result["_multi_entry"] = False

        # 如果是模糊匹配结果，用模糊匹配的科目覆盖规则库结果
        if verdict_result.get("verdict") == "fuzzy_match":
            fuzzy_acct = verdict_result.get("fuzzy_account", "")
            if fuzzy_acct:
                result["debit_account"] = fuzzy_acct
                result["credit_account"] = "银行存款/应付账款"
                result["description"] = f"模糊匹配：{fuzzy_acct}（请人工核实）"
                result["confidence"] = "low"
        return result

    if _elapsed >= 3:
        return {"_error": "timeout"}

    # ── 第二层：AI 大模型兜底匹配 ──
    with st.spinner("🤖 规则库未匹配到，正在调用 AI 智能分析..."):
        result = call_ai_for_recommendation(text)

    if result is not None:
        # 如果是模糊匹配结果，用模糊匹配的科目覆盖 AI 结果
        if verdict_result.get("verdict") == "fuzzy_match":
            fuzzy_acct = verdict_result.get("fuzzy_account", "")
            if fuzzy_acct:
                result["debit_account"] = fuzzy_acct
                result["credit_account"] = "银行存款/应付账款"
                result["description"] = f"模糊匹配：{fuzzy_acct}（请人工核实）"
                result["confidence"] = "low"
        return result

    return None


def _display_matched_result(result, text: str, verdict_result: dict,
                            capitalization_confirmed: bool, user_chosen_account: str):
    """展示匹配到的凭证结果，并保存到 session_state。"""
    display_voucher_result(result, text, verdict_result)

    # 展示匹配到的规则说明
    is_multi = isinstance(result, dict) and result.get("_multi_entry")
    if not is_multi:
        st.info(f"📌 匹配规则：{result['description']}")
    else:
        st.info(f"📌 匹配规则：{result['description']}")

    # 如果用户之前确认了科目选择，展示对照
    if capitalization_confirmed and user_chosen_account:
        st.info(f"💡 您已确认选择「{user_chosen_account}」，与推荐结果不一致时请以您的判断为准。")

    # 保存结果到 session_state，防止 rerun 后丢失
    st.session_state["voucher_result"] = {
        "result": result,
        "text": text,
        "verdict_result": verdict_result,
        "capitalization_confirmed": capitalization_confirmed,
        "user_chosen_account": user_chosen_account,
    }


# ─── 处理推荐逻辑 ───────────────────────────────────────────
if st.session_state.get("recommend_triggered", False):
    text = st.session_state["recommend_text"]

    if not text:
        st.warning("⚠️ 请先输入业务描述再点击推荐！")
        st.session_state["recommend_triggered"] = False
    else:
        # ── 第〇层：标点过滤 + 空输入检测（在预检之前） ──
        from rule_engine import _strip_punctuation, _clean_text
        _stripped = _strip_punctuation(text)
        _core = _clean_text(_stripped).strip()
        if len(_core) <= 2:
            st.warning(
                "⚠️ **未识别到核心财税词汇，请补充关键业务词（如采购、维修、工资等）。**"
            )
            _show_scenario_table()
            st.session_state["recommend_triggered"] = False
            st.stop()

        # ── 第〇层：会计常识预检（资本化/费用化判断） ──
        st.markdown("---")
        st.markdown("### 🔶 会计常识预检")

        verdict_result = check_capitalization(text)
        needs_manual = render_capitalization_ui(verdict_result)

        # 如果预检结果是"强制手动干预"且用户尚未确认，阻止自动推荐
        if needs_manual:
            st.info(
                "💡 请在上方选择科目方向并点击【确认选择此科目方向】，"
                "系统将根据您的选择调整推荐结果。"
            )
            # 仍然展示场景表格供参考
            _show_scenario_table()
            # 停止执行，等待用户确认
            st.stop()

        # ── 模糊匹配结果 → 显示黄色提醒框 ──
        if verdict_result.get("verdict") == "fuzzy_match":
            fuzzy_acct = verdict_result.get("fuzzy_account", "")
            st.warning(f"⚠️ **此为模糊匹配结果，请人工核实科目。** 系统推荐科目：`{fuzzy_acct}`")

        # ── 判断用户是否已确认 ──
        capitalization_confirmed = st.session_state.get("capitalization_confirmed", False)
        user_chosen_account = st.session_state.get("manual_account_selected", None)

        # ── 高置信度预检（绿色框）也需要一个确认按钮 ──
        # 但如果用户已经在 ambiguous/unknown 弹窗中确认过了，就不再显示此按钮
        if not capitalization_confirmed:
            st.markdown("---")
            st.markdown("### 📋 生成凭证")

            # 检查用户是否已点击"确认并生成凭证"
            if not st.session_state.get("voucher_confirmed", False):
                if st.button("✅ 确认并生成凭证", key="confirm_voucher", type="primary", width="stretch"):
                    st.session_state["voucher_confirmed"] = True
                    st.rerun()
                st.info("👆 请确认上述预检结果无误后，点击上方按钮生成推荐凭证。")
                _show_scenario_table()
                st.stop()

        # ── 执行匹配并生成凭证 ──
        result = _run_matching(text, verdict_result)

        # 展示结果（必须在清除 trigger 之前，否则底部 voucher_result 会重复渲染）
        if isinstance(result, dict) and result.get("_error") == "empty_input":
            st.warning(
                "⚠️ **未识别到核心财税词汇，请补充关键业务词（如采购、维修、工资等）。**"
            )
            _show_scenario_table()

        elif isinstance(result, dict) and result.get("_error") == "timeout":
            st.warning(
                "⚠️ **当前描述较复杂，暂未匹配到精准科目。"
                "建议您选择下方预设场景，或者拆分录入。**"
            )
            _show_scenario_table()

        elif result is not None:
            _display_matched_result(result, text, verdict_result,
                                    capitalization_confirmed, user_chosen_account)
            # 标记已在当前 run 中展示过，防止底部 voucher_result 重复渲染
            st.session_state["_displayed_in_this_run"] = True
            # 清除 trigger，防止 rerun 后重复执行推荐逻辑
            st.session_state["recommend_triggered"] = False

        else:
            # 两层都失败 → 引导用户输入关键词 + 手工入账按钮
            st.warning(
                "⚠️ **当前描述较复杂，暂未匹配到精准科目。"
                "建议您选择下方预设场景，或者拆分录入。**"
            )
            if st.button("📝 手工入账", type="secondary", width="stretch"):
                st.info(
                    "请手动录入会计分录：\n\n"
                    "借：____________________  ￥______\n"
                    "贷：____________________  ￥______\n\n"
                    "（建议咨询会计主管或参考《企业会计准则》确认科目）"
                )
            _show_scenario_table()

# ─── 如果 session 中有已保存的凭证结果且不是刚触发的推荐，直接展示 ──
# 这确保用户刷新页面或 rerun 后不会丢失凭证
# 注意：刚触发的推荐（recommend_triggered=True）已经在上面展示过了，
# 这里只处理页面刷新后或非触发状态下的展示
# 同时避免在同一 run 中重复展示（_displayed_in_this_run 标记）
if (st.session_state.get("voucher_result")
    and not st.session_state.get("recommend_triggered", False)
    and not st.session_state.get("_displayed_in_this_run", False)):
    saved = st.session_state["voucher_result"]
    _display_matched_result(
        saved["result"], saved["text"], saved["verdict_result"],
        saved["capitalization_confirmed"], saved["user_chosen_account"],
    )

# ─── 手工录入凭证区域 ───────────────────────────────────────
st.markdown("---")
st.markdown("### 🛠️ 专业财务人员手工干预区")
st.caption("💡 **提示：** AI推荐仅供参考，实际做账请务必以会计准则为准。复杂业务请在此手工确认。")

with st.expander("📝 展开手工录入凭证", expanded=False):
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        manual_debit = st.text_input(
            "借方科目",
            placeholder="例如：管理费用-办公费",
            key="manual_debit",
        )
    with col_b:
        manual_credit = st.text_input(
            "贷方科目",
            placeholder="例如：银行存款",
            key="manual_credit",
        )
    with col_c:
        manual_amount = st.text_input(
            "金额",
            placeholder="例如：500.00",
            key="manual_amount",
        )

    if st.button("📋 生成手工凭证", type="primary", width="stretch"):
        if not manual_debit or not manual_credit or not manual_amount:
            st.warning("⚠️ 请完整填写借方科目、贷方科目和金额！")
        else:
            try:
                amt = float(manual_amount.replace("¥", "").replace(",", "").strip())
            except ValueError:
                st.error("❌ 金额格式不正确，请输入数字（如 500.00）")
                st.stop()

            st.markdown(
                '<div class="voucher-card">'
                '<div class="voucher-title">📋 手工凭证（已确认）</div>',
                unsafe_allow_html=True,
            )

            col_l, col_r = st.columns([1, 1])
            with col_l:
                st.markdown("**借方**")
                st.markdown(
                    f'<p class="debit-row" style="font-size:1.1rem;">'
                    f'📌 {manual_debit}</p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<p class="amount-cell debit-row" style="font-size:1.3rem;">'
                    f'¥ {amt:,.2f}</p>',
                    unsafe_allow_html=True,
                )
            with col_r:
                st.markdown("**贷方**")
                st.markdown(
                    f'<p class="credit-row" style="font-size:1.1rem;">'
                    f'📌 {manual_credit}</p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<p class="amount-cell credit-row" style="font-size:1.3rem;">'
                    f'¥ {amt:,.2f}</p>',
                    unsafe_allow_html=True,
                )

            st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)

            voucher_data = [
                {"方向": "借", "科目": manual_debit, "金额": f"¥ {amt:,.2f}"},
                {"方向": "贷", "科目": manual_credit, "金额": f"¥ {amt:,.2f}"},
            ]
            st.dataframe(
                voucher_data,
                width="stretch",
                hide_index=True,
                column_config={
                    "方向": st.column_config.TextColumn("方向", width="small"),
                    "科目": st.column_config.TextColumn("会计科目", width="large"),
                    "金额": st.column_config.TextColumn("金额", width="medium"),
                },
            )

            st.markdown("</div>", unsafe_allow_html=True)
            st.success("✅ 手工凭证已生成，请导出或归档。")

# ─── 页脚 ───────────────────────────────────────────────────
st.markdown(
    '<div class="footer">'
    "📒 智能会计凭证推荐系统 · 仅供学习参考，实际做账请以会计准则为准"
    "</div>",
    unsafe_allow_html=True,
)
