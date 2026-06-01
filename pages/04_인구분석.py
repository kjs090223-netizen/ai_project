import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="서울 인구 분석",
    page_icon="📊",
    layout="wide"
)

# =========================
# GitHub RAW 주소 입력
# =========================
RAW_URL = "여기에_GitHub_RAW_URL_입력"

# =========================
# 데이터 불러오기
# =========================
@st.cache_data
def load_data():

    encodings = [
        "utf-8",
        "utf-8-sig",
        "cp949",
        "euc-kr"
    ]

    for enc in encodings:
        try:
            return pd.read_csv(RAW_URL, encoding=enc)
        except:
            continue

    raise Exception(
        "CSV 파일 인코딩을 읽을 수 없습니다."
    )

try:

    df = load_data()

    st.title("📊 행정구별 연령대 인구 분석")

    # 첫 번째 열 = 행정구
    region_col = df.columns[0]

    regions = df[region_col].unique()

    selected_region = st.selectbox(
        "🏙️ 행정구 선택",
        regions
    )

    selected_row = df[
        df[region_col] == selected_region
    ].iloc[0]

    age_columns = list(df.columns[1:])

    populations = []

    for col in age_columns:
        value = str(selected_row[col]).replace(",", "")
        populations.append(float(value))

    # =========================
    # 그래프
    # =========================

    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(
        figsize=(12, 6)
    )

    # 연한 회색 배경
    fig.patch.set_facecolor("#f2f2f2")
    ax.set_facecolor("#f2f2f2")

    # 빨간색 꺾은선
    ax.plot(
        age_columns,
        populations,
        color="red",
        linewidth=3,
        marker="o",
        markersize=8
    )

    ax.set_title(
        f"{selected_region} 연령대별 인구",
        fontsize=18,
        fontweight="bold"
    )

    ax.set_xlabel("나이")
    ax.set_ylabel("인구수")

    ax.grid(
        linestyle="--",
        alpha=0.5
    )

    plt.xticks(rotation=45)

    st.pyplot(fig)

    # =========================
    # 데이터 테이블
    # =========================

    st.subheader("📋 연령대별 인구")

    result_df = pd.DataFrame({
        "나이대": age_columns,
        "인구수": populations
    })

    st.dataframe(
        result_df,
        use_container_width=True
    )

except Exception as e:

    st.error("데이터를 불러올 수 없습니다.")
    st.code(str(e))
