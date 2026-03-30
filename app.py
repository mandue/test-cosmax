import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="시제품 안정성 분석 대시보드", layout="wide")

# ── 커스텀 CSS ──
st.markdown("""
<style>
/* ── 전체 배경 ── */
.stApp {
    background: #F5F7FB;
}

/* 사이드바 숨기기 */
section[data-testid="stSidebar"] { display: none; }

/* ── 제목 ── */
h1 {
    color: #1B2A4A !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
    padding-bottom: 4px;
    border-bottom: 3px solid #4A7BF7;
    display: inline-block;
}
h2, h3 {
    color: #2C3E6B !important;
    font-weight: 700 !important;
}

/* ── 메트릭 카드 ── */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #FFFFFF 0%, #EDF2FB 100%);
    border: 1px solid #C4D3EB;
    border-radius: 16px;
    padding: 20px 24px;
    box-shadow: 0 2px 12px rgba(74, 123, 247, 0.08);
    transition: transform 0.2s, box-shadow 0.2s;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(74, 123, 247, 0.15);
}
div[data-testid="stMetric"] label {
    color: #5A7BA6 !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}
div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    color: #1B2A4A !important;
    font-weight: 700 !important;
    font-size: 1.8rem !important;
}

/* ── 차트 카드 ── */
div.stPlotlyChart {
    background: #FFFFFF;
    border: 1px solid #D6DFEF;
    border-radius: 16px;
    padding: 12px;
    box-shadow: 0 2px 10px rgba(44, 62, 107, 0.06);
}

/* ── 파일 업로더 ── */
div[data-testid="stFileUploader"] {
    background: #FFFFFF;
    border: 2px dashed #93ADDB;
    border-radius: 20px;
    padding: 24px;
    transition: border-color 0.2s;
}
div[data-testid="stFileUploader"]:hover {
    border-color: #4A7BF7;
}

/* ══════════════════════════════════════ */
/* ── 필터 pill 버튼 (popover trigger) ── */
/* ══════════════════════════════════════ */
div[data-testid="stPopover"] > button {
    background: #FFFFFF !important;
    border: 1.5px solid #D6DFEF !important;
    border-radius: 24px !important;
    color: #3A4D6B !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    padding: 8px 20px !important;
    transition: all 0.2s !important;
    width: auto !important;
    min-width: 0 !important;
}
div[data-testid="stPopover"] > button:hover {
    border-color: #4A7BF7 !important;
    color: #4A7BF7 !important;
    box-shadow: 0 2px 8px rgba(74, 123, 247, 0.10) !important;
}
/* 활성 필터 pill (CSS class 로 구분 불가 → JS 없이 불가하므로 popover body 스타일로 보완) */
div[data-testid="stPopoverBody"] {
    border-radius: 16px !important;
    border: 1px solid #D6DFEF !important;
    box-shadow: 0 10px 36px rgba(44, 62, 107, 0.14) !important;
    padding: 12px 8px !important;
    max-height: 360px;
    overflow-y: auto;
}

/* 체크박스 행 */
div[data-testid="stPopoverBody"] div[data-testid="stCheckbox"] label {
    padding: 7px 14px !important;
    border-radius: 10px !important;
    transition: background 0.15s !important;
    cursor: pointer !important;
    font-size: 0.9rem !important;
}
div[data-testid="stPopoverBody"] div[data-testid="stCheckbox"] label:hover {
    background: #EDF2FB !important;
}

/* ══════════════════════ */
/* ── 태그 바 (하단) ──  */
/* ══════════════════════ */
.tag-bar {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    padding: 14px 20px;
    background: #FFFFFF;
    border: 1px solid #E0E8F5;
    border-radius: 14px;
    min-height: 48px;
    box-shadow: 0 1px 4px rgba(44, 62, 107, 0.04);
}
.tag-bar-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    flex: 1;
}
.tag-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #3468E5;
    color: #FFFFFF;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.01em;
    white-space: nowrap;
}
.tag-pill .tag-x {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: rgba(255,255,255,0.25);
    font-size: 0.7rem;
    cursor: default;
}
.tag-empty {
    color: #8DA0BE;
    font-size: 0.85rem;
}
.tag-reset {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    color: #5A7BA6;
    font-size: 0.85rem;
    font-weight: 600;
    white-space: nowrap;
    cursor: default;
}
.tag-reset .reset-icon { font-size: 1rem; }

/* ── 버튼 (초기화 등) ── */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 8px 20px !important;
    transition: all 0.2s !important;
}

/* ── Expander ── */
div[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid #D6DFEF;
    border-radius: 16px !important;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(44, 62, 107, 0.05);
}

/* ── Tabs ── */
button[data-baseweb="tab"] {
    border-radius: 12px 12px 0 0 !important;
    font-weight: 600 !important;
}

/* ── 구분선 ── */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #B0C4DE, transparent);
    margin: 1.5rem 0;
}

/* ── info 박스 ── */
div[data-testid="stAlert"] {
    border-radius: 14px !important;
    border-left: 4px solid #4A7BF7 !important;
}
</style>
""", unsafe_allow_html=True)

