import streamlit as st

st.title("🧪 중화반응 실험 가이드")

# 1. 세션 상태 초기화
if "acid" not in st.session_state:
    st.session_state.acid = []   # [1mL당 이온수, 부피]
if "basic" not in st.session_state:
    st.session_state.basic = []  # [1mL당 이온수, 부피]
if "first_choice" not in st.session_state:
    st.session_state.first_choice = None  # 사용자가 처음 선택한 용액 저장

# 2. 드롭다운 및 입력 UI
solution_type = st.selectbox("용액의 종류를 선택하세요", ["산성", "염기성"])

col1, col2 = st.columns(2)
with col1:
    ion_per_ml = st.number_input("1mL당 이온 수 (개/mL)", value=0.0, step=1.0)
with col2:
    volume = st.number_input("용액의 부피 (mL)", value=0.0, step=1.0)

# 데이터 저장 버튼
if st.button("용액 데이터 저장"):
    # while문을 활용한 입력값 검증 (0 이하일 경우 break로 빠져나오며 경고)
    while ion_per_ml <= 0 or volume <= 0:
        st.error("⚠️ 이온 수와 부피는 0보다 커야 합니다. 값을 다시 입력해 주세요.")
        st.stop()
        break

    # 사용자가 '처음'으로 저장한 용액 기록
    if st.session_state.first_choice is None:
        st.session_state.first_choice = solution_type

    if solution_type == "산성":
        st.session_state.acid = [ion_per_ml, volume]
        st.success(f"산성 용액 저장 완료: 1mL당 {ion_per_ml}개, 부피 {volume}mL")
    else:
        st.session_state.basic = [ion_per_ml, volume]
        st.success(f"염기성 용액 저장 완료: 1mL당 {ion_per_ml}개, 부피 {volume}mL")

# 저장된 상태 확인
st.write("---")
st.write(f"**처음 선택한 용액:** {st.session_state.first_choice}")
st.write(f"**산성 리스트 (`acid`):** {st.session_state.acid}")
st.write(f"**염기성 리스트 (`basic`):** {st.session_state.basic}")


# 3. 중화반응 계산 함수 정의
# 파이썬에서 같은 이름의 함수를 두 번 정의하면 덮어쓰기 되므로,
# 인자(acid_ion, acid_volume 또는 basic_ion, basic_volume)에 따라 분기하도록 구현했습니다.
def check_react(acid_ion=None, acid_volume=None, basic_ion=None, basic_volume=None):
    first_selected = st.session_state.first_choice
    
    # [경우 A] 산성의 이온 수와 부피를 입력받아 -> 필요한 염기성 용액의 부피 계산
    if acid_ion is not None and acid_volume is not None:
        b_ion_per_ml = st.session_state.basic[0]
        b_vol = st.session_state.basic[1]
        
        total_acid = acid_ion * acid_volume
        total_basic = b_ion_per_ml * b_vol
        
        st.subheader("📊 실험 결과 (염기성 용액 기준 계산)")
        st.write(f"현재 용액은 **<<{first_selected}>>**입니다.")
        
        if total_basic > total_acid:
            # while문을 이용해 염기 이온과 산성 이온이 같아질 때까지 부피 감소 계산
            temp_vol = b_vol
            while (b_ion_per_ml * temp_vol) > total_acid:
                temp_vol -= 0.1
            st.info(f"염기성 이온이 더 많습니다. 중화반응이 일어나기 위해서는 1ml당 이온 수가 {int(b_ion_per_ml)}개인 염기성용액이 총 {temp_vol:.1f}ml만 필요합니다.")
            
        elif total_basic == total_acid:
            st.success("이온 수가 같으므로 **중화반응**이 일어납니다. (추가 계산 없음)")
            
        else:
            # while문을 이용해 염기 이온이 산성 이온과 같아질 때까지 필요한 추가 부피 계산
            added_vol = 0.0
            while (b_ion_per_ml * (b_vol + added_vol)) < total_acid:
                added_vol += 0.1
            st.info(f"중화반응이 일어나기 위해서는 1ml당 이온 수가 {int(b_ion_per_ml)}개인 염기성용액이 **{added_vol:.1f}ml** 더 필요합니다.")

    # [경우 B] 염기의 이온 수와 부피를 입력받아 -> 필요한 산성 용액의 부피 계산
    elif basic_ion is not None and basic_volume is not None:
        a_ion_per_ml = st.session_state.acid[0]
        a_vol = st.session_state.acid[1]
        
        total_basic = basic_ion * basic_volume
        total_acid = a_ion_per_ml * a_vol
        
        st.subheader("📊 실험 결과 (산성 용액 기준 계산)")
        st.write(f"현재 용액은 **<<{first_selected}>>**입니다.")
        
        if total_acid > total_basic:
            # while문을 이용해 산성 이온과 염기 이온이 같아질 때까지 부피 감소 계산
            temp_vol = a_vol
            while (a_ion_per_ml * temp_vol) > total_basic:
                temp_vol -= 0.1
            st.info(f"산성 이온이 더 많습니다. 중화반응이 일어나기 위해서는 1ml당 이온 수가 {int(a_ion_per_ml)}개인 산성용액이 총 {temp_vol:.1f}ml만 필요합니다.")
            
        elif total_acid == total_basic:
            st.success("이온 수가 같으므로 **중화반응**이 일어납니다. (추가 계산 없음)")
            
        else:
            # while문을 이용해 산성 이온이 염기 이온과 같아질 때까지 필요한 추가 부피 계산
            added_vol = 0.0
            while (a_ion_per_ml * (a_vol + added_vol)) < total_basic:
                added_vol += 0.1
            st.info(f"중화반응이 일어나기 위해서는 1ml당 이온 수가 {int(a_ion_per_ml)}개인 산성용액이 **{added_vol:.1f}ml** 더 필요합니다.")


# 4. 실험 시작 버튼
if st.button("🚀 실험 시작"):
    if not st.session_state.acid or not st.session_state.basic:
        st.error("⚠️ 산성과 염기성 리스트가 모두 채워져야 합니다!")
    else:
        # for문을 활용해 두 리스트의 모든 값(이온수, 부피)이 0보다 큰지 반복 검증
        all_values = st.session_state.acid + st.session_state.basic
        for val in all_values:
            while val <= 0:
                st.error("⚠️ 0보다 작거나 같은 값이 포함되어 있습니다. 다시 입력해 주세요.")
                st.stop()
                break

        # 저장된 값 꺼내기
        acid_ion = float(st.session_state.acid[0])
        acid_volume = float(st.session_state.acid[1])
        basic_ion = float(st.session_state.basic[0])
        basic_volume = float(st.session_state.basic[1])

        # 처음 선택한 용액이 무엇이냐에 따라 각각의 방식으로 함수 호출
        if st.session_state.first_choice == "산성":
            check_react(acid_ion=acid_ion, acid_volume=acid_volume)
        else:
            check_react(basic_ion=basic_ion, basic_volume=basic_volume)
