import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="서울 기온 분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 기온 데이터 분석")
st.write("날짜 범위를 선택하면 최고기온과 최저기온 변화를 확인할 수 있습니다.")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("seoul.csv", encoding="cp949")

    # 날짜 변환
    df["날짜"] = pd.to_datetime(df["날짜"])

    # 결측치 제거
    df["최고기온(℃)"] = pd.to_numeric(df["최고기온(℃)"], errors="coerce")
    df["최저기온(℃)"] = pd.to_numeric(df["최저기온(℃)"], errors="coerce")

    df = df.dropna(subset=["최고기온(℃)", "최저기온(℃)"])

    return df

df = load_data()

# 날짜 선택
st.sidebar.header("📅 날짜 선택")

start_date = st.sidebar.date_input(
    "시작 날짜",
    value=df["날짜"].min().date(),
    min_value=df["날짜"].min().date(),
    max_value=df["날짜"].max().date()
)

end_date = st.sidebar.date_input(
    "종료 날짜",
    value=df["날짜"].max().date(),
    min_value=df["날짜"].min().date(),
    max_value=df["날짜"].max().date()
)

# 데이터 필터링
filtered_df = df[
    (df["날짜"] >= pd.to_datetime(start_date))
    & (df["날짜"] <= pd.to_datetime(end_date))
]

st.subheader("📈 최고기온 · 최저기온 변화")

# 그래프 생성
fig = go.Figure()

# 최고기온 (핫핑크)
fig.add_trace(
    go.Scatter(
        x=filtered_df["날짜"],
        y=filtered_df["최고기온(℃)"],
        mode="lines",
        name="최고기온",
        line=dict(color="hotpink", width=3)
    )
)

# 최저기온 (연한 하늘색)
fig.add_trace(
    go.Scatter(
        x=filtered_df["날짜"],
        y=filtered_df["최저기온(℃)"],
        mode="lines",
        name="최저기온",
        line=dict(color="lightskyblue", width=3)
    )
)

fig.update_layout(
    title="서울 기온 변화",
    xaxis_title="날짜",
    yaxis_title="기온(℃)",
    hovermode="x unified",
    legend_title="범례",
    height=650
)

st.plotly_chart(fig, use_container_width=True)

# 통계
st.subheader("📊 선택 구간 통계")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "최고기온 최고값",
        f"{filtered_df['최고기온(℃)'].max():.1f}℃"
    )

with col2:
    st.metric(
        "최저기온 최저값",
        f"{filtered_df['최저기온(℃)'].min():.1f}℃"
    )

# 데이터 표시
with st.expander("원본 데이터 보기"):
    st.dataframe(filtered_df, use_container_width=True)

st.caption("데이터 출처: seoul.csv")
