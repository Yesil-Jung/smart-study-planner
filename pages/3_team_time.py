"""팀 공통 빈 시간 화면 (C 담당)"""

import os
import sys
import json

import pandas as pd
import streamlit as st

# modules 폴더를 불러올 수 있게 프로젝트 최상위 폴더를 경로에 추가
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

from modules.team_time import (
    DAYS, DAY_START, DAY_END, SLOT,
    to_minutes, to_hhmm, get_busy_slots, find_common_free,
)

st.title("👥 팀 공통 빈 시간 찾기")
st.caption("팀원 시간표를 합쳐서 모두 비어 있는 시간을 찾아줘요.")

# 1. 시간표 불러오기: 파일 업로드 or 샘플 데이터
uploaded = st.file_uploader("시간표 JSON 파일 올리기 (없으면 샘플 사용)", type="json")
if uploaded:
    timetables = json.load(uploaded)
else:
    with open(os.path.join(ROOT, "data", "sample_timetables.json"), encoding="utf-8") as f:
        timetables = json.load(f)

# 2. 팀원 선택
names = [t["owner"] for t in timetables]
selected = st.multiselect("팀원 선택", names, default=names)
min_hours = st.slider("최소 빈 시간 (시간)", 0.5, 3.0, 1.0, step=0.5)

if st.button("빈 시간 찾기", type="primary"):
    chosen = [t for t in timetables if t["owner"] in selected]
    if len(chosen) < 2:
        st.warning("팀원을 2명 이상 선택해주세요.")
        st.stop()

    free = find_common_free(chosen, min_minutes=int(min_hours * 60))

    # 3. 결과 텍스트
    st.subheader("✅ 모두 가능한 시간")
    for day in DAYS:
        text = ", ".join(f"{s}~{e}" for s, e in free[day]) or "없음"
        st.write(f"**{day}**: {text}")

    # 4. 색칠된 시간표 (초록 = 모두 빔)
    st.subheader("🗓 한눈에 보기")
    busy = get_busy_slots(chosen)
    times = list(range(to_minutes(DAY_START), to_minutes(DAY_END), SLOT))
    table = pd.DataFrame(
        {day: ["" if t not in busy[day] else "수업" for t in times] for day in DAYS},
        index=[to_hhmm(t) for t in times],
    )

    def color(cell):
        return "background-color: #ffcdd2" if cell else "background-color: #c8e6c9"

    st.dataframe(table.style.map(color), height=600, width="stretch")
