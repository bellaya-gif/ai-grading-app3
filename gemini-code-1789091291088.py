import re
import streamlit as st

# ============================================================
# 페이지 기본 설정
# ============================================================
st.set_page_config(
    page_title="문장 성분 및 문장 구조 서술형 평가 채점 시스템",
    layout="wide",
)

st.title("📝 문장 성분 및 문장 구조 서술형 평가 채점 시스템")
st.caption(
    "문제를 확인하고 답안을 입력한 후 채점 버튼을 누르면 "
    "핵심 정답 요소와 보완할 점을 확인할 수 있습니다."
)

# ============================================================
# 공통 함수
# ============================================================
def contains_any(text, keywords):
    text = text.replace(" ", "")
    return any(kw.replace(" ", "") in text for kw in keywords)


def normalize(text):
    """채점 시 띄어쓰기와 일부 표기를 유연하게 처리한다."""
    return re.sub(r"\s+", "", text.strip())


def show_result(score, total, passes, deductions):
    st.subheader(f"💯 채점 결과: {score} / {total}점")

    if passes:
        st.success(
            "충족된 정답 요건:\n\n"
            + "\n".join(f"• {item}" for item in passes)
        )

    if deductions:
        st.error(
            "📌 보완할 점:\n\n"
            + "\n".join(f"• {item}" for item in deductions)
        )

    if not deductions:
        st.info("모든 핵심 채점 요소가 충족되었습니다.")


# ============================================================
# 탭 구성
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "[1번] 서술어 자릿수와 필수적 부사어",
        "[2번] 보어와 필수적 부사어",
        "[3번] 관계 관형절과 동격 관형절",
        "[4번] 이어진 문장",
        "[5번] 안긴절의 유형과 문법적 구실",
    ]
)


# ============================================================
# [문항 1] 서술어의 자릿수와 필수적 부사어
# ============================================================
with tab1:
    st.markdown("### [문항 1] 서술어의 자릿수와 필수적 부사어")

    st.info(
        """
**[문제]** 다음 문장에서 서술어 **‘선물했다’**의 자릿수를 쓰고,
서술어가 필수적으로 요구하는 문장 성분을 찾아 그 문장 성분의
종류와 이유를 서술하시오.

**제시문:** 지훈이가 유나에게 예쁜 꽃다발을 선물했다.
"""
    )

    q1_target = st.text_input(
        "1. 서술어의 자릿수와 필수적으로 요구되는 문장 성분:",
        placeholder="예: 세 자리 서술어, 유나에게(필수적 부사어)",
        key="q1_t",
    )
    q1_reason = st.text_area(
        "2. 해당 문장 성분이 필수적인 이유:",
        placeholder="서술어가 어떤 성분을 요구하는지 설명해 보세요.",
        key="q1_r",
    )

    if st.button("1번 문항 채점", key="btn1"):
        score = 0
        deductions = []
        passes = []

        t = normalize(q1_target)
        r = normalize(q1_reason)

        # 1. 자릿수
        if contains_any(t, ["세자리", "3자리", "세자릿수", "3자릿수"]):
            score += 1
            passes.append("‘선물했다’를 세 자리 서술어로 정확하게 판단함")
        else:
            deductions.append(
                "자릿수: ‘선물했다’는 주어·목적어·선물을 받는 대상을 "
                "나타내는 성분을 요구하므로 세 자리 서술어로 봄."
            )

        # 2. 필수적 부사어
        if contains_any(t + r, ["유나에게", "받는대상", "대상"]) and \
           contains_any(t + r, ["부사어", "필수적부사어"]):
            score += 1
            passes.append("‘유나에게’를 필수적 부사어로 정확하게 제시함")
        else:
            deductions.append(
                "필수 성분: ‘유나에게’는 부사어의 형태이지만 "
                "‘선물했다’가 요구하는 선물을 받는 대상을 나타내는 필수적 부사어임."
            )

        # 3. 이유 설명
        has_required = contains_any(
            r, ["필수", "요구", "필요", "생략하기어렵", "생략할수없"]
        )
        has_receiver = contains_any(
            r, ["받는대상", "받는사람", "대상", "누구에게", "상대"]
        )

        if has_required:
            score += 1
            passes.append("필수적으로 요구되는 성분이라는 점을 설명함")
        else:
            deductions.append(
                "이유 설명: ‘유나에게’가 서술어가 필수적으로 요구하는 성분임을 밝혀야 함."
            )

        if has_receiver:
            score += 1
            passes.append("‘선물을 받는 대상’이라는 의미적 기능을 설명함")
        else:
            deductions.append(
                "의미 설명: ‘유나에게’가 선물을 받는 대상을 나타낸다는 점을 설명하면 좋음."
            )

        show_result(score, 4, passes, deductions)

    with st.expander("💡 모범 답안"):
        st.markdown(
            """
- **서술어의 자릿수:** 세 자리 서술어
- **필수적으로 요구되는 문장 성분:** ‘유나에게’(필수적 부사어)
- **이유:** ‘선물했다’는 주어와 목적어뿐 아니라 선물을 받는 대상을
  나타내는 성분을 요구한다. ‘유나에게’는 부사어의 형태이지만
  서술어가 필수적으로 요구하는 성분이므로 필수적 부사어이다.
"""
        )


