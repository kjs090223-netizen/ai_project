import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# -------------------------------
# 페이지 설정
# -------------------------------
st.set_page_config(
    page_title="국가별 교통사고 분석",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 국가별 교통사고 분석")

# -------------------------------
# CSV 자동 찾기
# -------------------------------
root = Path(__file__).parent.parent

csv_files = list(root.glob("*.csv"))

if len(csv_files) == 0:
    st.error("상위 폴더에 CSV 파일이 없습니다.")
    st.stop()

csv_path = csv_files[0]

st.caption(f"불러온 파일 : {csv_path.name}")

# -------------------------------
# CSV 읽기
# -------------------------------
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
    st.error("CSV 파일을 읽을 수 없습니다.")
    st.stop()

# -------------------------------
# 컬럼 찾기
# -------------------------------
country_col = None
death_col = None

for col in df.columns:

    col_str = str(col)

    if "국가" in col_str:
        country_col = col

    if (
        "사망" in col_str
        and "10만" not in col_str
        and "1만" not in col_str
    ):
        death_col = col

if country_col is None or death_col is None:
    st.error(
        f"""
필수 컬럼을 찾을 수 없습니다.

현재 컬럼:
{list(df.columns)}
"""
    )
    st.stop()

# -------------------------------
# 비율 계산
# -------------------------------
total = df[death_col].sum()

df["교통사고 비율"] = (
    df[death_col] / total * 100
).round(2)

df = df.sort_values(
    "교통사고 비율",
    ascending=False
).reset_index(drop=True)

# -------------------------------
# 국가 선택
# -------------------------------
country = st.selectbox(
    "🌏 국가 선택",
    df[country_col]
)

selected_row = df[
    df[country_col] == country
].iloc[0]

# -------------------------------
# 색상
# -------------------------------
colors = []

for i in range(len(df)):

    if i == 0:
        colors.append("#ff0000")

    else:

        opacity = max(
            0.25,
            1 - i * 0.03
        )

        colors.append(
            f"rgba(255,80,80,{opacity})"
        )

# 선택 국가 파랑 강조
selected_idx = df.index[
    df[country_col] == country
][0]

colors[selected_idx] = "#0066ff"

# -------------------------------
# Plotly 그래프
# -------------------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        y=df[country_col],
        x=df["교통사고 비율"],
        orientation="h",
        marker_color=colors,
        text=df["교통사고 비율"].astype(str) + "%",
        textposition="outside",
        hovertemplate=
        "<b>%{y}</b><br>"
        "비율: %{x:.2f}%"
        "<extra></extra>"
    )
)

fig.update_layout(
    title="국가별 교통사고 사망 비율",
    template="plotly_white",
    height=900,
    showlegend=False
)

fig.update_yaxes(
    categoryorder="total ascending"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------
# 선택 국가 정보
# -------------------------------
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "교통사고 비율",
        f"{selected_row['교통사고 비율']:.2f}%"
    )

with col2:
    rank = selected_idx + 1

    st.metric(
        "순위",
        f"{rank}위"
    )

# -------------------------------
# TOP10
# -------------------------------
st.markdown("---")

st.subheader("🏆 TOP 10 국가")

st.dataframe(
    df[
        [country_col, "교통사고 비율"]
    ].head(10),
    use_container_width=True,
    hide_index=True
)
