import streamlit as st

# 🎨 페이지 설정
st.set_page_config(
    page_title="MBTI 책 & 영화 추천 🎬📚",
    page_icon="✨",
    layout="centered"
)

# 🧠 MBTI 데이터
mbti_data = {
    "INTJ": {
        "books": [
            {
                "title": "1984",
                "author": "조지 오웰",
                "year": "1900년대 작가 📚",
                "reason": "깊은 사고와 미래 사회에 대한 통찰을 좋아하는 INTJ에게 딱!"
            },
            {
                "title": "아몬드",
                "author": "손원평",
                "year": "2000년 이후 작가 🌟",
                "reason": "감정과 인간관계를 차분하게 바라보게 해주는 이야기!"
            }
        ],
        "movies": [
            {
                "title": "스타워즈 (1977)",
                "reason": "거대한 세계관과 전략적인 이야기 전개가 매력적!"
            },
            {
                "title": "대부 (1972)",
                "reason": "냉철한 판단과 리더십을 좋아한다면 추천!"
            }
        ]
    },

    "INTP": {
        "books": [
            {
                "title": "멋진 신세계",
                "author": "올더스 헉슬리",
                "year": "1900년대 작가 📚",
                "reason": "철학적 상상과 사회 비판을 좋아하는 INTP 취향 저격!"
            },
            {
                "title": "달러구트 꿈 백화점",
                "author": "이미예",
                "year": "2000년 이후 작가 🌟",
                "reason": "독특한 상상력이 가득한 판타지!"
            }
        ],
        "movies": [
            {
                "title": "백 투 더 퓨처 (1985)",
                "reason": "과학과 상상력을 좋아한다면 꼭 봐야 할 영화!"
            },
            {
                "title": "죠스 (1975)",
                "reason": "긴장감 넘치는 전개를 즐길 수 있어!"
            }
        ]
    },

    "ENTP": {
        "books": [
            {
                "title": "위대한 개츠비",
                "author": "F. 스콧 피츠제럴드",
                "year": "1900년대 작가 📚",
                "reason": "화려함과 도전적인 삶을 좋아하는 ENTP에게 추천!"
            },
            {
                "title": "불편한 편의점",
                "author": "김호연",
                "year": "2000년 이후 작가 🌟",
                "reason": "유쾌하면서도 따뜻한 이야기!"
            }
        ],
        "movies": [
            {
                "title": "록키 (1976)",
                "reason": "도전 정신 가득한 스토리!"
            },
            {
                "title": "에이리언 (1979)",
                "reason": "스릴 넘치는 전개와 창의적인 설정!"
            }
        ]
    },

    "INFJ": {
        "books": [
            {
                "title": "어린 왕자",
                "author": "생텍쥐페리",
                "year": "1900년대 작가 📚",
                "reason": "따뜻한 감성과 깊은 메시지가 INFJ와 잘 어울려!"
            },
            {
                "title": "82년생 김지영",
                "author": "조남주",
                "year": "2000년 이후 작가 🌟",
                "reason": "사람과 사회를 깊이 생각하게 만드는 책!"
            }
        ],
        "movies": [
            {
                "title": "사운드 오브 뮤직 (1965)",
                "reason": "따뜻한 감동과 음악이 가득해 🎵"
            },
            {
                "title": "티파니에서 아침을 (1961)",
                "reason": "감성적인 분위기를 좋아한다면 추천!"
            }
        ]
    }
}

# 🔁 나머지 MBTI 자동 추가
default_data = {
    "books": [
        {
            "title": "데미안",
            "author": "헤르만 헤세",
            "year": "1900년대 작가 📚",
            "reason": "자아와 성장에 대해 생각하게 해주는 명작!"
        },
        {
            "title": "미드나잇 라이브러리",
            "author": "매트 헤이그",
            "year": "2000년 이후 작가 🌟",
            "reason": "삶의 선택과 가능성을 돌아보게 하는 이야기!"
        }
    ],
    "movies": [
        {
            "title": "E.T. (1982)",
            "reason": "우정과 모험이 담긴 따뜻한 영화 👽"
        },
        {
            "title": "죠스 (1975)",
            "reason": "긴장감 넘치는 클래식 스릴러!"
        }
    ]
}

all_mbti = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

for mbti in all_mbti:
    if mbti not in mbti_data:
        mbti_data[mbti] = default_data

# 🏠 제목
st.title("✨ MBTI별 책 & 영화 추천 📚🎬")
st.write("너의 MBTI에 어울리는 책과 영화를 추천해줄게 😎")

# 📌 선택
selected_mbti = st.selectbox(
    "🧠 너의 MBTI를 골라봐!",
    all_mbti
)

# 📖 결과 출력
data = mbti_data[selected_mbti]

st.header(f"💡 {selected_mbti} 추천 리스트")

# 📚 책 추천
st.subheader("📚 추천 책 2권")

for book in data["books"]:
    st.markdown(f"""
### 📖 {book['title']}
- ✍️ 작가: **{book['author']}**
- 🕰️ 구분: **{book['year']}**
- 💬 추천 이유: {book['reason']}
""")

# 🎬 영화 추천
st.subheader("🎬 추천 영화 2편")

for movie in data["movies"]:
    st.markdown(f"""
### 🍿 {movie['title']}
- 💬 추천 이유: {movie['reason']}
""")

# 🎉 하단 문구
st.success("오늘의 취향 추천 완료! 😆✨")
st.caption("친구들이랑 서로 MBTI 추천 비교해봐도 재밌어 👀")