# ============================================================
# [문항 2] 보어와 필수적 부사어의 구별
# ============================================================
with tab2:
    st.markdown("### [문항 2] 보어와 필수적 부사어의 구별")

    st.info(
        """
**[문제]** 다음 (가), (나)의 괄호 친 문장 성분의 명칭을 각각 쓰고,
두 성분을 구별하는 기준을 **서술어와 조사의 관계**를 중심으로 설명하시오.

- **(가)** 기범이는 훌륭한 **(교사가)** 되었다.
- **(나)** 얼음이 **(물로)** 되었다.
"""
    )

    q2_names = st.text_input(
        "1. (가)와 (나)의 문장 성분 명칭:",
        placeholder="예: (가) 보어, (나) 필수적 부사어",
        key="q2_n",
    )
    q2_reason = st.text_area(
        "2. 두 성분을 구별하는 기준:",
        placeholder="‘되다’와 조사의 관계를 중심으로 설명하세요.",
        key="q2_r",
    )

    if st.button("2번 문항 채점", key="btn2"):
        score = 0
        deductions = []
        passes = []

        n = normalize(q2_names)
        r = normalize(q2_reason)

        ga_correct = "보어" in n
        na_correct = contains_any(n, ["부사어", "필수적부사어"])

        if ga_correct and na_correct:
            score += 2
            passes.append("(가)는 보어, (나)는 필수적 부사어라고 정확하게 판단함")
        else:
            deductions.append(
                "(가)는 ‘교사가’ → 보어, (나)는 ‘물로’ → 필수적 부사어임."
            )

        # 서술어 조건
        if contains_any(r, ["되다", "아니다", "서술어"]) and \
           contains_any(r, ["필수", "요구"]):
            score += 1
            passes.append("보어와 필수적 부사어가 서술어의 요구와 관련됨을 설명함")
        else:
            deductions.append(
                "서술어와의 관계: 보어는 주로 ‘되다’, ‘아니다’와 같은 "
                "서술어가 요구하는 성분이라는 점을 설명해야 함."
            )

        # 조사 차이
        has_ga = contains_any(r, ["보격조사", "이/가", "이가", "가결합", "이결합"])
        has_ro = contains_any(r, ["부사격조사", "로", "으로"])

        if has_ga and has_ro:
            score += 1
            passes.append("보격 조사 ‘이/가’와 부사격 조사 ‘로/으로’의 차이를 설명함")
        else:
            deductions.append(
                "조사 차이: (가)의 ‘교사가’에는 보격 조사 ‘이/가’가, "
                "(나)의 ‘물로’에는 부사격 조사 ‘로’가 결합함."
            )

        show_result(score, 4, passes, deductions)

    with st.expander("💡 모범 답안"):
        st.markdown(
            """
- **(가):** ‘교사가’ → 보어
- **(나):** ‘물로’ → 필수적 부사어
- **구별 기준:** 두 성분 모두 서술어가 요구하는 필수 성분이지만,
  (가)의 ‘교사가’에는 보격 조사 ‘이/가’가 결합하여 보어가 되고,
  (나)의 ‘물로’에는 부사격 조사 ‘로’가 결합하여 필수적 부사어가 된다.
  ‘되다’, ‘아니다’와 같은 서술어와 결합하는 성분이라고 해서 모두
  보어가 되는 것은 아니며, 조사와 문장 구조를 함께 살펴야 한다.
"""
        )


