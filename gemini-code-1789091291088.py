import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="문장 성분과 문장 구조 서술형 평가 채점 시스템", layout="wide"
)

st.title("📝 문장 성분 및 문장 구조 서술형 평가 채점 시스템")
st.caption(
    "문제를 확인하고 답안을 입력한 후 '채점하기' 버튼을 누르면 실시간 피드백과 모범 답안이 제공됩니다."
)


# 의미 포함 여부 검증용 헬퍼 함수
def contains_any(text, keywords):
    return any(kw in text for kw in keywords)


# 탭 구성 (1번 ~ 5번 문항)
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "[1번] 서술어 자릿수 및 필수 부사어",
        "[2번] 보어와 필수 부사어 구별",
        "[3번] 관계/동격 관형절 비교",
        "[4번] 종속적으로 이어진 문장",
        "[5번] 안긴절의 유형과 문법적 구실",
    ]
)

# ====================================================
# [문항 1] 서술어 자릿수와 필수적 부사어
# ====================================================
with tab1:
    st.markdown("### [문항 1] 서술어의 자릿수와 필수적 부사어 판별")

    st.info(
        """
    **[문제]** 다음 문장을 바탕으로 서술어 '선물했다'의 자릿수를 제시하고, 이 문장에서 생략하기 어려운 문장 성분이 있다면 해당 부분을 찾아 쓰고 그 이유를 서술하시오.
    
    * **제시문:** 지훈이가 유나에게 아름다운 꽃다발을 선물했다.
    """
    )

    q1_target = st.text_input(
        "1. 서술어 자릿수 및 생략하기 어려운 문장 성분 명칭:",
        placeholder="답안을 입력하세요.",
        key="q1_t",
    )
    q1_reason = st.text_area(
        "2. 해당 문장 성분을 생략할 수 없는 이유 서술:",
        placeholder="답안을 입력하세요.",
        key="q1_r",
    )

    if st.button("1번 문항 채점", key="btn1"):
        score = 0
        deductions = []
        passes = []

        # 1. 자릿수 채점 (세 자리 / 3자리 / 3개 성분)
        if contains_any(q1_target, ["세 자리", "3자리", "세자릿수", "3개"]):
            score += 1
            passes.append("서술어 자릿수 정확히 제시 (세 자리 서술어)")
        else:
            deductions.append(
                "자릿수 오류: '선물했다'는 3개의 문장 성분을 필수적으로 요구하는 '세 자리 서술어'입니다."
            )

        # 2. 필수 성분 추출 ('유나에게')
        if "유나에게" in q1_target or "유나에게" in q1_reason:
            score += 1
            passes.append("생략하기 어려운 성분 정확히 추출 ('유나에게')")
        else:
            deductions.append(
                "성분 추출 오류: 부사어 형태를 띠며 생략할 수 없는 성명은 '유나에게'입니다."
            )

        # 3. 필수적 부사어 성격 및 이유 설명 (의미 포함 허용 및 오개념 검증)
        has_essential_concept = contains_any(
            q1_reason, ["필수", "꼭", "반드시", "없으면 안"]
        )
        has_target_concept = contains_any(
            q1_reason, ["받는", "대상", "상대", "누구에게", "주체 외"]
        )
        has_vague_error = (
            "비문" in q1_reason or "문장이 안 된다" in q1_reason
        ) and not has_target_concept

        if has_essential_concept and has_target_concept:
            score += 2
            passes.append(
                "필수적 부사어의 성격 및 서술어가 요구하는 구체적 이유(선물을 받는 대상) 서술 완비"
            )
        else:
            if not has_essential_concept:
                deductions.append(
                    "성격 설명 부족: 부사어 형태이지만 생략할 수 없는 '필수적 부사어'임을 명시해야 합니다."
                )
            if not has_target_concept or has_vague_error:
                deductions.append(
                    "근거 제시 미흡: 단순히 '생략하면 비문이 된다'에 그치지 않고, 서술어 '선물했다'가 주어·목적어 외에 '선물을 받는 대상'을 요구한다는 점을 서술해야 합니다."
                )

        st.subheader(f"💯 채점 결과: {score} / 4점")
        if passes:
            st.success("충족된 정답 요건:\n\n" + "\n".join([f"• {p}" for p in passes]))
        if deductions:
            st.error(
                "📌 감점 요인 발견:\n\n"
                + "\n".join([f"• {d}" for d in deductions])
            )

        with st.expander("💡 선택지별 모범 답안 보기"):
            st.markdown(
                """
            * **서술어 자릿수:** 세 자리 서술어
            * **생략하기 어려운 성분:** '유나에게' (필수적 부사어)
            * **이유:** '유나에게'는 부사어의 형태를 띠지만 생략하면 문장의 의미가 불완전해지므로 필수적 부사어이다. 서술어 '선물했다'는 주어('지훈이가'), 목적어('꽃다발을') 외에 선물을 받는 대상을 나타내는 성분('유나에게')을 필수적으로 요구한다.
            """
            )


