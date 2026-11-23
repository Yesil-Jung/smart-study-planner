from datetime import datetime, timedelta

# 마감일이 가까운 과제부터 정렬
def sort_tasks(tasks):
    return sorted(
        tasks,
        key=lambda task: datetime.strptime(task["due"], "%Y-%m-%d")
    )

# 과제를 공부 가능한 시간에 자동 배치
def create_schedule(tasks, free_slots):
    schedule = []

    # 원본 시간표가 변경되지 않도록 복사
    available_slots = [slot.copy() for slot in free_slots]

    # 날짜와 시작 시간순으로 빈 시간 정렬
    available_slots.sort(
        key=lambda slot: (slot["date"], slot["start"])
    )

    for task in sort_tasks(tasks):
        remaining = task["hours"] * 60

        for slot in available_slots:
            if remaining <= 0:
                break

            # 마감일이 지났거나 마감일 당일인 시간은 제외
            if slot["date"] >= task["due"]:
                continue

            start = datetime.strptime(
                slot["date"] + " " + slot["start"],
                "%Y-%m-%d %H:%M"
            )
            end = datetime.strptime(
                slot["date"] + " " + slot["end"],
                "%Y-%m-%d %H:%M"
            )

            available = int((end - start).total_seconds() / 60)
            minutes = min(remaining, available)

            if minutes <= 0:
                continue

            finish = start + timedelta(minutes=minutes)

            schedule.append({
                "title": task["title"],
                "date": slot["date"],
                "start": start.strftime("%H:%M"),
                "end": finish.strftime("%H:%M")
            })

            # 사용한 시간만큼 빈 시간 갱신
            slot["start"] = finish.strftime("%H:%M")
            remaining -= minutes

    return schedule

# 이 파일을 직접 실행할 때만 테스트
if __name__ == "__main__":

    tasks = [
        {
            "course": "자료구조",
            "title": "과제2",
            "type": "과제",
            "due": "2026-12-05",
            "hours": 3
        },
        {
            "course": "통계학",
            "title": "과제1",
            "type": "과제",
            "due": "2026-12-02",
            "hours": 2
        }
    ]

    free_slots = [
        {"date": "2026-11-24", "start": "13:00", "end": "15:00"},
        {"date": "2026-11-25", "start": "14:00", "end": "16:00"},
        {"date": "2026-11-26", "start": "10:00", "end": "12:00"}
    ]

    print("자동 생성된 공부 계획")

    for block in create_schedule(tasks, free_slots):
        print(block)