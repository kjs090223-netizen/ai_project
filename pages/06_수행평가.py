import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# ---------------------------------
# 페이지 설정
# ---------------------------------
st.set_page_config(
    page_title="연령별 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 행정구역별 연령 인구 분석")

# ---------------------------------
# CSV 경로
# ---------------------------------
csv_path = Path(__file__).parent.parent / "kim.csv"

# CSV 존재 확인
if not csv_path.exists():
    st.error(
        f"""
CSV 파일을 찾을 수 없습니다.

현재 찾는 위치:
{csv_path}
"""
    )
    st.stop()

# ---------------------------------
# CSV 읽기
# ---------------------------------
df = None

encodings = [
    "utf-8",
    "utf-8-sig",
    "cp949",
    "euc-kr"
]

for enc in encodings:

    try:
        df = pd.read_csv(
            csv_path,
            encoding=enc
        )
        break

    except:
        continue

if df is None:
    st.error("CSV 읽기 실패")
    st.stop()

# ---------------------------------
# 연령 컬럼
# ---------------------------------
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

# 컬럼 체크
missing = [
    col
    for col in age_cols
    if col not in df.columns
]

if missing:
    st.error(
        f"없는 컬럼: {missing}"
    )
    st.write(df.columns.tolist())
    st.stop()

# ---------------------------------
# 숫자 변환
# ---------------------------------
for col in age_cols:

    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

df = df.fillna(0)

# ---------------------------------
# 지역 선택
# ---------------------------------
region = st.selectbox(
    "📍 행정구역 선택",
    df["행정구역"].unique()
)

selected = (
    df[
        df["행정구역"] == region
    ]
    .iloc[0]
)

# ---------------------------------
# 차트 데이터
# ---------------------------------
chart_df = pd.DataFrame({
    "연령대": age_cols,
    "인구수": [
        selected[col]
        for col in age_cols
    ]
})

total = chart_df["인구수"].sum()

chart_df["비율"] = (
    chart_df["인구수"]
    / total
    * 100
).round(2)

# ---------------------------------
# 색상
# ---------------------------------
max_idx = (
    chart_df["비율"]
    .idxmax()
)

colors = []

for i in range(len(chart_df)):

    if i == max_idx:
        colors.append(
            "#ff0000"
        )

    else:

        alpha = max(
            0.3,
            1 - i * 0.08
        )

        colors.append(
            f"rgba(80,150,255,{alpha})"
        )

# ---------------------------------
# Plotly 그래프
# ---------------------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=chart_df["연령대"],
        y=chart_df["비율"],
        marker_color=colors,
        text=(
            chart_df["비율"]
            .astype(str)
            + "%"
        ),
        textposition="outside",
        hovertemplate=
        "<b>%{x}</b><br>"
        "비율: %{y:.2f}%"
        "<extra></extra>"
    )
)

fig.update_layout(
    title=f"{region} 연령별 인구 비율",
    template="plotly_white",
    height=650,
    showlegend=False,
    xaxis_title="연령대",
    yaxis_title="비율 (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------
# 요약
# ---------------------------------
st.markdown("---")

c1, c2 = st.columns(2)

with c1:

    st.metric(
        "총 인구",
        f"{int(total):,}명"
    )

with c2:

    st.metric(
        "가장 많은 연령대",
        chart_df.loc[
            max_idx,
            "연령대"
        ]
    )

# ---------------------------------
# 표
# ---------------------------------
st.markdown("---")

st.subheader(
    "📋 상세 데이터"
)

st.dataframe(
    chart_df,
    use_container_width=True,
    hide_index=True
)
