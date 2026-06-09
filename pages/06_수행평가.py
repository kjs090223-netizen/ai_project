import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# ----------------------------------
# 페이지 설정
# ----------------------------------
st.set_page_config(
    page_title="국가별 교통사고 분석",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 국가별 교통사고 분석")
st.markdown("---")

# ----------------------------------
# CSV 불러오기
# pages 폴더 안에 코드
# csv는 상위 폴더
# ----------------------------------
csv_path = Path(__file__).parent.parent / "kim.csv"

try:
    df = pd.read_csv(csv_path)
except:
    df = pd.read_csv(csv_path, encoding="cp949")

# ----------------------------------
# 컬럼 자동 찾기
# ----------------------------------
country_col = [c for c in df.columns if "국가" in c][0]
death_col = [c for c in df.columns if "사망" in c and "10만" not in c][0]

# ----------------------------------
# 비율 계산
# ----------------------------------
total_death = df[death_col].sum()

df["교통사고 비율"] = (
    df[death_col] / total_death * 100
).round(2)

# 내림차순 정렬
df = df.sort_values(
    "교통사고 비율",
    ascending=False
).reset_index(drop=True)

# ----------------------------------
# 국가 선택
# ----------------------------------
country = st.selectbox(
    "🌎 국가를 선택하세요",
    df[country_col]
)

selected = df[df[country_col] == country]

st.metric(
    "선택 국가 교통사고 비율",
    f"{selected['교통사고 비율'].iloc[0]:.2f}%"
)

# ----------------------------------
# 그래프용 색상
# ----------------------------------
colors = []

for i in range(len(df)):
    if i == 0:
        colors.append("#ff0000")  # 1위 빨강
    else:
        opacity = max(0.25, 1 - (i * 0.03))
        colors.append(
            f"rgba(255,100,100,{opacity})"
        )

# 선택 국가 강조
for idx in df.index:
    if df.loc[idx, country_col] == country:
        colors[idx] = "#0066ff"

# ----------------------------------
# Plotly 그래프
# ----------------------------------
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
        "교통사고 비율: %{x:.2f}%<extra></extra>"
    )
)

fig.update_layout(
    height=900,
    template="plotly_white",
    title={
        "text":"국가별 교통사고 비율 순위",
        "x":0.5
    },
    xaxis_title="교통사고 비율 (%)",
    yaxis_title="국가",
    showlegend=False,
    margin=dict(
        l=20,
        r=20,
        t=70,
        b=20
    )
)

fig.update_yaxes(
    categoryorder="total ascending"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# 선택 국가 상세 정보
# ----------------------------------
st.markdown("---")
st.subheader(f"📊 {country} 상세 정보")

col1, col2 = st.columns(2)

with col1:
    st.write(
        f"**사망자 수:** "
        f"{int(selected[death_col].iloc[0]):,}명"
    )

with col2:
    rank = (
        df.index[
            df[country_col] == country
        ][0] + 1
    )

    st.write(
        f"**비율 순위:** {rank}위"
    )

# ----------------------------------
# TOP10
# ----------------------------------
st.markdown("---")
st.subheader("🏆 교통사고 비율 TOP 10")

top10 = df.head(10)[
    [country_col, "교통사고 비율"]
]

st.dataframe(
    top10,
    use_container_width=True,
    hide_index=True
)