# ====================================================
# [문항 2] 보어와 필수적 부사어의 구별
# ====================================================
with tab2:
    st.markdown("### [문항 2] 보어와 필수적 부사어의 구별")

    st.info(
        """
    **[문제]** 다음 (가), (나)의 괄호 친 문장 성분의 명칭을 각각 쓰고, 두 성분을 구별하는 문법적 기준을 서술하시오.
    
    * (가) 기범이는 훌륭한 (교사가) 되었다.
    * (나) 얼음이 (물로) 되었다.
    """
    )

    q2_names = st.text_input(
        "1. (가)와 (나)의 밑줄 친 문장 성분 명칭:",
        placeholder="답안을 입력하세요.",
        key="q2_n",
    )
    q2_reason = st.text_area(
        "2. 두 성분을 구별하는 문법적 기준 서술:",
        placeholder="답안을 입력하세요.",
        key="q2_r",
    )

    if st.button("2번 문항 채점", key="btn2"):
        score = 0
        deductions = []
        passes = []

        # 1. 성분 명칭 구분
        ga_correct = "보어" in q2_names
        na_correct = contains_any(q2_names, ["부사어", "필수적 부사어"])

        if ga_correct and na_correct:
            score += 2
            passes.append("성분 명칭 정확히 명시 ((가) 보어, (나) 필수적 부사어)")
        else:
            deductions.append(
                "성분 명칭 오류: (가)는 보어, (나)는 필수적 부사어(부사어)입니다."
            )

        # 2. 오개념 검증 및 구별 기준 채점
        has_predicate_condition = contains_any(
            q2_reason, ["되다", "아니다", "되었다"]
        )
        has_ga_josa = contains_any(q2_reason, ["이/가", "이", "가", "보격"])
        has_na_josa = contains_any(q2_reason, ["로", "으로", "부사격"])

        misconception_water_as_complement = "물로가 보어" in q2_reason

        if (
            has_predicate_condition
            and has_ga_josa
            and has_na_josa
            and not misconception_water_as_complement
        ):
            score += 2
            passes.append(
                "서술어 조건('되다/아니다') 및 조사 결합 차이(보격조사 '이/가' vs 부사격조사 '로') 정확히 설명"
            )
        else:
            if misconception_water_as_complement:
                deductions.append(
                    "오개념 발견: (나)의 '물로'는 서술어 '되다'의 필수 성분이지만 보격 조사가 아니므로 보어가 될 수 없습니다."
                )
            if not has_predicate_condition:
                deductions.append(
                    "기준 서술 미흡: 보어는 서술어 '되다', '아니다' 앞에 위치한다는 서술어 조건이 언급되어야 합니다."
                )
            if not (has_ga_josa and has_na_josa):
                deductions.append(
                    "조사 차이 누락: (가) '교사가'에는 보격 조사 '이/가'가, (나) '물로'에는 부사격 조사 '로'가 결합했다는 조사의 차이를 서술해야 합니다."
                )

        st.subheader(f"💯 채점 결과: {score} / 4점")
        if passes:
            st.success("충족된 정답 요건:\n\n" + "\n".join([f"• {p}" for p in passes]))
        if deductions:
            st.error(
                "📌 감점 요인 발견:\n\n"
                + "\n".join([f"• {d}" for d in deductions])
            )

        with st.expander("💡 선택지별 모범 답안 보기"):
            st.markdown(
                """
            * **(가) 성분 명칭:** 보어
            * **(나) 성분 명칭:** 필수적 부사어
            * **구별 기준:** 보어는 서술어 '되다/아니다'가 필수적으로 요구하는 성분 중 보격 조사 '이/가'가 결합한 성분이다. 따라서 (가)의 '교사가'는 보격 조사가 결합한 보어이다. 반면 (나)의 '물로'는 서술어 '되었다'가 요구하지만 부사격 조사 '로'가 결합하였으므로 필수적 부사어이다.
            """
            )


