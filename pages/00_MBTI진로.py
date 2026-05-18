
import streamlit as st

st.set_page_config(
    page_title="MBTI 진로 추천 🌈",
    page_icon="✨",
    layout="centered"
)

# MBTI별 추천 데이터
mbti_data = {
    "INTJ": [
        {
            "job": "데이터 사이언티스트 💻",
            "major": "컴퓨터공학과, 인공지능학과",
            "personality": "논리적이고 분석적인 사람에게 잘 어울려!",
            "salary": "평균 연봉 약 5,500만원"
        },
        {
            "job": "건축가 🏢",
            "major": "건축학과",
            "personality": "계획 세우는 걸 좋아하고 창의적인 성격이면 좋아!",
            "salary": "평균 연봉 약 5,000만원"
        }
    ],
    "INTP": [
        {
            "job": "프로그래머 👨‍💻",
            "major": "소프트웨어학과, 컴퓨터공학과",
            "personality": "호기심 많고 문제 해결 좋아하는 성격 추천!",
            "salary": "평균 연봉 약 5,200만원"
        },
        {
            "job": "연구원 🔬",
            "major": "물리학과, 화학과",
            "personality": "깊게 탐구하는 걸 좋아하면 잘 맞아!",
            "salary": "평균 연봉 약 4,800만원"
        }
    ],
    "ENTJ": [
        {
            "job": "CEO 🏆",
            "major": "경영학과",
            "personality": "리더십 강하고 추진력 있는 사람 추천!",
            "salary": "평균 연봉 약 7,000만원"
        },
        {
            "job": "마케팅 기획자 📈",
            "major": "광고홍보학과",
            "personality": "사람 이끄는 걸 좋아하면 딱이야!",
            "salary": "평균 연봉 약 4,700만원"
        }
    ],
    "ENTP": [
        {
            "job": "광고 기획자 🎨",
            "major": "광고홍보학과",
            "personality": "아이디어 넘치고 말 잘하는 성격 추천!",
            "salary": "평균 연봉 약 4,500만원"
        },
        {
            "job": "창업가 🚀",
            "major": "경영학과",
            "personality": "새로운 도전 좋아하면 잘 어울려!",
            "salary": "평균 연봉은 다양하지만 성공 시 매우 높아!"
        }
    ],
    "INFJ": [
        {
            "job": "상담사 💖",
            "major": "심리학과",
            "personality": "공감 능력 좋고 배려심 깊은 사람 추천!",
            "salary": "평균 연봉 약 4,200만원"
        },
        {
            "job": "작가 ✍️",
            "major": "문예창작과",
            "personality": "감수성 풍부하고 상상력 많은 성격 추천!",
            "salary": "평균 연봉 약 3,800만원"
        }
    ],
    "INFP": [
        {
            "job": "일러스트레이터 🎨",
            "major": "디자인학과",
            "personality": "감성적이고 창의적인 사람에게 추천!",
            "salary": "평균 연봉 약 3,500만원"
        },
        {
            "job": "사회복지사 🤝",
            "major": "사회복지학과",
            "personality": "따뜻한 마음을 가진 사람에게 잘 맞아!",
            "salary": "평균 연봉 약 3,600만원"
        }
    ],
    "ENFJ": [
        {
            "job": "교사 🍎",
            "major": "교육학과",
            "personality": "사람 도와주는 걸 좋아하면 최고!",
            "salary": "평균 연봉 약 5,000만원"
        },
        {
            "job": "HR 매니저 👔",
            "major": "경영학과",
            "personality": "소통 능력 좋은 사람 추천!",
            "salary": "평균 연봉 약 5,300만원"
        }
    ],
    "ENFP": [
        {
            "job": "유튜버 📹",
            "major": "미디어학과",
            "personality": "에너지 넘치고 끼 많은 사람 추천!",
            "salary": "수입 차이가 크지만 인기 많으면 매우 높아!"
        },
        {
            "job": "여행 작가 ✈️",
            "major": "관광학과",
            "personality": "자유로운 분위기 좋아하면 잘 맞아!",
            "salary": "평균 연봉 약 3,800만원"
        }
    ],
    "ISTJ": [
        {
            "job": "공무원 🏛️",
            "major": "행정학과",
            "personality": "책임감 강하고 꼼꼼한 사람 추천!",
            "salary": "평균 연봉 약 4,500만원"
        },
        {
            "job": "회계사 📊",
            "major": "회계학과",
            "personality": "계산 정확하게 하는 걸 좋아하면 좋아!",
            "salary": "평균 연봉 약 6,000만원"
        }
    ],
    "ISFJ": [
        {
            "job": "간호사 🏥",
            "major": "간호학과",
            "personality": "배려심 많고 성실한 사람 추천!",
            "salary": "평균 연봉 약 4,700만원"
        },
        {
            "job": "유치원 교사 🧸",
            "major": "유아교육과",
            "personality": "아이 좋아하면 정말 잘 맞아!",
            "salary": "평균 연봉 약 3,700만원"
        }
    ],
    "ESTJ": [
        {
            "job": "경찰관 🚓",
            "major": "경찰행정학과",
            "personality": "리더십 있고 책임감 강한 사람 추천!",
            "salary": "평균 연봉 약 5,000만원"
        },
        {
            "job": "관리자 📋",
            "major": "경영학과",
            "personality": "체계적으로 일하는 걸 좋아하면 딱!",
            "salary": "평균 연봉 약 5,500만원"
        }
    ],
    "ESFJ": [
        {
            "job": "승무원 ✈️",
            "major": "항공서비스학과",
            "personality": "친절하고 사교적인 사람 추천!",
            "salary": "평균 연봉 약 4,500만원"
        },
        {
            "job": "호텔리어 🏨",
            "major": "호텔관광학과",
            "personality": "사람 응대하는 걸 좋아하면 좋아!",
            "salary": "평균 연봉 약 4,200만원"
        }
    ],
    "ISTP": [
        {
            "job": "자동차 엔지니어 🚗",
            "major": "기계공학과",
            "personality": "손으로 만드는 걸 좋아하면 추천!",
            "salary": "평균 연봉 약 5,500만원"
        },
        {
            "job": "파일럿 ✈️",
            "major": "항공운항학과",
            "personality": "침착하고 집중력 높은 사람 추천!",
            "salary": "평균 연봉 약 7,000만원"
        }
    ],
    "ISFP": [
        {
            "job": "패션 디자이너 👗",
            "major": "패션디자인학과",
            "personality": "예술 감각 뛰어난 사람 추천!",
            "salary": "평균 연봉 약 4,000만원"
        },
        {
            "job": "플로리스트 🌸",
            "major": "원예학과",
            "personality": "감성적이고 섬세한 사람 추천!",
            "salary": "평균 연봉 약 3,500만원"
        }
    ],
    "ESTP": [
        {
            "job": "영업 전문가 💼",
            "major": "경영학과",
            "personality": "활발하고 자신감 넘치는 사람 추천!",
            "salary": "평균 연봉 약 5,000만원"
        },
        {
            "job": "스포츠 트레이너 🏋️",
            "major": "체육학과",
            "personality": "활동적인 거 좋아하면 최고!",
            "salary": "평균 연봉 약 3,800만원"
        }
    ],
    "ESFP": [
        {
            "job": "배우 🎭",
            "major": "연극영화과",
            "personality": "끼 많고 사람 좋아하는 성격 추천!",
            "salary": "수입 차이가 크지만 인기 많으면 매우 높아!"
        },
        {
            "job": "이벤트 플래너 🎉",
            "major": "관광경영학과",
            "personality": "분위기 메이커 스타일이면 잘 맞아!",
            "salary": "평균 연봉 약 4,000만원"
        }
    ]
}

st.title("✨ MBTI 진로 추천 서비스 ✨")
st.write("너의 MBTI에 어울리는 진로를 찾아보자 😎")

mbti = st.selectbox(
    "👉 MBTI를 선택해줘!",
    list(mbti_data.keys())
)

if st.button("추천 보기 🔍"):
    st.subheader(f"🌈 {mbti} 유형 추천 진로")

    careers = mbti_data[mbti]

    for career in careers:
        st.markdown(f"""
        ---
        ## {career['job']}

        🎓 **추천 학과**  
        {career['major']}

        😊 **잘 맞는 성격**  
        {career['personality']}

        💰 **평균 연봉**  
        {career['salary']}
        """)

    st.success("🔥 미래는 아직 무한 가능성! 재밌게 탐색해봐 😆")
