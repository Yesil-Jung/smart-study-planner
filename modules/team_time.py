"""팀원 시간표를 합쳐서 모두 비어 있는 시간을 찾는 모듈 (C 담당)"""

import json

DAYS = ["월", "화", "수", "목", "금"]
DAY_START = "09:00"   # 하루 시작 시간
DAY_END = "22:00"     # 하루 끝 시간
SLOT = 30             # 30분 단위


def to_minutes(hhmm):
    """'13:30' → 810 (분 단위 숫자로 바꾸기)"""
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def to_hhmm(minutes):
    """810 → '13:30' (다시 시간 글자로 바꾸기)"""
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def load_timetables(path):
    """json 파일에서 시간표 리스트 읽기"""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_busy_slots(timetables):
    """모든 팀원의 수업 시간을 30분 칸 단위로 모으기
    결과 예: {"월": {540, 570, ...}, "화": {...}}  (540 = 09:00)
    """
    busy = {day: set() for day in DAYS}
    for person in timetables:
        for c in person["classes"]:
            if c["day"] not in busy:
                continue
            t = to_minutes(c["start"])
            while t < to_minutes(c["end"]):
                busy[c["day"]].add(t)
                t += SLOT
    return busy


def find_common_free(timetables, min_minutes=60):
    """모두 비어 있는 시간을 요일별로 찾기
    min_minutes: 이보다 짧은 빈 시간은 제외 (기본 1시간)
    결과 예: {"월": [("14:30", "22:00")], ...}
    """
    busy = get_busy_slots(timetables)
    result = {}

    for day in DAYS:
        free_ranges = []
        start = None
        t = to_minutes(DAY_START)
        end_of_day = to_minutes(DAY_END)

        while t <= end_of_day:
            is_free = t < end_of_day and t not in busy[day]
            if is_free and start is None:        # 빈 시간 시작
                start = t
            elif not is_free and start is not None:  # 빈 시간 끝
                if t - start >= min_minutes:
                    free_ranges.append((to_hhmm(start), to_hhmm(t)))
                start = None
            t += SLOT

        result[day] = free_ranges
    return result


if __name__ == "__main__":
    # 직접 실행해서 테스트: python modules/team_time.py
    tables = load_timetables("data/sample_timetables.json")
    free = find_common_free(tables)
    for day, ranges in free.items():
        text = ", ".join(f"{s}~{e}" for s, e in ranges) or "없음"
        print(f"{day}: {text}")