# ====================================================
# [문항 3] 관계 관형절과 동격 관형절
# ====================================================
with tab3:
    st.markdown("### [문항 3] 관계 관형절과 동격 관형절의 구조적 차이")

    st.info(
        """
    **[문제]** 다음 (가), (나)의 문장에 안겨 있는 관형절을 각각 찾아 쓰고, 관계 관형절과 동격 관형절 중 어느 것인지 밝히시오. 또한 관형절 내부에서 생략된 문장 성분의 유무를 중심으로 두 관형절의 구조적 차이를 설명하시오.
    
    * (가) 동생이 만든 케이크는 정말 달콤했다.
    * (나) 우리가 우승했다는 소문이 학교에 퍼졌다.
    """
    )

    q3_ga = st.text_input(
        "1. (가) 안긴 관형절 및 유형:",
        placeholder="답안을 입력하세요.",
        key="q3_g",
    )
    q3_na = st.text_input(
        "2. (나) 안긴 관형절 및 유형:",
        placeholder="답안을 입력하세요.",
        key="q3_n",
    )
    q3_diff = st.text_area(
        "3. 생략된 성분 유무를 중심으로 한 구조적 차이 설명:",
        placeholder="답안을 입력하세요.",
        key="q3_d",
    )

    if st.button("3번 문항 채점", key="btn3"):
        score = 0
        deductions = []
        passes = []

        # 1. (가) 추출 및 유형
        if "동생이 만든" in q3_ga and "관계" in q3_ga:
            score += 2
            passes.append("(가) 관형절('동생이 만든') 및 유형(관계 관형절) 정확함")
        else:
            deductions.append(
                "(가) 오류: 관형절은 '동생이 만든'이며, 관계 관형절입니다."
            )

        # 2. (나) 추출 및 유형
        if "우리가 우승했다는" in q3_na and "동격" in q3_na:
            score += 2
            passes.append(
                "(나) 관형절('우리가 우승했다는') 및 유형(동격 관형절) 정확함"
            )
        else:
            deductions.append(
                "(나) 오류: 관형절은 '우리가 우승했다는'이며, 동격 관형절입니다."
            )

        # 3. 구조적 차이 (생략 유무 및 성분 제시)
        has_ga_deleted = contains_any(
            q3_diff, ["목적어", "케이크", "생략", "빠진"]
        )
        has_na_no_deleted = contains_any(
            q3_diff, ["생략된 성분이 없", "빠진 것이 없", "내용", "동일"]
        )

        if has_ga_deleted and has_na_no_deleted:
            score += 2
            passes.append(
                "구조적 차이 명확히 제시 ((가) 목적어 생략 vs (나) 생략된 성분 없음)"
            )
        else:
            if not has_ga_deleted:
                deductions.append(
                    "(가) 설명 부족: 수식받는 '케이크'가 관형절 내에서 목적어 역할을 하여 생략되었음을 기술해야 합니다."
                )
            if not has_na_no_deleted:
                deductions.append(
                    "(나) 설명 부족: 절 전체가 '소문'의 내용 자체이며 관형절 내부에 생략된 성분이 없음을 기술해야 합니다."
                )

        st.subheader(f"💯 채점 결과: {score} / 6점")
        if passes:
            st.success("충족된 정답 요건:\n\n" + "\n".join([f"• {p}" for p in passes]))
        if deductions:
            st.error(
                "📌 감점 요인 발견:\n\n"
                + "\n".join([f"• {d}" for d in deductions])
            )

        with st.expander("💡 선택지별 모범 답안 보기"):
            st.markdown(
                """
            * **(가) 관형절 및 유형:** '동생이 만든' / 관계 관형절
            * **(가) 구조 설명:** 관형절이 수식하는 '케이크'가 관형절 내부에서 목적어 역할을 하므로, '동생이 케이크를 만들었다'에서 목적어('케이크를')가 생략되어 있다.
            * **(나) 관형절 및 유형:** '우리가 우승했다는' / 동격 관형절
            * **(나) 구조 설명:** '우리가 우승했다'라는 절 전체가 '소문'의 내용을 나타내며, 관형절 내부에서 수식을 받는 체언과 대응하여 생략된 문장 성분이 없다.
            """
            )


