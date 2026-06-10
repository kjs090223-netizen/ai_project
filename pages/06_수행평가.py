import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# =========================
# 페이지 설정
# =========================
st.set_page_config(
    page_title="국가별 교통사고 분석",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 국가별 교통사고 분석")

# =========================
# CSV 불러오기
# =========================
csv_path = Path(__file__).parent.parent / "kim.csv"

if not csv_path.exists():
    st.error(
        f"""
CSV 파일을 찾을 수 없습니다.

현재 위치:
{csv_path}
"""
    )
    st.stop()

df = None

encodings = [
    "utf-8",
    "utf-8-sig",
    "cp949",
    "euc-kr"
]

for enc in encodings:

    try:
        df = pd.read_csv(
            csv_path,
            encoding=enc
        )
        break

    except:
        continue

if df is None:
    st.error("CSV 읽기 실패")
    st.stop()

# =========================
# 컬럼 확인
# =========================
required_cols = [
    "국가",
    "사고(건)",
    "사망(명)",
    "자동차1만대당 사망(명)",
    "인구10만명당 사망(명)"
]

missing = [
    col
    for col in required_cols
    if col not in df.columns
]

if missing:

    st.error(
        f"없는 컬럼: {missing}"
    )

    st.write(
        list(df.columns)
    )

    st.stop()

# =========================
# 숫자 변환
# =========================
number_cols = [
    "사고(건)",
    "사망(명)",
    "자동차1만대당 사망(명)",
    "인구10만명당 사망(명)"
]

for col in number_cols:

    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

df = df.fillna(0)

# =========================
# 비율 계산
# =========================
total = df["사망(명)"].sum()

df["교통사고 비율"] = (
    df["사망(명)"]
    / total
    * 100
).round(2)

df = (
    df
    .sort_values(
        "교통사고 비율",
        ascending=False
    )
    .reset_index(drop=True)
)

# =========================
# 국가 선택
# =========================
country = st.selectbox(
    "🌍 국가 선택",
    df["국가"]
)

selected = (
    df[
        df["국가"] == country
    ]
    .iloc[0]
)

# =========================
# 색상 설정
# =========================
colors = []

for i in range(len(df)):

    if i == 0:

        colors.append(
            "#ff0000"
        )

    else:

        alpha = max(
            0.25,
            1 - i * 0.03
        )

        colors.append(
            f"rgba(255,80,80,{alpha})"
        )

selected_idx = (
    df.index[
        df["국가"] == country
    ][0]
)

colors[selected_idx] = "#0066ff"

# =========================
# Plotly 그래프
# =========================
fig = go.Figure()

fig.add_trace(
    go.Bar(
        y=df["국가"],
        x=df["교통사고 비율"],
        orientation="h",
        marker_color=colors,
        text=(
            df["교통사고 비율"]
            .astype(str)
            + "%"
        ),
        textposition="outside",
        hovertemplate=
        "<b>%{y}</b><br>"
        "비율: %{x:.2f}%"
        "<extra></extra>"
    )
)

fig.update_layout(
    title="국가별 교통사고 사망 비율",
    template="plotly_white",
    height=900,
    showlegend=False,
    xaxis_title="교통사고 비율 (%)",
    yaxis_title="국가"
)

fig.update_yaxes(
    categoryorder="total ascending"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================
# 상세 정보
# =========================
st.markdown("---")

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "사고 건수",
        f"{int(selected['사고(건)']):,}"
    )

with c2:

    st.metric(
        "사망자 수",
        f"{int(selected['사망(명)']):,}"
    )

with c3:

    rank = selected_idx + 1

    st.metric(
        "비율 순위",
        f"{rank}위"
    )

# =========================
# TOP10
# =========================
st.markdown("---")

st.subheader(
    "🏆 교통사고 비율 TOP10"
)

st.dataframe(
    df[
        [
            "국가",
            "교통사고 비율",
            "사망(명)"
        ]
    ].head(10),
    use_container_width=True,
    hide_index=True
)
