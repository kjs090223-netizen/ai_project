# app.py
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="서울 관광지 TOP10 🗺️",
    page_icon="📍",
    layout="wide"
)

st.title("🇰🇷 외국인들이 좋아하는 서울 관광지 TOP10")
st.markdown("서울의 인기 관광지를 지도에서 확인해보세요! ✨")

# 관광지 데이터
spots = [
    {
        "name": "경복궁",
        "location": [37.5796, 126.9770],
        "station": "경복궁역 (3호선)",
        "fun": "한복 체험 👘, 궁궐 산책, 사진 촬영 📸"
    },
    {
        "name": "N서울타워",
        "location": [37.5512, 126.9882],
        "station": "명동역 (4호선)",
        "fun": "야경 감상 🌃, 사랑의 자물쇠 🔒"
    },
    {
        "name": "명동",
        "location": [37.5636, 126.9827],
        "station": "명동역 (4호선)",
        "fun": "쇼핑 🛍️, 길거리 음식 🍢"
    },
    {
        "name": "홍대거리",
        "location": [37.5563, 126.9220],
        "station": "홍대입구역 (2호선)",
        "fun": "버스킹 🎸, 카페 투어 ☕"
    },
    {
        "name": "북촌한옥마을",
        "location": [37.5826, 126.9830],
        "station": "안국역 (3호선)",
        "fun": "전통 한옥 구경 🏡, 감성 사진 📷"
    },
    {
        "name": "롯데월드",
        "location": [37.5110, 127.0980],
        "station": "잠실역 (2호선)",
        "fun": "놀이기구 🎢, 아이스링크 ⛸️"
    },
    {
        "name": "코엑스",
        "location": [37.5125, 127.0588],
        "station": "삼성역 (2호선)",
        "fun": "별마당도서관 📚, 쇼핑 🛒"
    },
    {
        "name": "광장시장",
        "location": [37.5704, 126.9998],
        "station": "종로5가역 (1호선)",
        "fun": "빈대떡 🥞, 마약김밥 🍙"
    },
    {
        "name": "한강공원",
        "location": [37.5207, 126.9396],
        "station": "여의나루역 (5호선)",
        "fun": "치맥 🍗🍺, 자전거 🚴"
    },
    {
        "name": "동대문디자인플라자(DDP)",
        "location": [37.5665, 127.0092],
        "station": "동대문역사문화공원역 (2호선)",
        "fun": "야경 ✨, 전시회 🎨"
    }
]

# 서울 중심 지도 생성
m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=11
)

# 노란색 마커 추가
for spot in spots:
    folium.Marker(
        location=spot["location"],
        tooltip=f"🚇 가까운 역: {spot['station']}",
        popup=f"""
        <b>{spot['name']}</b><br>
        🚇 {spot['station']}<br>
        🎈 {spot['fun']}
        """,
        icon=folium.Icon(color="orange", icon="star")
    ).add_to(m)

# 지도 출력
st.subheader("📍 서울 관광 지도")
st_folium(m, width=1000, height=600)

# 관광지 설명
st.subheader("🎉 관광지 & 가까운 지하철역 정보")

for idx, spot in enumerate(spots, start=1):
    st.markdown(f"""
    ### {idx}. {spot['name']}
    - 🚇 가까운 역: **{spot['station']}**
    - 🎈 놀거리: {spot['fun']}
    """)

st.success("즐거운 서울 여행 되세요! 🇰🇷✨")