# ============================================================
# [문항 3] 관계 관형절과 동격 관형절
# ============================================================
with tab3:
    st.markdown("### [문항 3] 관계 관형절과 동격 관형절의 구조적 차이")

    st.info(
        """
**[문제]** 다음 (가), (나)의 문장에서 관형절을 각각 찾아 쓰고,
관계 관형절과 동격 관형절 중 어느 것인지 밝히시오.
또한 관형절 내부의 생략된 문장 성분을 중심으로 두 관형절의
구조적 차이를 설명하시오.

- **(가)** 동생이 만든 케이크는 정말 달콤했다.
- **(나)** 우리가 우승했다는 소문이 학교에 퍼졌다.
"""
    )

    q3_ga = st.text_input(
        "1. (가) 관형절과 유형:",
        placeholder="예: ‘동생이 만든’, 관계 관형절",
        key="q3_g",
    )
    q3_na = st.text_input(
        "2. (나) 관형절과 유형:",
        placeholder="예: ‘우리가 우승했다는’, 동격 관형절",
        key="q3_n",
    )
    q3_diff = st.text_area(
        "3. 두 관형절의 구조적 차이:",
        placeholder="관형절 내부에서 생략된 성분이 있는지 비교해 보세요.",
        key="q3_d",
    )

    if st.button("3번 문항 채점", key="btn3"):
        score = 0
        deductions = []
        passes = []

        g = normalize(q3_ga)
        n = normalize(q3_na)
        d = normalize(q3_diff)

        if "동생이만든" in g and "관계" in g:
            score += 2
            passes.append("(가) ‘동생이 만든’ / 관계 관형절을 정확하게 판단함")
        else:
            deductions.append(
                "(가): 관형절은 ‘동생이 만든’이며 관계 관형절임."
            )

        if "우리가우승했다는" in n and "동격" in n:
            score += 2
            passes.append("(나) ‘우리가 우승했다는’ / 동격 관형절을 정확하게 판단함")
        else:
            deductions.append(
                "(나): 관형절은 ‘우리가 우승했다는’이며 동격 관형절임."
            )

        ga_structure = contains_any(
            d, ["목적어", "케이크", "생략", "생략됨", "빠진"]
        )
        na_structure = contains_any(
            d, ["없", "생략된성분이없", "빠진성분이없", "내용", "소문"]
        )

        if ga_structure:
            score += 1
            passes.append("(가)에서 수식받는 ‘케이크’가 관형절 내부의 목적어에 대응함을 설명함")
        else:
            deductions.append(
                "(가): ‘동생이 케이크를 만들었다’에서 ‘케이크를’이 "
                "관형절 내부의 목적어에 대응하여 생략된 구조임을 설명해야 함."
            )

        if na_structure:
            score += 1
            passes.append("(나)에서 관형절 전체가 ‘소문’의 내용을 나타냄을 설명함")
        else:
            deductions.append(
                "(나): ‘우리가 우승했다’라는 내용 전체가 ‘소문’의 내용을 "
                "나타내므로 관형절 내부에 수식받는 체언과 대응하는 성분이 없음을 설명해야 함."
            )

        show_result(score, 6, passes, deductions)

    with st.expander("💡 모범 답안"):
        st.markdown(
            """
- **(가) 관형절:** ‘동생이 만든’ → **관계 관형절**
  - ‘동생이 케이크를 만들었다’에서 ‘케이크를’이 관형절 내부의
    목적어에 해당하며, 이 성분이 생략된 구조이다.
- **(나) 관형절:** ‘우리가 우승했다는’ → **동격 관형절**
  - ‘우리가 우승했다’라는 절 전체가 ‘소문’의 내용을 나타낸다.
    따라서 관형절 내부에 수식받는 체언과 대응하여 생략된 성분이 없다.
"""
        )


