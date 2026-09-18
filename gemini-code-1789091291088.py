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
    "문제를 확인하고 답안을 입력한 후 채점하기 버튼을 누르면 "
    "채점 결과와 보완할 점을 확인할 수 있습니다."
)


# ============================================================
# 공통 함수
# ============================================================
def normalize(text):
    """채점 시 띄어쓰기를 유연하게 처리한다."""
    return re.sub(r"\s+", "", text.strip())


def contains_any(text, keywords):
    text = normalize(text)
    return any(normalize(keyword) in text for keyword in keywords)


def show_result(score, total, passes, deductions):
    st.subheader(f"💯 채점 결과: {score} / {total}점")

    if passes:
        st.success(
            "충족된 정답 요소:\n\n"
            + "\n".join(f"• {item}" for item in passes)
        )

    if deductions:
        st.warning(
            "📌 보완할 점:\n\n"
            + "\n".join(f"• {item}" for item in deductions)
        )

    if not deductions:
        st.success("모든 핵심 채점 요소가 충족되었습니다.")


# ============================================================
# 탭 구성
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "[1번] 서술어의 자릿수와 필수적 부사어",
        "[2번] 보어와 필수적 부사어",
        "[3번] 관계 관형절과 동격 관형절",
        "[4번] 이어진 문장",
        "[5번] 안긴절의 유형과 문장에서 하는 역할",
    ]
)


# ============================================================
# [문항 1]
# ============================================================
with tab1:
    st.markdown("### [문항 1] 서술어의 자릿수와 필수적 부사어")

    st.info(
        """
**[문제]** 다음 문장에서 서술어 **‘선물했다’**의 자릿수를 쓰고,
서술어가 필수적으로 요구하는 문장 성분을 찾아 그 종류와 이유를
서술하시오.

**제시문:** 지훈이가 유나에게 예쁜 꽃다발을 선물했다.
"""
    )

    q1_target = st.text_input(
        "1. 서술어의 자릿수와 필수적으로 요구되는 문장 성분:",
        placeholder="답안을 입력하세요.",
        key="q1_t",
    )

    q1_reason = st.text_area(
        "2. 해당 문장 성분이 필수적인 이유:",
        placeholder="서술어가 어떤 성분을 요구하는지 설명하세요.",
        key="q1_r",
    )

    if st.button("1번 문항 채점", key="btn1"):
        score = 0
        deductions = []
        passes = []

        target = normalize(q1_target)
        reason = normalize(q1_reason)

        if contains_any(target, ["세자리", "3자리", "세자릿수", "3자릿수"]):
            score += 1
            passes.append("‘선물했다’를 세 자리 서술어로 판단함")
        else:
            deductions.append(
                "‘선물했다’는 주어, 목적어, 선물을 받는 대상을 나타내는 "
                "성분을 요구하므로 세 자리 서술어로 봄."
            )

        if contains_any(
            target + reason,
            ["유나에게", "받는대상", "받는사람", "대상"]
        ) and contains_any(
            target + reason,
            ["부사어", "필수적부사어"]
        ):
            score += 1
            passes.append("‘유나에게’를 필수적 부사어로 제시함")
        else:
            deductions.append(
                "‘유나에게’는 부사어의 형태이지만 ‘선물했다’가 요구하는 "
                "선물을 받는 대상을 나타내는 필수적 부사어임."
            )

        if contains_any(
            reason,
            ["필수", "요구", "필요", "생략하기어렵", "생략할수없"]
        ):
            score += 1
            passes.append("해당 성분이 서술어에 의해 필수적으로 요구됨을 설명함")
        else:
            deductions.append(
                "해당 성분이 서술어에 의해 필수적으로 요구되는 성분이라는 "
                "점을 설명할 필요가 있음."
            )

        if contains_any(
            reason,
            ["받는대상", "받는사람", "대상", "누구에게", "상대"]
        ):
            score += 1
            passes.append("‘선물을 받는 대상’이라는 의미를 설명함")
        else:
            deductions.append(
                "‘유나에게’가 선물을 받는 대상을 나타낸다는 점을 설명하면 좋음."
            )

        show_result(score, 4, passes, deductions)


