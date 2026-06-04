import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# ---------------------------
# 페이지 설정
# ---------------------------

st.set_page_config(
    page_title="서울 기온 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 기온 분석 및 미래 예측")

# ---------------------------
# 데이터 불러오기
# ---------------------------

@st.cache_data
def load_data():

    # 인코딩 자동 처리
    try:
        df = pd.read_csv("seoul.csv", encoding="cp949")
    except:
        try:
            df = pd.read_csv("seoul.csv", encoding="utf-8")
        except:
            df = pd.read_csv("seoul.csv", encoding="euc-kr")

    # 컬럼명 공백 제거
    df.columns = df.columns.str.strip()

    # 날짜 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"],
        errors="coerce",
        format="mixed"
    )

    df = df.dropna(subset=["날짜"])

    # 기온 데이터 숫자 변환
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

    # 연도 월 일 추출
    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df


df = load_data()

# ---------------------------
# 사이드바
# ---------------------------

st.sidebar.header("📅 날짜 선택")

month = st.sidebar.selectbox(
    "월 선택",
    range(1, 13),
    index=0
)

day = st.sidebar.selectbox(
    "일 선택",
    range(1, 32),
    index=0
)

future_year = st.sidebar.number_input(
    "예측할 미래 연도",
    min_value=int(df["연도"].max() + 1),
    value=int(df["연도"].max() + 10),
    step=1
)

# ---------------------------
# 선택 날짜 데이터 추출
# ---------------------------

target = df[
    (df["월"] == month) &
    (df["일"] == day)
].copy()

st.subheader(f"📈 {month}월 {day}일의 역대 기온 변화")

if len(target) < 5:
    st.warning("해당 날짜의 데이터가 부족합니다.")
    st.stop()

target = target.sort_values("연도")

# ---------------------------
# 선형회귀 예측
# ---------------------------

X = target[["연도"]]

y_max = target["최고기온(℃)"]
y_min = target["최저기온(℃)"]

model_max = LinearRegression()
model_min = LinearRegression()

model_max.fit(X, y_max)
model_min.fit(X, y_min)

pred_max = model_max.predict([[future_year]])[0]
pred_min = model_min.predict([[future_year]])[0]

# ---------------------------
# 그래프 생성
# ---------------------------

fig = go.Figure()

# 최고기온
fig.add_trace(
    go.Scatter(
        x=target["연도"],
        y=target["최고기온(℃)"],
        mode="lines",
        name="최고기온",
        line=dict(
            color="hotpink",
            width=3
        )
    )
)

# 최저기온
fig.add_trace(
    go.Scatter(
        x=target["연도"],
        y=target["최저기온(℃)"],
        mode="lines",
        name="최저기온",
        line=dict(
            color="lightskyblue",
            width=3
        )
    )
)

# 예측 최고기온
fig.add_trace(
    go.Scatter(
        x=[future_year],
        y=[pred_max],
        mode="markers+text",
        text=[f"{pred_max:.1f}℃"],
        textposition="top center",
        name="예측 최고기온",
        marker=dict(
            color="hotpink",
            size=12
        )
    )
)

# 예측 최저기온
fig.add_trace(
    go.Scatter(
        x=[future_year],
        y=[pred_min],
        mode="markers+text",
        text=[f"{pred_min:.1f}℃"],
        textposition="bottom center",
        name="예측 최저기온",
        marker=dict(
            color="lightskyblue",
            size=12
        )
    )
)

fig.update_layout(
    title=f"{month}월 {day}일 기온 변화 및 미래 예측",
    xaxis_title="연도",
    yaxis_title="기온 (℃)",
    hovermode="x unified",
    legend_title="범례",
    height=700
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------
# 예측 결과
# ---------------------------

st.subheader("🔮 미래 기온 예측")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        f"{future_year}년 예상 최고기온",
        f"{pred_max:.2f} ℃"
    )

with col2:
    st.metric(
        f"{future_year}년 예상 최저기온",
        f"{pred_min:.2f} ℃"
    )

# ---------------------------
# 데이터 보기
# ---------------------------

with st.expander("📋 사용된 데이터 보기"):
    st.dataframe(
        target[
            [
                "날짜",
                "최고기온(℃)",
                "최저기온(℃)"
            ]
        ],
        use_container_width=True
    )

st.info(
    "예측값은 과거 데이터를 기반으로 한 선형회귀 결과이며 실제 기온과 차이가 있을 수 있습니다."
)
