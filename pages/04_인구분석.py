import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="서울 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 서울시 연령대별 인구 분석")

uploaded_file = st.file_uploader(
    "population.csv 파일을 업로드하세요",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    region_col = df.columns[0]

    regions = df[region_col].tolist()

    selected_region = st.selectbox(
        "행정구를 선택하세요",
        regions
    )

    row = df[df[region_col] == selected_region].iloc[0]

    age_columns = [
        col for col in df.columns
        if col != region_col
    ]

    populations = row[age_columns].values

    fig, ax = plt.subplots(figsize=(10, 5))

    # 배경색
    fig.patch.set_facecolor("#f2f2f2")
    ax.set_facecolor("#f2f2f2")

    # 꺾은선 그래프
    ax.plot(
        age_columns,
        populations,
        color="red",
        marker="o",
        linewidth=3
    )

    ax.set_title(
        f"{selected_region} 연령대별 인구",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel("나이")
    ax.set_ylabel("인구수")

    ax.grid(
        True,
        linestyle="--",
        alpha=0.5
    )

    plt.xticks(rotation=45)

    st.pyplot(fig)

    st.subheader("📋 선택한 지역 데이터")
    result_df = pd.DataFrame({
        "나이대": age_columns,
        "인구수": populations
    })

    st.dataframe(
        result_df,
        use_container_width=True
    )

else:
    st.info("population.csv 파일을 업로드해주세요.")
