import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="서울 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 서울 행정구별 연령대 인구 분석")

# GitHub Raw URL
RAW_URL = "https://raw.githubusercontent.com/사용자이름/저장소명/main/population.csv"

@st.cache_data
def load_data():
    return pd.read_csv(RAW_URL)

try:
    df = load_data()

    region_col = df.columns[0]

    regions = df[region_col].tolist()

    selected_region = st.selectbox(
        "🏙️ 행정구 선택",
        regions
    )

    row = df[df[region_col] == selected_region].iloc[0]

    age_columns = df.columns[1:]
    populations = row[age_columns]

    fig, ax = plt.subplots(figsize=(12, 6))

    # 연한 회색 배경
    fig.patch.set_facecolor("#f0f0f0")
    ax.set_facecolor("#f0f0f0")

    # 빨간색 꺾은선
    ax.plot(
        age_columns,
        populations,
        color="red",
        marker="o",
        linewidth=3
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

    st.subheader("📋 연령대별 인구")

    result_df = pd.DataFrame({
        "나이대": age_columns,
        "인구수": populations.values
    })

    st.dataframe(
        result_df,
        use_container_width=True
    )

except Exception as e:
    st.error(f"데이터를 불러올 수 없습니다.\n\n{e}")
