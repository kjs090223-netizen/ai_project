# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# ---------------------------------------------------
# 페이지 설정
# ---------------------------------------------------
st.set_page_config(
    page_title="🌍 MBTI Countries Analyzer",
    page_icon="🧠",
    layout="wide"
)

# ---------------------------------------------------
# 제목
# ---------------------------------------------------
st.title("🌍 MBTI 유형별 국가 분석기")
st.markdown(
    """
    원하는 MBTI 유형을 선택하면  
    해당 유형 비율이 가장 높은 국가 TOP10을 보여줘요 ✨
    """
)

# ---------------------------------------------------
# 데이터 불러오기
# ---------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# ---------------------------------------------------
# MBTI 목록
# ---------------------------------------------------
mbti_types = [
    'ISTJ', 'ISFJ', 'INFJ', 'INTJ',
    'ISTP', 'ISFP', 'INFP', 'INTP',
    'ESTP', 'ESFP', 'ENFP', 'ENTP',
    'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ'
]

# ---------------------------------------------------
# 사이드바
# ---------------------------------------------------
st.sidebar.title("⚙️ 설정")

selected_mbti = st.sidebar.selectbox(
    "🧠 MBTI 유형 선택",
    mbti_types
)

# ---------------------------------------------------
# 데이터 정렬
# ---------------------------------------------------
top10 = (
    df[["Country", selected_mbti]]
    .sort_values(by=selected_mbti, ascending=False)
    .head(10)
    .reset_index(drop=True)
)

# 퍼센트 변환
top10["Percentage"] = top10[selected_mbti] * 100

# ---------------------------------------------------
# 색상 설정
# 1등 = 핫핑크
# 나머지 = 초록색 그라데이션
# ---------------------------------------------------
green_gradient = [
    f'rgba(34,139,34,{opacity})'
    for opacity in np.linspace(1.0, 0.3, 9)
]

colors = ['hotpink'] + green_gradient

# ---------------------------------------------------
# 그래프 생성
# ---------------------------------------------------
fig = go.Figure()

fig.add_trace(go.Bar(
    x=top10["Country"],
    y=top10["Percentage"],
    marker_color=colors,
    text=[f"{v:.2f}%" for v in top10["Percentage"]],
    textposition='outside'
))

# ---------------------------------------------------
# 그래프 꾸미기
# ---------------------------------------------------
fig.update_layout(
    title=f"🏆 {selected_mbti} 비율이 가장 높은 국가 TOP10",
    xaxis_title="국가",
    yaxis_title="비율 (%)",
    template="plotly_white",
    height=650,
    title_font_size=28,
    font=dict(size=16),
)

# ---------------------------------------------------
# 그래프 출력
# ---------------------------------------------------
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# 1위 국가 강조
# ---------------------------------------------------
winner = top10.iloc[0]

st.success(
    f"""
🥇 {selected_mbti} 비율 세계 1위 국가는  
### 🌟 {winner['Country']}
비율: **{winner['Percentage']:.2f}%**
"""
)

# ---------------------------------------------------
# TOP10 표 출력
# ---------------------------------------------------
st.subheader("📊 국가 순위 데이터")

table_df = top10[["Country", "Percentage"]].copy()
table_df.columns = ["Country", "MBTI Percentage (%)"]

table_df["MBTI Percentage (%)"] = (
    table_df["MBTI Percentage (%)"]
    .round(2)
)

st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True
)

# ---------------------------------------------------
# 추가 설명
# ---------------------------------------------------
st.info(
    "💡 핫핑크 막대는 해당 MBTI 비율이 가장 높은 국가예요!"
)

# ---------------------------------------------------
# 푸터
# ---------------------------------------------------
st.markdown("---")
st.markdown(
    "Made with ❤️ using Streamlit & Plotly"
)