# ── 타이틀 ──
st.title("시제품 안정성 테스트 대시보드")

# 파일 업로드
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요 (.xlsx)", type=["xlsx"])

if uploaded_file is None:
    st.info("엑셀 파일을 업로드하면 대시보드가 표시됩니다.")
    st.stop()

# 데이터 로드
df_product = pd.read_excel(uploaded_file, sheet_name="시제품정보")
df_test = pd.read_excel(uploaded_file, sheet_name="안정성테스트결과")
df = df_test.merge(df_product, on="시제품코드", how="left")

# ── Plotly 공통 레이아웃 ──
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(240,244,250,0.5)",
    font=dict(family="Pretendard, -apple-system, sans-serif", color="#1B2A4A", size=13),
    margin=dict(t=24, b=24, l=16, r=16),
    legend=dict(bgcolor="rgba(255,255,255,0.8)", bordercolor="#D6DFEF", borderwidth=1, font=dict(size=12)),
    xaxis=dict(gridcolor="#E0E8F5", zerolinecolor="#C4D3EB"),
    yaxis=dict(gridcolor="#E0E8F5", zerolinecolor="#C4D3EB"),
)
CHART_COLORS = ["#4A7BF7", "#6C63FF", "#36B5A0", "#F5A623", "#E85D75",
                "#8B5CF6", "#3AAFA9", "#FF6B6B", "#4ECDC4", "#45B7D1"]
RESULT_COLORS = {"적합": "#36B5A0", "경미변화": "#F5A623", "부적합": "#E85D75"}

# ══════════════════════════════════════════════════
# ── 필터 시스템 ──
# ══════════════════════════════════════════════════

FILTERS = {
    "sel_products":   {"label": "시제품코드", "col": "시제품코드"},
    "sel_conditions": {"label": "테스트조건", "col": "테스트조건"},
    "sel_results":    {"label": "판정결과",  "col": "판정결과"},
    "sel_types":      {"label": "제품유형",  "col": "제품유형"},
    "sel_stages":     {"label": "개발단계",  "col": "개발단계"},
    "sel_teams":      {"label": "담당팀",   "col": "담당팀"},
}

all_values = {}
for key, meta in FILTERS.items():
    vals = sorted(df[meta["col"]].dropna().unique())
    all_values[key] = vals
    if key not in st.session_state:
        st.session_state[key] = {v: True for v in vals}


# ── 콜백 ──
def _toggle_all(state_key):
    new_val = st.session_state[f"{state_key}__all"]
    for v in all_values[state_key]:
        st.session_state[f"{state_key}__{v}"] = new_val
        st.session_state[state_key][v] = new_val


def _toggle_item(state_key, item):
    new_val = st.session_state[f"{state_key}__{item}"]
    st.session_state[state_key][item] = new_val
    all_on = all(st.session_state[state_key].get(v, True) for v in all_values[state_key])
    st.session_state[f"{state_key}__all"] = all_on


def _remove_tag(state_key, item):
    st.session_state[state_key][item] = False
    st.session_state[f"{state_key}__{item}"] = False
    all_on = all(st.session_state[state_key].get(v, True) for v in all_values[state_key])
    st.session_state[f"{state_key}__all"] = all_on


# ── 필터 pill 행 (가로 나열) ──
pill_cols = st.columns(len(FILTERS))

