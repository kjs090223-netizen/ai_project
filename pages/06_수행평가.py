import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="연령별 인구 분석",
    page_icon="👨‍👩‍👧‍👦",
    layout="wide"
)

st.title("👨‍👩‍👧‍👦 연령별 인구 분석")

# ------------------
# CSV 자동 찾기
# ------------------
root = Path(__file__).parent.parent

csv_files = list(root.glob("*.csv"))

if not csv_files:
    st.error("CSV 파일이 없습니다.")
    st.stop()

csv_path = csv_files[0]

# ------------------
# CSV 읽기
# ------------------
encodings = [
    "utf-8",
    "utf-8-sig",
    "cp949",
    "euc-kr"
]

df = None

for enc in encodings:
    try:
        df = pd.read_csv(csv_path, encoding=enc)
        break
    except:
        pass

if df is None:
    st.error("파일을 읽을 수 없습니다.")
    st.stop()

# ------------------
# 숫자형 변환
# ------------------
age_cols = [
    "09세",
    "1019세",
    "2029세",
    "3039세",
    "4049세",
    "5059세",
    "6069세",
    "7079세",
    "8089세",
    "9099세",
    "100세 이상"
]

for col in age_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "")
        .astype(float)
    )

# ------------------
# 행정구역 선택
# ------------------
region = st.selectbox(
    "📍 행정구역 선택",
    df["행정구역"]
)

selected = df[df["행정구역"] == region].iloc[0]

# ------------------
# 데이터 생성
# ------------------
chart_df = pd.DataFrame({
    "연령대": age_cols,
    "인구수": [selected[col] for col in age_cols]
})

total = chart_df["인구수"].sum()

chart_df["비율"] = (
    chart_df["인구수"] / total * 100
).round(2)

# ------------------
# 색상
# ------------------
max_idx = chart_df["인구수"].idxmax()

colors = []

for i in range(len(chart_df)):

    if i == max_idx:
        colors.append("#ff0000")

    else:
        opacity = 1 - i * 0.07

        if opacity < 0.3:
            opacity = 0.3

        colors.append(
            f"rgba(0,120,255,{opacity})"
        )

# ------------------
# 그래프
# ------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=chart_df["연령대"],
        y=chart_df["비율"],
        marker_color=colors,
        text=chart_df["비율"].astype(str) + "%",
        textposition="outside",
        hovertemplate=
        "<b>%{x}</b><br>" +
        "비율: %{y:.2f}%<extra></extra>"
    )
)

fig.update_layout(
    title=f"{region} 연령대별 인구 비율",
    template="plotly_white",
    height=600,
    showlegend=False,
    yaxis_title="비율 (%)",
    xaxis_title="연령대"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ------------------
# 통계
# ------------------
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "총 인구수",
        f"{int(total):,}명"
    )

with col2:
    top_age = chart_df.loc[
        chart_df["인구수"].idxmax(),
        "연령대"
    ]

    st.metric(
        "가장 많은 연령대",
        top_age
    )

# ------------------
# 표
# ------------------
st.markdown("---")

st.subheader("📊 상세 데이터")

st.dataframe(
    chart_df,
    use_container_width=True,
    hide_index=True
)
