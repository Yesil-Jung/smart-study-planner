import streamlit as st
from datetime import date, timedelta
from scheduler import create_schedule

# 페이지 제목
st.title("📚 스마트 학업 플래너")
st.subheader("자동 스케줄러")

# 과제 정보 입력
course = st.text_input("과목명", "자료구조")
task_name = st.text_input("과제 이름", "과제2")
due_date = st.date_input(
    "과제 마감일",
    value=date.today() + timedelta(days=7)
)
hours = st.number_input(
    "예상 소요 시간 (시간)",
    min_value=1,
    max_value=24,
    value=3
)

# 테스트용 공부 가능 시간 / 실제 시간표 연동 기능은 추후 추가
tomorrow = date.today() + timedelta(days=1)

free_slots = [
    {
        "date": (tomorrow + timedelta(days=i)).isoformat(),
        "start": "13:00",
        "end": "15:00"
    }
    for i in range(7)
]

# 자동 스케줄러 실행
if st.button("공부 계획 생성"):

    tasks = [{
        "course": course,
        "title": task_name,
        "type": "과제",
        "due": due_date.isoformat(),
        "hours": hours
    }]

    schedule = create_schedule(tasks, free_slots)

    if schedule:
        st.success("공부 계획이 생성되었습니다!")
        st.dataframe(schedule, hide_index=True)
    else:
        st.warning("마감일 전 배치 가능한 시간이 없습니다.")