# ============================================================
# [문항 2]
# ============================================================
with tab2:
    st.markdown("### [문항 2] 보어와 필수적 부사어의 구별")

    st.info(
        """
**[문제]** 다음 (가), (나)의 괄호 친 문장 성분의 명칭을 각각 쓰고,
두 성분을 구별하는 기준을 **서술어와 조사의 관계를 중심으로**
설명하시오.

- **(가)** 기범이는 훌륭한 **(교사가)** 되었다.
- **(나)** 얼음이 **(물로)** 되었다.
"""
    )

    q2_names = st.text_input(
        "1. (가)와 (나)의 문장 성분 명칭:",
        placeholder="답안을 입력하세요.",
        key="q2_n",
    )

    q2_reason = st.text_area(
        "2. 두 성분을 구별하는 기준:",
        placeholder="서술어와 조사의 관계를 중심으로 설명하세요.",
        key="q2_r",
    )

    if st.button("2번 문항 채점", key="btn2"):
        score = 0
        deductions = []
        passes = []

        names = normalize(q2_names)
        reason = normalize(q2_reason)

        if "보어" in names and contains_any(
            names, ["부사어", "필수적부사어"]
        ):
            score += 2
            passes.append("(가)는 보어, (나)는 필수적 부사어라고 판단함")
        else:
            deductions.append(
                "(가)의 ‘교사가’는 보어이고, (나)의 ‘물로’는 필수적 부사어임."
            )

        if contains_any(reason, ["되다", "아니다", "서술어"]) and \
           contains_any(reason, ["필수", "요구"]):
            score += 1
            passes.append("서술어가 요구하는 성분이라는 점을 설명함")
        else:
            deductions.append(
                "보어는 ‘되다’, ‘아니다’와 같은 서술어가 요구하는 성분이라는 "
                "점을 설명할 필요가 있음."
            )

        if contains_any(reason, ["보격조사", "이/가", "이가"]) and \
           contains_any(reason, ["부사격조사", "로", "으로"]):
            score += 1
            passes.append("보격 조사 ‘이/가’와 부사격 조사 ‘로/으로’의 차이를 설명함")
        else:
            deductions.append(
                "(가)의 ‘교사가’에는 보격 조사 ‘이/가’가, (나)의 ‘물로’에는 "
                "부사격 조사 ‘로’가 결합한다는 점을 설명해야 함."
            )

        show_result(score, 4, passes, deductions)


# ============================================================
# [문항 3]
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
        placeholder="답안을 입력하세요.",
        key="q3_g",
    )

    q3_na = st.text_input(
        "2. (나) 관형절과 유형:",
        placeholder="답안을 입력하세요.",
        key="q3_n",
    )

    q3_diff = st.text_area(
        "3. 두 관형절의 구조적 차이:",
        placeholder="관형절 내부의 생략된 성분을 중심으로 설명하세요.",
        key="q3_d",
    )

    if st.button("3번 문항 채점", key="btn3"):
        score = 0
        deductions = []
        passes = []

        ga = normalize(q3_ga)
        na = normalize(q3_na)
        diff = normalize(q3_diff)

        if "동생이만든" in ga and "관계" in ga:
            score += 2
            passes.append("(가) ‘동생이 만든’ / 관계 관형절을 정확하게 판단함")
        else:
            deductions.append(
                "(가)의 관형절은 ‘동생이 만든’이며 관계 관형절임."
            )

        if "우리가우승했다는" in na and "동격" in na:
            score += 2
            passes.append("(나) ‘우리가 우승했다는’ / 동격 관형절을 정확하게 판단함")
        else:
            deductions.append(
                "(나)의 관형절은 ‘우리가 우승했다는’이며 동격 관형절임."
            )

        if contains_any(
            diff,
            ["목적어", "케이크", "생략", "생략됨", "빠진"]
        ):
            score += 1
            passes.append(
                "(가)에서 ‘케이크’가 관형절 내부의 목적어에 대응함을 설명함"
            )
        else:
            deductions.append(
                "(가)는 ‘동생이 케이크를 만들었다’에서 ‘케이크를’이 "
                "관형절 내부의 목적어에 대응하여 생략된 구조임."
            )

        if contains_any(
            diff,
            ["없", "생략된성분이없", "빠진성분이없", "내용", "소문"]
        ):
            score += 1
            passes.append(
                "(나)에서 관형절 전체가 ‘소문’의 내용을 나타냄을 설명함"
            )
        else:
            deductions.append(
                "(나)는 ‘우리가 우승했다’라는 절 전체가 ‘소문’의 내용을 "
                "나타내므로 관형절 내부에 대응하여 생략된 성분이 없음."
            )

        show_result(score, 6, passes, deductions)


