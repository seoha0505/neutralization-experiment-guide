import streamlit as st

st.title("🧪 중화반응 실험 가이드")

# 1. 세션 상태 초기화
if "acid" not in st.session_state:
    st.session_state.acid = []   # [1mL당 이온수, 부피]
if "basic" not in st.session_state:
    st.session_state.basic = []  # [1mL당 이온수, 부피]
if "first_choice" not in st.session_state:
    st.session_state.first_choice = None

# 2. 드롭다운 및 입력 UI
solution_type = st.selectbox("용액의 종류를 선택하세요", ["산성", "염기성"])

col1, col2 = st.columns(2)
with col1:
    ion_per_ml = st.number_input("1mL당 이온 수 (개/mL)", value=0.0, step=1.0)
with col2:
    volume = st.number_input("용액의 부피 (mL)", value=0.0, step=1.0)

# 데이터 저장 버튼
if st.button("용액 데이터 저장"):
    while ion_per_ml <= 0 or volume <= 0:
        st.error("⚠️ 이온 수와 부피는 0보다 커야 합니다. 값을 다시 입력해 주세요.")
        st.stop()
        break

    if st.session_state.first_choice is None:
        st.session_state.first_choice = solution_type

    if solution_type == "산성":
        st.session_state.acid = [ion_per_ml, volume]
        st.success(f"산성 용액 저장 완료: 1mL당 {ion_per_ml}개, 부피 {volume}mL")
    else:
        st.session_state.basic = [ion_per_ml, volume]
        st.success(f"염기성 용액 저장 완료: 1mL당 {ion_per_ml}개, 부피 {volume}mL")

# 초기화 버튼 추가 (새 실험 시 편리함)
if st.button("🔄 실험 데이터 초기화"):
    st.session_state.acid = []
    st.session_state.basic = []
    st.session_state.first_choice = None
    st.rerun()

st.write("---")
st.write(f"**처음 선택한 용액:** {st.session_state.first_choice}")
st.write(f"**산성 리스트 (`acid`):** {st.session_state.acid}")
st.write(f"**염기성 리스트 (`basic`):** {st.session_state.basic}")


# 3. 수정된 중화반응 계산 함수
def check_react(acid_ion=None, acid_volume=None, basic_ion=None, basic_volume=None):
    # 저장된 두 용액의 정보 모두 불러오기
    a_ion = float(st.session_state.acid[0])
    a_vol = float(st.session_state.acid[1])
    b_ion = float(st.session_state.basic[0])
    b_vol = float(st.session_state.basic[1])

    # 총 이온 수 계산 (소수점 오차 방지를 위해 round 사용)
    total_acid = round(a_ion * a_vol, 2)
    total_basic = round(b_ion * b_vol, 2)

    st.subheader("📊 실험 분석 결과")
    st.write(f"- 산성 총 이온 수: **{total_acid}**개 (`{a_ion}` × `{a_vol}ml`)")
    st.write(f"- 염기성 총 이온 수: **{total_basic}**개 (`{b_ion}` × `{b_vol}ml`)")
    st.write("---")

    # 1) 산성 이온이 더 많은 경우 -> 현재 용액은 <<산성>> -> 염기성 용액을 더 넣어야 함
    if total_acid > total_basic:
        st.write("현재 용액은 **<<산성>>**입니다.")
        
        added_vol = 0.0
        # while문으로 염기 이온 총합이 산성 이온 총합과 같아질 때까지 0.1ml씩 추가
        while round(b_ion * (b_vol + added_vol), 2) < total_acid:
            added_vol = round(added_vol + 0.1, 1)
            
        st.info(f"중화반응이 일어나기 위해서는 1ml당 이온 수가 {int(b_ion)}개인 염기성용액이 **{added_vol}ml** 더 필요합니다.")

    # 2) 염기성 이온이 더 많은 경우 -> 현재 용액은 <<염기성>> -> 산성 용액을 더 넣어야 함
    elif total_basic > total_acid:
        st.write("현재 용액은 **<<염기성>>**입니다.")
        
        added_vol = 0.0
        # while문으로 산성 이온 총합이 염기성 이온 총합과 같아질 때까지 0.1ml씩 추가
        while round(a_ion * (a_vol + added_vol), 2) < total_basic:
            added_vol = round(added_vol + 0.1, 1)
            
        st.info(f"중화반응이 일어나기 위해서는 1ml당 이온 수가 {int(a_ion)}개인 산성용액이 **{added_vol}ml** 더 필요합니다.")

    # 3) 두 이온 수가 같은 경우 -> 현재 용액은 <<중성>>
    else:
        st.write("현재 용액은 **<<중성>>**입니다.")
        st.success("산성과 염기성의 이온 수가 같으므로 완벽한 **중화반응**이 일어납니다. (추가 계산 없음)")


# 4. 실험 시작 버튼
if st.button("🚀 실험 시작"):
    if not st.session_state.acid or not st.session_state.basic:
        st.error("⚠️ 산성과 염기성 리스트가 모두 채워져야 합니다!")
    else:
        all_values = st.session_state.acid + st.session_state.basic
        for val in all_values:
            while val <= 0:
                st.error("⚠️ 0보다 작거나 같은 값이 포함되어 있습니다. 다시 입력해 주세요.")
                st.stop()
                break

        acid_ion = float(st.session_state.acid[0])
        acid_volume = float(st.session_state.acid[1])
        basic_ion = float(st.session_state.basic[0])
        basic_volume = float(st.session_state.basic[1])

        if st.session_state.first_choice == "산성":
            check_react(acid_ion=acid_ion, acid_volume=acid_volume)
        else:
            check_react(basic_ion=basic_ion, basic_volume=basic_volume)