# ====================================================
# [문항 4] 종속적으로 이어진 문장
# ====================================================
with tab4:
    st.markdown("### [문항 4] 종속적으로 이어진 문장의 의미 관계")

    st.info(
        """
    **[문제]** 다음 문장을 두 절로 나누어 쓰고, 두 절이 종속적으로 이어진 문장인 이유를 연결 어미와 의미 관계를 중심으로 서술하시오.
    
    * **제시문:** 날씨가 추워서 나는 외투를 입었다.
    """
    )

    q4_split = st.text_input(
        "1. 두 절로 구분:",
        placeholder="답안을 입력하세요.",
        key="q4_s",
    )
    q4_reason = st.text_area(
        "2. 종속적으로 이어진 문장인 이유 서술 (연결 어미 및 의미 관계):",
        placeholder="답안을 입력하세요.",
        key="q4_r",
    )

    if st.button("4번 문항 채점", key="btn4"):
        score = 0
        deductions = []
        passes = []

        # 1. 절의 구분
        if "날씨가 추워서" in q4_split and "나는 외투를 입었다" in q4_split:
            score += 1
            passes.append("두 절 정확히 구분 ('날씨가 추워서' / '나는 외투를 입었다')")
        else:
            deductions.append(
                "절 구분 오류: '날씨가 추워서'와 '나는 외투를 입었다'로 나뉘어야 합니다."
            )

        # 2. 연결 어미 명시
        has_eomi = contains_any(q4_reason, ["-어서", "어서"])
        if has_eomi:
            score += 1
            passes.append("연결 어미('-어서') 정확히 명시")
        else:
            deductions.append(
                "연결 어미 누락: 두 절을 연결하는 어미 '-어서'를 제시해야 합니다."
            )

        # 3. 의미 관계 및 종속성
        has_cause = contains_any(q4_reason, ["원인", "인과", "이유", "결과"])
        has_subordinate = contains_any(
            q4_reason, ["종속", "독립적이지", "주속"]
        )

        if has_cause:
            score += 1
            passes.append("의미 관계(원인과 결과/인과) 정확히 제시")
        else:
            deductions.append(
                "의미 관계 누락: 앞 절이 뒤 절의 '원인(이유)'이 됨을 설명해야 합니다."
            )

        if has_subordinate or has_cause:
            score += 1
            passes.append("종속적 연결 관계 판단 타당함")
        else:
            deductions.append(
                "판단 설명 미흡: 두 절이 대등하지 않고 종속적인 관계임을 서술해야 합니다."
            )

        st.subheader(f"💯 채점 결과: {score} / 4점")
        if passes:
            st.success("충족된 정답 요건:\n\n" + "\n".join([f"• {p}" for p in passes]))
        if deductions:
            st.error(
                "📌 감점 요인 발견:\n\n"
                + "\n".join([f"• {d}" for d in deductions])
            )

        with st.expander("💡 선택지별 모범 답안 보기"):
            st.markdown(
                """
            * **절의 구분:** '날씨가 추워서' / '나는 외투를 입었다'
            * **종속적으로 이어진 문장인 이유:** 두 절이 연결 어미 '-어서'에 의해 연결되어 있으며, 앞 절('날씨가 추워서')은 뒤 절('나는 외투를 입었다')이 일어난 원인(이유)을 나타내므로 종속적으로 이어진 문장이다.
            """
            )


