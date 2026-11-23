import streamlit as st

# 페이지 제목
st.title("📚 스마트 학업 플래너")
st.subheader("자동 스케줄러")

# 과제 정보 입력
task_name = st.text_input("과제 이름", "자료구조 과제2")
due_date = st.date_input("과제 마감일")
hours = st.number_input(
    "예상 소요 시간 (시간)",
    min_value=1,
    max_value=24,
    value=3
)

# 자동 배치 버튼
if st.button("공부 계획 생성"):
    st.success("과제 정보가 입력되었습니다!")
    st.write("과제명:", task_name)
    st.write("마감일:", due_date)
    st.write("예상 소요 시간:", hours)