for idx, (state_key, meta) in enumerate(FILTERS.items()):
    label = meta["label"]
    state = st.session_state[state_key]
    vals = all_values[state_key]
    selected_count = sum(state.values())
    is_all = selected_count == len(vals)
    none_selected = selected_count == 0

    if is_all or none_selected:
        btn_text = f"{label}  ▾"
    else:
        btn_text = f"**{label}**  ▾"

    with pill_cols[idx]:
        with st.popover(btn_text, use_container_width=True):
            st.checkbox(
                "전체",
                value=is_all,
                key=f"{state_key}__all",
                on_change=_toggle_all,
                args=(state_key,),
            )
            st.markdown("<hr style='margin:4px 0;background:#E0E8F5;height:1px;border:none;'>", unsafe_allow_html=True)
            for v in vals:
                st.checkbox(
                    str(v),
                    value=state.get(v, True),
                    key=f"{state_key}__{v}",
                    on_change=_toggle_item,
                    args=(state_key, v),
                )

# ── 태그 바: 적용 필터 + 개별 제거 버튼 + 초기화 ──
active_tags = []  # (state_key, value, label)
for state_key, meta in FILTERS.items():
    state = st.session_state[state_key]
    vals = all_values[state_key]
    if sum(state.values()) < len(vals):
        for v in vals:
            if state.get(v, True):
                active_tags.append((state_key, v, meta["label"]))

all_default = len(active_tags) == 0

if all_default:
    st.markdown(
        '<div class="tag-bar"><span class="tag-empty">모든 필터가 전체로 설정되어 있습니다.</span></div>',
        unsafe_allow_html=True,
    )
else:
    # 태그 HTML
    tags_html = '<div class="tag-bar"><div class="tag-bar-tags">'
    for _, v, lbl in active_tags:
        tags_html += f'<span class="tag-pill">{lbl}: {v}<span class="tag-x">&times;</span></span>'
    tags_html += '</div></div>'
    st.markdown(tags_html, unsafe_allow_html=True)

    # 개별 제거 버튼 + 초기화 버튼 (태그 아래)
    max_cols = min(len(active_tags), 10)
    btn_cols = st.columns(max_cols + 1)
    for i, (sk, v, lbl) in enumerate(active_tags[:max_cols]):
        with btn_cols[i]:
            if st.button(f"{v} ✕", key=f"rm_{sk}_{v}", use_container_width=True):
                _remove_tag(sk, v)
                st.rerun()
    with btn_cols[-1]:
        if st.button("초기화", key="reset_all", use_container_width=True):
            for sk in FILTERS:
                st.session_state[sk] = {v: True for v in all_values[sk]}
                for v in all_values[sk]:
                    st.session_state[f"{sk}__{v}"] = True
                st.session_state[f"{sk}__all"] = True
            st.rerun()

# ── 필터 적용 ──
selected = {}
for state_key, meta in FILTERS.items():
    state = st.session_state[state_key]
    sel = [v for v, on in state.items() if on]
    selected[meta["col"]] = sel

filtered = df.copy()
for col, sel in selected.items():
    if sel:
        filtered = filtered[filtered[col].isin(sel)]
    else:
        filtered = filtered[filtered[col].isin(all_values[[k for k, m in FILTERS.items() if m["col"] == col][0]])]

if len(filtered) == 0:
    st.warning("선택된 필터에 해당하는 데이터가 없습니다.")
    st.stop()

# ── KPI 카드 ──
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("총 테스트 수", len(filtered))
col2.metric("시제품 수", filtered["시제품코드"].nunique())
pass_rate = (filtered["판정결과"] == "적합").mean() * 100
col3.metric("적합률", f"{pass_rate:.1f}%")
col4.metric("평균 pH", f"{filtered['pH'].mean():.2f}")

# ── 1행: 판정결과 분포 + 테스트조건별 판정 ──
st.markdown("---")
row1_left, row1_right = st.columns(2)

