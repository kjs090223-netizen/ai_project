import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="서울 기온 분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 기온 분석")

@st.cache_data
def load_data():

    # utf-8 → cp949 순서로 시도
    try:
        df = pd.read_csv("seoul.csv", encoding="utf-8")
    except:
        df = pd.read_csv("seoul.csv", encoding="cp949")

    # 컬럼명 공백 제거
    df.columns = df.columns.str.strip()

    # 날짜 변환 (오류 해결)
    df["날짜"] = pd.to_datetime(
        df["날짜"],
        errors="coerce"
    )

    # 날짜 변환 실패 행 제거
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

    return df.sort_values("날짜")


df = load_data()

st.sidebar.header("📅 날짜 선택")

start_date = st.sidebar.date_input(
    "시작 날짜",
    value=df["날짜"].min().date()
)

end_date = st.sidebar.date_input(
    "종료 날짜",
    value=df["날짜"].max().date()
)

filtered_df = df[
    (df["날짜"] >= pd.to_datetime(start_date))
    & (df["날짜"] <= pd.to_datetime(end_date))
]

st.subheader("📈 최고기온 · 최저기온 그래프")

fig = go.Figure()

# 최고기온
fig.add_trace(
    go.Scatter(
        x=filtered_df["날짜"],
        y=filtered_df["최고기온(℃)"],
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
        x=filtered_df["날짜"],
        y=filtered_df["최저기온(℃)"],
        mode="lines",
        name="최저기온",
        line=dict(
            color="lightskyblue",
            width=3
        )
    )
)

fig.update_layout(
    title="서울 최고기온 · 최저기온 변화",
    xaxis_title="날짜",
    yaxis_title="기온(℃)",
    hovermode="x unified",
    legend_title="범례",
    height=700
)

st.plotly_chart(
    fig,
    use_container_width=True
)

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

with st.expander("데이터 보기"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )
