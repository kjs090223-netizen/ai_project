import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# ==========================
# 페이지 설정
# ==========================
st.set_page_config(
    page_title="국가별 교통사고 분석",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 국가별 교통사고 분석")
st.caption("국가별 교통사고 데이터를 분석하고 정책을 제안해보세요")

# ==========================
# CSV 읽기
# ==========================
csv_path = Path(__file__).parent.parent / "kim.csv"

if not csv_path.exists():
    st.error("kim.csv 파일을 찾을 수 없습니다.")
    st.stop()

df = None

for enc in [
    "utf-8",
    "utf-8-sig",
    "cp949",
    "euc-kr"
]:
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

# ==========================
# 숫자 처리
# ==========================
num_cols = [
    "사고(건)",
    "사망(명)",
    "자동차1만대당 사망(명)",
    "인구10만명당 사망(명)"
]

for col in num_cols:

    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
    )

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

df = df.fillna(0)

# ==========================
# 비율 계산
# ==========================
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

# ==========================
# 국가 선택
# ==========================
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

# ==========================
# 색상
# ==========================
colors = []

for i in range(len(df)):

    if i == 0:
        colors.append("#ff0000")

    else:

        alpha = max(
            0.25,
            1 - i * 0.03
        )

        colors.append(
            f"rgba(255,90,90,{alpha})"
        )

selected_idx = (
    df.index[
        df["국가"] == country
    ][0]
)

colors[selected_idx] = "#0066ff"

# ==========================
# Plotly
# ==========================
fig = go.Figure()

fig.add_trace(
    go.Bar(
        y=df["국가"],
        x=df["교통사고 비율"],
        orientation="h",
        marker_color=colors,
        text=df["교통사고 비율"],
        texttemplate="%{text:.1f}%",
        hovertemplate=
        "<b>%{y}</b><br>"
        "비율:%{x:.2f}%<extra></extra>"
    )
)

fig.update_layout(
    template="plotly_white",
    height=850,
    title="국가별 교통사고 사망 비율",
    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# 통계
# ==========================
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
    st.metric(
        "인구10만명당 사망",
        f"{selected['인구10만명당 사망(명)']:.1f}"
    )

# ==========================
# 정책 제안 기능
# ==========================
st.markdown("---")
st.subheader("🚦 내가 정책 담당자라면")

if st.button("정책 제안 생성"):

    death = selected["사망(명)"]
    per_car = selected["자동차1만대당 사망(명)"]
    per_pop = selected["인구10만명당 사망(명)"]

    policy = []

    if death > df["사망(명)"].median():
        policy.append(
            "🚔 교통법규 단속 강화 및 사고 다발 구간 관리"
        )

    if per_car > 1:
        policy.append(
            "🚘 차량 안전기준 강화 및 정기점검 확대"
        )

    if per_pop > 8:
        policy.append(
            "🚶 보행자 보호구역 및 속도 제한 확대"
        )

    if len(policy) == 0:
        policy.append(
            "🌱 현재 수준 유지 및 스마트 교통 시스템 확대"
        )

    st.success(f"{country} 정책 제안")

    for p in policy:
        st.write(p)

    st.info(
        """
📌 해석
현재 국가의 교통사고 지표를 기준으로
개선 효과가 클 것으로 예상되는 정책을 자동 추천했습니다.
"""
    )

# ==========================
# TOP10
# ==========================
st.markdown("---")

st.subheader("🏆 TOP10")

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