with row1_left:
    st.subheader("판정결과 분포")
    result_counts = filtered["판정결과"].value_counts().reset_index()
    result_counts.columns = ["판정결과", "건수"]
    fig = px.pie(result_counts, names="판정결과", values="건수", color="판정결과",
                 color_discrete_map=RESULT_COLORS, hole=0.45)
    fig.update_traces(textinfo="percent+label", textfont_size=13,
                      marker=dict(line=dict(color="#FFFFFF", width=2)))
    fig.update_layout(**PLOT_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

with row1_right:
    st.subheader("테스트조건별 판정결과")
    ct = filtered.groupby(["테스트조건", "판정결과"]).size().reset_index(name="건수")
    fig2 = px.bar(ct, x="테스트조건", y="건수", color="판정결과", barmode="group",
                  color_discrete_map=RESULT_COLORS)
    fig2.update_traces(marker_line_width=0, marker_cornerradius=8)
    fig2.update_layout(**PLOT_LAYOUT)
    st.plotly_chart(fig2, use_container_width=True)

# ── 2행: 보관기간별 pH 변화 + 점도 변화 ──
row2_left, row2_right = st.columns(2)

with row2_left:
    st.subheader("보관기간별 pH 변화")
    fig3 = px.line(filtered.sort_values("보관기간_주"),
                   x="보관기간_주", y="pH", color="시제품코드", markers=True,
                   color_discrete_sequence=CHART_COLORS)
    fig3.update_traces(line=dict(width=2.5), marker=dict(size=8))
    fig3.update_layout(**PLOT_LAYOUT, xaxis_title="보관기간 (주)", yaxis_title="pH")
    st.plotly_chart(fig3, use_container_width=True)

with row2_right:
    st.subheader("보관기간별 점도 변화")
    fig4 = px.line(filtered.sort_values("보관기간_주"),
                   x="보관기간_주", y="점도_cP", color="시제품코드", markers=True,
                   color_discrete_sequence=CHART_COLORS)
    fig4.update_traces(line=dict(width=2.5), marker=dict(size=8))
    fig4.update_layout(**PLOT_LAYOUT, xaxis_title="보관기간 (주)", yaxis_title="점도 (cP)")
    st.plotly_chart(fig4, use_container_width=True)

# ── 3행: 시제품별 적합률 + 색상변화등급 히트맵 ──
row3_left, row3_right = st.columns(2)

with row3_left:
    st.subheader("시제품별 적합률")
    prod_pass = (
        filtered.groupby("시제품코드")
        .apply(lambda g: (g["판정결과"] == "적합").mean() * 100)
        .reset_index(name="적합률(%)")
        .sort_values("적합률(%)")
    )
    fig5 = px.bar(prod_pass, x="적합률(%)", y="시제품코드", orientation="h", color="적합률(%)",
                  color_continuous_scale=["#E85D75", "#F5A623", "#36B5A0"], range_color=[0, 100])
    fig5.update_traces(marker_cornerradius=8)
    fig5.update_layout(**PLOT_LAYOUT)
    st.plotly_chart(fig5, use_container_width=True)

with row3_right:
    st.subheader("시제품 x 테스트조건 색상변화등급 (평균)")
    heatmap_data = filtered.pivot_table(index="시제품코드", columns="테스트조건", values="색상변화등급", aggfunc="mean")
    fig6 = px.imshow(heatmap_data, text_auto=".1f",
                     color_continuous_scale=["#EDF2FB", "#4A7BF7", "#1B2A4A"], aspect="auto")
    fig6.update_layout(**PLOT_LAYOUT)
    st.plotly_chart(fig6, use_container_width=True)

# ── 4행: 보관온도별 pH 분포 + 이상현상 요약 ──
row4_left, row4_right = st.columns(2)

with row4_left:
    st.subheader("보관온도별 pH 분포")
    fig7 = px.box(filtered, x="보관온도", y="pH", color="보관온도",
                  color_discrete_sequence=["#4A7BF7", "#6C63FF", "#8B5CF6", "#36B5A0"])
    fig7.update_traces(marker=dict(size=5), line=dict(width=1.5))
    fig7.update_layout(**PLOT_LAYOUT)
    st.plotly_chart(fig7, use_container_width=True)

with row4_right:
    st.subheader("이상현상 요약")
    anomaly = filtered.groupby("시제품코드").agg(
        향변화건수=("향변화여부", lambda x: (x == "Y").sum()),
        분리현상건수=("분리현상여부", lambda x: (x == "Y").sum()),
        부적합건수=("판정결과", lambda x: (x == "부적합").sum()),
    ).reset_index()
    fig8 = px.bar(anomaly.melt(id_vars="시제품코드", var_name="항목", value_name="건수"),
                  x="시제품코드", y="건수", color="항목", barmode="group",
                  color_discrete_sequence=["#F5A623", "#8B5CF6", "#E85D75"])
    fig8.update_traces(marker_cornerradius=8, marker_line_width=0)
    fig8.update_layout(**PLOT_LAYOUT)
    st.plotly_chart(fig8, use_container_width=True)

# ── 원본 데이터 테이블 ──
st.markdown("---")
with st.expander("원본 데이터 보기"):
    tab1, tab2 = st.tabs(["시제품정보", "안정성테스트결과"])
    with tab1:
        st.dataframe(df_product, use_container_width=True)
    with tab2:
        st.dataframe(filtered, use_container_width=True)