# ============================================================
# [문항 4] 이어진 문장
# ============================================================
with tab4:
    st.markdown("### [문항 4] 이어진 문장의 의미 관계")

    st.info(
        """
**[문제]** 다음 문장을 두 절로 나누어 쓰고, 두 절의 연결 관계를
연결 어미와 의미 관계를 중심으로 설명하시오.

**제시문:** 비가 많이 와서 경기가 취소되었다.
"""
    )

    q4_split = st.text_input(
        "1. 두 절로 구분:",
        placeholder="예: 비가 많이 와서 / 경기가 취소되었다",
        key="q4_s",
    )
    q4_reason = st.text_area(
        "2. 두 절의 연결 관계 설명:",
        placeholder="연결 어미와 의미 관계를 중심으로 설명하세요.",
        key="q4_r",
    )

    if st.button("4번 문항 채점", key="btn4"):
        score = 0
        deductions = []
        passes = []

        s = normalize(q4_split)
        r = normalize(q4_reason)

        if "비가많이와서" in s and "경기가취소되었다" in s:
            score += 1
            passes.append("‘비가 많이 와서’와 ‘경기가 취소되었다’로 두 절을 정확하게 구분함")
        else:
            deductions.append(
                "절 구분: ‘비가 많이 와서’ / ‘경기가 취소되었다’로 나눌 수 있음."
            )

        if contains_any(r, ["어서", "-어서", "와서", "연결어미"]):
            score += 1
            passes.append("연결 어미 ‘-아서/-어서’를 정확하게 제시함")
        else:
            deductions.append(
                "연결 어미: 앞 절의 ‘와서’에 쓰인 연결 어미 ‘-아서/-어서’를 제시해야 함."
            )

        if contains_any(r, ["원인", "이유", "인과"]):
            score += 1
            passes.append("앞 절이 뒤 절의 원인·이유를 나타낸다는 점을 설명함")
        else:
            deductions.append(
                "의미 관계: ‘비가 많이 온 것’이 ‘경기가 취소된 것’의 원인임을 설명해야 함."
            )

        if contains_any(r, ["이어진문장", "종속", "종속적"]):
            score += 1
            passes.append("두 절이 종속적인 의미 관계로 이어짐을 설명함")
        else:
            deductions.append(
                "문장 구조: 두 절이 연결 어미로 이어진 ‘이어진 문장’이며, "
                "앞 절이 뒤 절에 종속적인 의미 관계를 이룸을 설명하면 좋음."
            )

        show_result(score, 4, passes, deductions)

    with st.expander("💡 모범 답안"):
        st.markdown(
            """
- **두 절:** ‘비가 많이 와서’ / ‘경기가 취소되었다’
- **설명:** 두 절이 연결 어미 ‘-아서/-어서’로 이어져 있으며,
  앞 절인 ‘비가 많이 와서’가 뒤 절인 ‘경기가 취소되었다’의
  원인·이유를 나타낸다. 따라서 두 절이 종속적인 의미 관계를
  이루는 **이어진 문장**이다.
"""
        )


