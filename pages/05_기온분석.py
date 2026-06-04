import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="서울 기온 분석 및 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 기온 분석 및 미래 예측")

@st.cache_data
def load_data():

    # 인코딩 자동 처리
    try:
        df = pd.read_csv("seoul.csv", encoding="utf-8")
    except:
        df = pd.read_csv("seoul.csv", encoding="cp949")

    df.columns = df.columns.str.strip()

    # 날짜 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"],
        errors="coerce",
        format="mixed"
    )

    df = df.dropna(subset=["날짜"])

    # 기온 숫자 변환
    df["최고기온(℃)"] = pd.to_numeric(
        df["최고기온(℃)"],
        errors="coerce"
    )

    df["최저기온(℃)"] = pd.to_numeric(
        df["최저기온(℃)"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["최고기온(℃)", "최저기온(℃)"]
    )

    return df


df = load_data()

# --------------------------
# 실제 데이터 조회
# --------------------------

st.header("📈 과거 기온 조회")

selected_date = st.date_input(
    "날짜 선택",
    value=df["날짜"].max().date()
)

selected = df[df["날짜"].dt.date == selected_date]

if not selected.empty:

    max_temp = selected["최고기온(℃)"].iloc[0]
    min_temp = selected["최저기온(℃)"].iloc[0]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=["최저기온", "최고기온"],
            y=[min_temp, max_temp],
            mode="lines+markers",
            name="기온",
            line=dict(color="hotpink", width=4),
            marker=dict(size=12)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=["최저기온"],
            y=[min_temp],
            mode="markers",
            name="최저기온",
            marker=dict(color="lightskyblue", size=15)
        )
    )

    fig.update_layout(
        title=f"{selected_date} 기온",
        yaxis_title="기온(℃)",
        legend_title="범례",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("최고기온", f"{max_temp:.1f}℃")

    with col2:
        st.metric("최저기온", f"{min_temp:.1f}℃")

else:
    st.warning("해당 날짜 데이터가 없습니다.")

# --------------------------
# 미래 예측
# --------------------------

st.header("🔮 미래 연도 기온 예측")

df["연도"] = df["날짜"].dt.year

yearly = (
    df.groupby("연도")
    .agg({
        "최고기온(℃)": "max",
        "최저기온(℃)": "min"
    })
    .reset_index()
)

X = yearly[["연도"]]

max_model = LinearRegression()
max_model.fit(X, yearly["최고기온(℃)"])

min_model = LinearRegression()
min_model.fit(X, yearly["최저기온(℃)"])

future_year = st.number_input(
    "예측할 미래 연도",
    min_value=int(yearly["연도"].max() + 1),
    value=int(yearly["연도"].max() + 10),
    step=1
)

pred_max = max_model.predict([[future_year]])[0]
pred_min = min_model.predict([[future_year]])[0]

st.subheader(f"📊 {future_year}년 예측 결과")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "예상 최고기온",
        f"{pred_max:.1f}℃"
    )

with col2:
    st.metric(
        "예상 최저기온",
        f"{pred_min:.1f}℃"
    )

# 예측 그래프

future_df = yearly.copy()

future_df.loc[len(future_df)] = [
    future_year,
    pred_max,
    pred_min
]

fig2 = go.Figure()

fig2.add_trace(
    go.Scatter(
        x=future_df["연도"],
        y=future_df["최고기온(℃)"],
        mode="lines",
        name="최고기온",
        line=dict(
            color="hotpink",
            width=3
        )
    )
)

fig2.add_trace(
    go.Scatter(
        x=future_df["연도"],
        y=future_df["최저기온(℃)"],
        mode="lines",
        name="최저기온",
        line=dict(
            color="lightskyblue",
            width=3
        )
    )
)

fig2.update_layout(
    title="연도별 기온 및 미래 예측",
    xaxis_title="연도",
    yaxis_title="기온(℃)",
    legend_title="범례",
    height=700
)

st.plotly_chart(fig2, use_container_width=True)
