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
st.title("🌍 세계 MBTI 국가 분석기")
st.markdown(
    """
    ### 원하는 분석을 선택해보세요 ✨
    
    1️⃣ 국가를 선택 → 해당 국가의 MBTI 비율 분석  
    2️⃣ MBTI를 선택 → 해당 유형 비율이 높은 국가 TOP10 분석
    """
)

# ---------------------------------------------------
# 데이터 불러오기
# ---------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types.csv")

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
st.sidebar.title("⚙️ 분석 메뉴")

analysis_type = st.sidebar.radio(
    "분석 종류 선택",
    [
        "🌎 국가별 MBTI 분석",
        "🧠 MBTI별 국가 TOP10"
    ]
)

# ===================================================
# 1. 국가별 MBTI 분석
# ===================================================
if analysis_type == "🌎 국가별 MBTI 분석":

    st.header("🌎 국가별 MBTI 비율 분석")

    # 국가 선택
    country = st.selectbox(
        "국가를 선택하세요",
        sorted(df["Country"].unique())
    )

    # 선택된 데이터
    selected_row = df[df["Country"] == country].iloc[0]

    values = [selected_row[col] * 100 for col in mbti_types]

    chart_df = pd.DataFrame({
        "MBTI": mbti_types,
        "Percentage": values
    })

    # 정렬
    chart_df = chart_df.sort_values(
        by="Percentage",
        ascending=False
    ).reset_index(drop=True)

    # 색상
    green_gradient = [
        f'rgba(34,139,34,{opacity})'
        for opacity in np.linspace(1.0, 0.3, len(chart_df)-1)
    ]

    colors = ['hotpink'] + green_gradient

    # 그래프
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=chart_df["MBTI"],
        y=chart_df["Percentage"],
        marker_color=colors,
        text=[f"{v:.2f}%" for v in chart_df["Percentage"]],
        textposition='outside'
    ))

    # 레이아웃
    fig.update_layout(
        title=f"🧠 {country} MBTI 비율",
        xaxis_title="MBTI 유형",
        yaxis_title="비율 (%)",
        template="plotly_white",
        height=650,
        title_font_size=28,
        font=dict(size=16)
    )

    # 출력
    st.plotly_chart(fig, use_container_width=True)

    # TOP3
    st.subheader("🏆 가장 높은 MBTI TOP3")

    top3 = chart_df.head(3)

    medals = ["🥇", "🥈", "🥉"]

    for idx, row in top3.iterrows():
        st.markdown(
            f"""
            ### {medals[idx]} {idx+1}위
            **{row['MBTI']}** : {row['Percentage']:.2f}%
            """
        )

    # 표
    st.subheader("📊 전체 MBTI 비율")

    display_df = chart_df.copy()
    display_df["Percentage"] = display_df["Percentage"].round(2)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    st.info("💡 핫핑크 막대는 해당 국가에서 가장 높은 MBTI 유형이에요!")

# ===================================================
# 2. MBTI별 국가 TOP10
# ===================================================
else:

    st.header("🧠 MBTI 유형별 국가 TOP10")

    # MBTI 선택
    selected_mbti = st.selectbox(
        "MBTI 유형 선택",
        mbti_types
    )

    # TOP10 추출
    top10 = (
        df[["Country", selected_mbti]]
        .sort_values(by=selected_mbti, ascending=False)
        .head(10)
        .reset_index(drop=True)
    )

    # 퍼센트 변환
    top10["Percentage"] = top10[selected_mbti] * 100

    # 색상
    green_gradient = [
        f'rgba(34,139,34,{opacity})'
        for opacity in np.linspace(1.0, 0.3, 9)
    ]

    colors = ['hotpink'] + green_gradient

    # 그래프
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=top10["Country"],
        y=top10["Percentage"],
        marker_color=colors,
        text=[f"{v:.2f}%" for v in top10["Percentage"]],
        textposition='outside'
    ))

    # 레이아웃
    fig.update_layout(
        title=f"🏆 {selected_mbti} 비율이 높은 국가 TOP10",
        xaxis_title="국가",
        yaxis_title="비율 (%)",
        template="plotly_white",
        height=650,
        title_font_size=28,
        font=dict(size=16)
    )

    # 출력
    st.plotly_chart(fig, use_container_width=True)

    # 1위 국가
    winner = top10.iloc[0]

    st.success(
        f"""
🥇 {selected_mbti} 비율 세계 1위 국가는  
### 🌟 {winner['Country']}
비율: **{winner['Percentage']:.2f}%**
"""
    )

    # 표
    st.subheader("📊 TOP10 국가 데이터")

    display_df = top10[["Country", "Percentage"]].copy()

    display_df["Percentage"] = (
        display_df["Percentage"]
        .round(2)
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    st.info("💡 핫핑크 막대는 1위 국가를 의미해요!")

# ---------------------------------------------------
# 푸터
# ---------------------------------------------------
st.markdown("---")
st.markdown(
    """
    🌍 MBTI Countries Analyzer  
    Made with ❤️ using Streamlit & Plotly
    """
)