# ====================================================
# [문항 5] 안긴절의 유형과 문법적 구실
# ====================================================
with tab5:
    st.markdown("### [문항 5] 안긴절의 유형과 문법적 구실")

    st.info(
        """
    **[문제]** 다음 (가), (나), (다)의 문장에 안겨 있는 절을 각각 찾아 쓰고, 안긴절의 종류와 전체 문장에서 담당하는 문장 성분 또는 문법적 구실을 서술하시오.
    
    * (가) 선생님은 우리가 시험을 잘 치르기를 바라신다.
    * (나) 그 나무는 잎이 푸르다.
    * (다) 진우는 나에게 "함께 가자."라고 말했다.
    """
    )

    q5_a = st.text_area(
        "1. (가) 안긴절, 종류, 문법적 구실:",
        placeholder="답안을 입력하세요.",
        key="q5_a",
    )
    q5_b = st.text_area(
        "2. (나) 안긴절, 종류, 문법적 구실:",
        placeholder="답안을 입력하세요.",
        key="q5_b",
    )
    q5_c = st.text_area(
        "3. (다) 안긴절, 종류, 문법적 구실:",
        placeholder="답안을 입력하세요.",
        key="q5_c",
    )

    if st.button("5번 문항 채점", key="btn5"):
        score = 0
        deductions = []
        passes = []

        # 1. (가) 채점 (우리가 시험을 잘 치르기 / 명사절 / 목적어)
        if (
            "우리가 시험을 잘 치르기" in q5_a
            and "명사절" in q5_a
            and "목적어" in q5_a
        ):
            score += 2
            passes.append("(가) 분석 완벽 (안긴절: '우리가 시험을 잘 치르기', 명사절, 목적어 역할)")
        else:
            deductions.append(
                "(가) 오류: 안긴절은 '우리가 시험을 잘 치르기'이며, 명사형 어미 '-기'가 결합한 명사절로서 목적어 역할을 합니다."
            )

        # 2. (나) 채점 (잎이 푸르다 / 서술절 / 서술어)
        if "잎이 푸르다" in q5_b and "서술절" in q5_b and "서술어" in q5_b:
            score += 2
            passes.append("(나) 분석 완벽 (안긴절: '잎이 푸르다', 서술절, 서술어 역할)")
        else:
            deductions.append(
                "(나) 오류: 안긴절은 '잎이 푸르다'이며, 서술절로서 전체 문장의 서술어 역할을 합니다."
            )

        # 3. (다) 채점 ("함께 가자." / 직접 인용절 / 부사어 또는 말했다 수식)
        if (
            "함께 가자" in q5_c
            and "인용" in q5_c
            and ("부사어" in q5_c or "수식" in q5_c)
        ):
            score += 2
            passes.append(
                "(다) 분석 완벽 (안긴절: '함께 가자.', 직접 인용절, 부사어 역할)"
            )
        else:
            deductions.append(
                "(다) 오류: 안긴절은 '함께 가자.'이며, 직접 인용절로서 인용격 조사 '라고'와 함께 서술어를 수식하는 부사어 역할을 합니다."
            )

        st.subheader(f"💯 채점 결과: {score} / 6점")
        if passes:
            st.success("충족된 정답 요건:\n\n" + "\n".join([f"• {p}" for p in passes]))
        if deductions:
            st.error(
                "📌 감점 요인 발견:\n\n"
                + "\n".join([f"• {d}" for d in deductions])
            )

        with st.expander("💡 선택지별 모범 답안 보기"):
            st.markdown(
                """
            * **(가)**
              * **안긴절:** '우리가 시험을 잘 치르기'
              * **종류:** 명사절
              * **구실:** 명사형 어미 '-기'가 결합한 명사절로, 목적격 조사 '를'과 결합하여 전체 문장에서 목적어 역할을 한다.
            * **(나)**
              * **안긴절:** '잎이 푸르다'
              * **종류:** 서술절
              * **구실:** 전체 문장에서 주어('그 나무는')를 설명하는 서술어 역할을 한다.
            * **(다)**
              * **안긴절:** "함께 가자."
              * **종류:** 직접 인용절
              * **구실:** 인용격 조사 '라고'와 결합한 인용 표현 전체가 '말했다'를 수식하는 부사어 역할을 한다.
            """
            )
