from datetime import datetime, timedelta

# 수업 시간과 겹치지 않는 공부 가능 시간 계산
def find_free_slots(classes, target_date, day, start_time="09:00", end_time="18:00"):
    start = datetime.strptime(start_time, "%H:%M")
    end = datetime.strptime(end_time, "%H:%M")

    # 해당 요일의 수업만 선택하고 시작 시간순 정렬
    today_classes = sorted(
        [c for c in classes if c["day"] == day],
        key=lambda c: c["start"]
    )

    free_slots = []
    current = start

    for c in today_classes:
        class_start = datetime.strptime(c["start"], "%H:%M")
        class_end = datetime.strptime(c["end"], "%H:%M")

        # 수업 시작 전까지의 빈 시간 저장
        if current < class_start:
            finish = min(class_start, end)

            if current < finish:
                free_slots.append({
                    "date": target_date,
                    "start": current.strftime("%H:%M"),
                    "end": finish.strftime("%H:%M")
                })

        # 수업 종료 시각으로 이동
        current = max(current, class_end)

        if current >= end:
            break

    # 마지막 수업 이후의 빈 시간 저장
    if current < end:
        free_slots.append({
            "date": target_date,
            "start": current.strftime("%H:%M"),
            "end": end.strftime("%H:%M")
        })

    return free_slots

# 테스트용 수업 시간표
if __name__ == "__main__":
    classes = [
        {
            "course": "자료구조",
            "day": "월",
            "start": "09:00",
            "end": "10:30"
        },
        {
            "course": "통계학",
            "day": "월",
            "start": "13:00",
            "end": "15:00"
        }
    ]

    result = find_free_slots(classes, "2026-11-30", "월")

    for slot in result:
        print(slot)