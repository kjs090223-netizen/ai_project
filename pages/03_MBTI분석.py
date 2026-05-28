# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="🌍 Countries MBTI Analyzer",
    page_icon="🧠",
    layout="wide"
)

# -----------------------------
# 제목
# -----------------------------
st.title("🌍 국가별 MBTI 비율 분석기")
st.markdown("국가를 선택하면 MBTI 유형 비율을 그래프로 보여줘요 ✨")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# -----------------------------
# 국가 선택
# -----------------------------
country = st.selectbox(
    "🌎 국가를 선택하세요",
    sorted(df["Country"].unique())
)

# -----------------------------
# 선택된 국가 데이터
# -----------------------------
selected_row = df[df["Country"] == country].iloc[0]

mbti_columns = [
    'ISTJ', 'ISFJ', 'INFJ', 'INTJ',
    'ISTP', 'ISFP', 'INFP', 'INTP',
    'ESTP', 'ESFP', 'ENFP', 'ENTP',
    'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ'
]

values = [selected_row[col] * 100 for col in mbti_columns]

chart_df = pd.DataFrame({
    "MBTI": mbti_columns,
    "Percentage": values
})

# -----------------------------
# 정렬
# -----------------------------
chart_df = chart_df.sort_values(
    by="Percentage",
    ascending=False
).reset_index(drop=True)

# -----------------------------
# 색상 설정
# 1등: 핫핑크
# 나머지: 초록 그라데이션
# -----------------------------
green_gradient = [
    f'rgba(34,139,34,{opacity})'
    for opacity in np.linspace(1.0, 0.3, len(chart_df)-1)
]

colors = ['hotpink'] + green_gradient

# -----------------------------
# 그래프
# -----------------------------
fig = go.Figure()

fig.add_trace(go.Bar(
    x=chart_df["MBTI"],
    y=chart_df["Percentage"],
    marker_color=colors,
    text=[f"{v:.2f}%" for v in chart_df["Percentage"]],
    textposition='outside'
))

# -----------------------------
# 그래프 꾸미기
# -----------------------------
fig.update_layout(
    title=f"🧠 {country} MBTI 비율",
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (%)",
    template="plotly_white",
    height=600,
    title_font_size=28,
    font=dict(size=16)
)

# -----------------------------
# 출력
# -----------------------------
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# TOP 3 출력
# -----------------------------
st.subheader("🏆 가장 높은 MBTI TOP 3")

top3 = chart_df.head(3)

for idx, row in top3.iterrows():
    st.markdown(
        f"""
        ### {idx+1}위 🥇  
        **{row['MBTI']}** : {row['Percentage']:.2f}%
        """
    )

# -----------------------------
# 설명
# -----------------------------
st.info(
    "💡 핫핑크는 해당 국가에서 가장 높은 MBTI 유형이에요!"
)
