import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="서울 인구 분석",
    page_icon="📊",
    layout="wide"
)

# GitHub RAW URL 입력
RAW_URL = "https://raw.githubusercontent.com/사용자명/저장소명/main/population.csv"

@st.cache_data
def load_data():

    encodings = ["utf-8", "utf-8-sig", "cp949", "euc-kr"]

    for enc in encodings:
        try:
            return pd.read_csv(RAW_URL, encoding=enc)
        except:
            pass

    raise Exception("CSV 파일을 읽을 수 없습니다.")

try:

    df = load_data()

    st.title("📊 행정구별 연령대 인구 분석")

    st.write("데이터 미리보기")
    st.dataframe(df.head())

    region_col = df.columns[0]

    selected_region = st.selectbox(
        "행정구 선택",
        df[region_col].unique()
    )

    row = df[df[region_col] == selected_region].iloc[0]

    # 숫자형 연령 컬럼만 추출
    age_cols = []

    for col in df.columns[1:]:
        if "세" in str(col) or "이상" in str(col):
            age_cols.append(col)

    populations = []

    for col in age_cols:
        value = str(row[col]).replace(",", "")
        populations.append(int(float(value)))

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=age_cols,
            y=populations,
            mode="lines+markers",
            line=dict(
                color="red",
                width=4
            ),
            marker=dict(
                size=8
            )
        )
    )

    fig.update_layout(
        title=f"{selected_region} 연령대별 인구",
        xaxis_title="나이",
        yaxis_title="인구수",
        plot_bgcolor="#f0f0f0",
        paper_bgcolor="#f0f0f0",
        height=600
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

except Exception as e:

    st.error("오류 발생")
    st.code(str(e))