# ============================================================
# [문항 4]
# ============================================================
with tab4:
    st.markdown("### [문항 4] 이어진 문장의 의미 관계")

    st.info(
        """
**[문제]** 다음 문장을 두 절로 나누어 쓰고, 두 절의 연결 관계를
**연결 어미와 의미 관계를 중심으로 설명하시오.**

**제시문:** 비가 많이 와서 경기가 취소되었다.
"""
    )

    q4_split = st.text_input(
        "1. 두 절로 구분:",
        placeholder="답안을 입력하세요.",
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

        split = normalize(q4_split)
        reason = normalize(q4_reason)

        if "비가많이와서" in split and "경기가취소되었다" in split:
            score += 1
            passes.append(
                "‘비가 많이 와서’와 ‘경기가 취소되었다’로 두 절을 정확하게 구분함"
            )
        else:
            deductions.append(
                "두 절은 ‘비가 많이 와서’ / ‘경기가 취소되었다’로 나눌 수 있음."
            )

        if contains_any(reason, ["-아서", "-어서", "아서", "어서", "와서"]):
            score += 1
            passes.append("연결 어미 ‘-아서/-어서’를 정확하게 제시함")
        else:
            deductions.append(
                "두 절을 연결하는 연결 어미 ‘-아서/-어서’를 제시해야 함."
            )

        if contains_any(reason, ["원인", "이유", "인과"]):
            score += 1
            passes.append("앞 절이 뒤 절의 원인·이유를 나타냄을 설명함")
        else:
            deductions.append(
                "‘비가 많이 온 것’이 ‘경기가 취소된 것’의 원인이라는 "
                "의미 관계를 설명해야 함."
            )

        if contains_any(reason, ["종속", "종속적", "이어진문장"]):
            score += 1
            passes.append("두 절이 종속적인 의미 관계로 이어짐을 설명함")
        else:
            deductions.append(
                "두 절이 연결 어미로 이어진 ‘이어진 문장’이며, "
                "앞 절이 뒤 절에 종속적인 의미 관계를 이룸을 설명하면 좋음."
            )

        show_result(score, 4, passes, deductions)


# ============================================================
# [문항 5]
# ============================================================
with tab5:
    st.markdown("### [문항 5] 안긴절의 유형과 문장에서 하는 역할")

    st.info(
        """
**[문제]** 다음 (가), (나), (다)의 문장에서 안긴절을 각각 찾아 쓰고,
안긴절의 종류와 **전체 문장에서 하는 역할을 구체적으로 설명하시오.**

- **(가)** 선생님은 우리가 시험을 잘 치르기를 바라신다.
- **(나)** 그 나무는 잎이 푸르다.
- **(다)** 진우는 나에게 “함께 가자.”라고 말했다.
"""
    )

    q5_a = st.text_area(
        "1. (가) 안긴절, 종류, 문장에서 하는 역할:",
        placeholder="답안을 입력하세요.",
        key="q5_a",
    )

    q5_b = st.text_area(
        "2. (나) 안긴절, 종류, 문장에서 하는 역할:",
        placeholder="답안을 입력하세요.",
        key="q5_b",
    )

    q5_c = st.text_area(
        "3. (다) 안긴절, 종류, 문장에서 하는 역할:",
        placeholder="답안을 입력하세요.",
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
            passes.append("(가) ‘우리가 시험을 잘 치르기’와 명사절을 정확하게 판단함")
        else:
            deductions.append(
                "(가)의 안긴절은 ‘우리가 시험을 잘 치르기’이며 명사절임."
            )

        if "목적어" in a:
            score += 1
            passes.append("(가)에서 명사절이 목적어 역할을 함을 설명함")
        else:
            deductions.append(
                "(가)의 명사절은 전체 문장에서 ‘바라신다’의 목적어 역할을 함."
            )

        # (나)
        if "잎이푸르다" in b and "서술절" in b:
            score += 1
            passes.append("(나) ‘잎이 푸르다’와 서술절을 정확하게 판단함")
        else:
            deductions.append(
                "(나)의 안긴절은 ‘잎이 푸르다’이며 서술절임."
            )

        if contains_any(b, ["서술어", "서술"]) and \
           contains_any(b, ["그나무", "주어", "설명"]):
            score += 1
            passes.append(
                "(나)에서 서술절이 ‘그 나무는’의 상태를 설명하는 역할을 함을 설명함"
            )
        else:
            deductions.append(
                "(나)의 서술절 ‘잎이 푸르다’는 전체 문장에서 주어인 "
                "‘그 나무는’의 상태를 설명하는 서술어 역할을 함."
            )

        # (다)
        if "함께가자" in c and "인용절" in c:
            score += 1
            passes.append("(다) ‘함께 가자’를 인용절로 정확하게 판단함")
        else:
            deductions.append(
                "(다)의 안긴절은 ‘함께 가자’이며 직접 인용한 인용절임."
            )

        if contains_any(c, ["부사어", "수식"]) and \
           contains_any(c, ["말했다", "라고"]):
            score += 1
            passes.append(
                "(다) 인용 표현이 ‘말했다’를 수식하는 역할을 함을 설명함"
            )
        else:
            deductions.append(
                "(다)는 인용격 조사 ‘라고’와 결합한 인용 표현 전체가 "
                "‘말했다’를 수식하는 부사어 역할을 함."
            )

        show_result(score, 6, passes, deductions)


# ============================================================
# 하단 안내
# ============================================================
st.divider()
st.caption(
    "※ 채점 결과는 학생 답안의 핵심 개념과 주요 표현을 기준으로 한 간이 채점입니다. "
    "표현이 모범 답안과 다르더라도 문법적 의미가 정확한 경우에는 교사가 최종 판단할 수 있습니다."
)