# ============================================================
# [문항 5] 안긴절의 유형과 문법적 구실
# ============================================================
with tab5:
    st.markdown("### [문항 5] 안긴절의 유형과 문법적 구실")

    st.info(
        """
**[문제]** 다음 (가), (나), (다)의 문장에서 안긴절을 각각 찾아 쓰고,
안긴절의 종류와 전체 문장에서 담당하는 문장 성분 또는 문법적
구실을 서술하시오.

- **(가)** 선생님은 우리가 시험을 잘 치르기를 바라신다.
- **(나)** 그 나무는 잎이 푸르다.
- **(다)** 진우는 나에게 “함께 가자.”라고 말했다.
"""
    )

    q5_a = st.text_area(
        "1. (가) 안긴절, 종류, 문법적 구실:",
        placeholder="예: ‘우리가 시험을 잘 치르기’, 명사절, 목적어",
        key="q5_a",
    )
    q5_b = st.text_area(
        "2. (나) 안긴절, 종류, 문법적 구실:",
        placeholder="예: ‘잎이 푸르다’, 서술절, 서술어",
        key="q5_b",
    )
    q5_c = st.text_area(
        "3. (다) 안긴절, 종류, 문법적 구실:",
        placeholder="예: ‘함께 가자’, 인용절(직접 인용절), 부사어",
        key="q5_c",
    )

    if st.button("5번 문항 채점", key="btn5"):
        score = 0
        deductions = []
        passes = []

        a = normalize(q5_a)
        b = normalize(q5_b)
        c = normalize(q5_c)

        # (가)
        if "우리가시험을잘치르기" in a and "명사절" in a:
            score += 1
            passes.append("(가) 안긴절과 명사절을 정확하게 판단함")
        else:
            deductions.append(
                "(가): 안긴절은 ‘우리가 시험을 잘 치르기’이며 명사절임."
            )

        if "목적어" in a:
            score += 1
            passes.append("(가)에서 명사절이 목적어 역할을 함을 설명함")
        else:
            deductions.append(
                "(가): 명사절 전체가 ‘바라신다’의 목적어 역할을 함."
            )

        # (나)
        if "잎이푸르다" in b and "서술절" in b:
            score += 1
            passes.append("(나) 안긴절과 서술절을 정확하게 판단함")
        else:
            deductions.append(
                "(나): 안긴절은 ‘잎이 푸르다’이며 서술절임."
            )

        if contains_any(b, ["서술어", "서술"]) and \
           contains_any(b, ["그나무", "주어", "설명"]):
            score += 1
            passes.append("(나) 서술절이 ‘그 나무는’의 상태를 설명하는 서술어 구실을 함을 설명함")
        else:
            deductions.append(
                "(나): 서술절 ‘잎이 푸르다’가 전체 문장에서 주어인 "
                "‘그 나무는’의 상태를 설명하는 서술어 구실을 함."
            )

        # (다)
        if "함께가자" in c and "인용절" in c:
            score += 1
            passes.append("(다) ‘함께 가자’를 인용절로 정확하게 판단함")
        else:
            deductions.append(
                "(다): ‘함께 가자’는 직접 인용된 인용절임."
            )

        if contains_any(c, ["부사어", "수식"]) and \
           contains_any(c, ["말했다", "라고"]):
            score += 1
            passes.append("(다) 인용 표현 전체가 ‘말했다’를 수식하는 부사어 구실을 함을 설명함")
        else:
            deductions.append(
                "(다): 인용격 조사 ‘라고’와 결합한 인용 표현 전체가 "
                "‘말했다’를 수식하는 부사어 구실을 함."
            )

        show_result(score, 6, passes, deductions)

    with st.expander("💡 모범 답안"):
        st.markdown(
            """
- **(가)**
  - 안긴절: ‘우리가 시험을 잘 치르기’
  - 종류: **명사절**
  - 구실: 전체 문장에서 **목적어** 역할을 함.
- **(나)**
  - 안긴절: ‘잎이 푸르다’
  - 종류: **서술절**
  - 구실: 전체 문장에서 주어인 ‘그 나무는’의 상태를 설명하는
    **서술어 구실**을 함.
- **(다)**
  - 안긴절: ‘함께 가자’
  - 종류: **인용절(직접 인용절)**
  - 구실: 인용격 조사 ‘라고’와 결합한 인용 표현 전체가
    ‘말했다’를 수식하는 **부사어 구실**을 함.
"""
        )


# ============================================================
# 하단 안내
# ============================================================
st.divider()
st.caption(
    "※ 이 앱의 채점은 핵심 개념과 주요 표현을 기준으로 한 간이 채점입니다. "
    "학생 답안의 표현이 정답과 다르더라도 의미가 정확하면 교사가 최종 판단하는 것이 좋습니다."
)
