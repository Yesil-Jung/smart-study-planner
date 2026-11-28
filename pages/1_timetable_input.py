import datetime
import json
from pathlib import Path

import pandas as pd
import streamlit as st

OWNER = "서연"
DATA_PATH = Path("data/timetable_seoyeon.json")
DAYS = ["월", "화", "수", "목", "금", "토", "일"]


def load_classes():
    if DATA_PATH.exists():
        with open(DATA_PATH, encoding="utf-8") as f:
            return json.load(f)["classes"]
    return []


def save_classes(classes):
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump({"owner": OWNER, "classes": classes}, f,
                  ensure_ascii=False, indent=2)


def is_overlap(new, classes):
    """같은 요일에 시간이 겹치는 수업이 있는지 검사"""
    for c in classes:
        if c["day"] == new["day"] and new["start"] < c["end"] and c["start"] < new["end"]:
            return c
    return None


st.title("내 시간표 입력")

if "classes" not in st.session_state:
    st.session_state.classes = load_classes()

# ---- 입력 폼 ----
with st.form("add_class", clear_on_submit=True):
    course = st.text_input("과목명")
    day = st.selectbox("요일", DAYS)
    col1, col2 = st.columns(2)
    start = col1.time_input("시작", value=datetime.time(9, 0), step=1800)
    end = col2.time_input("종료", value=datetime.time(10, 30), step=1800)
    submitted = st.form_submit_button("추가")

if submitted:
    new = {
        "course": course.strip(),
        "day": day,
        "start": start.strftime("%H:%M"),
        "end": end.strftime("%H:%M"),
    }
    if not new["course"]:
        st.error("과목명을 입력해주세요.")
    elif new["start"] >= new["end"]:
        st.error("종료 시간은 시작 시간보다 늦어야 해요.")
    elif (dup := is_overlap(new, st.session_state.classes)):
        st.error(f"'{dup['course']}' 수업과 시간이 겹쳐요.")
    else:
        st.session_state.classes.append(new)
        save_classes(st.session_state.classes)
        st.success(f"{new['course']} 추가 완료")

# ---- 현재 시간표 ----
st.subheader("현재 시간표")
if st.session_state.classes:
    df = pd.DataFrame(st.session_state.classes)
    df["요일순"] = df["day"].map(DAYS.index)
    df = df.sort_values(["요일순", "start"]).drop(columns="요일순")
    st.dataframe(df, use_container_width=True, hide_index=True)

    labels = [f"{c['day']} {c['start']}~{c['end']} {c['course']}"
              for c in st.session_state.classes]
    target = st.selectbox("삭제할 수업", labels)
    if st.button("삭제"):
        st.session_state.classes.pop(labels.index(target))
        save_classes(st.session_state.classes)
        st.rerun()
else:
    st.info("아직 등록된 수업이 없어요.")