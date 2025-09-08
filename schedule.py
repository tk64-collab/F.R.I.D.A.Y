import json
from datetime import datetime


def save_schedule(event):
    today = datetime.now().strftime("%Y-%m-%d")
    schedule = load_schedule()

    if today not in schedule:
        schedule[today] = []

    schedule[today].append(event)
    with open("schedule.json", "w", encoding="utf-8") as f:
        json.dump(schedule, f, ensure_ascii=False, indent=4)


def load_schedule():
    try:
        with open("schedule.json", "r", encoding="utf-8") as f:
            schedule = json.load(f)
    except FileNotFoundError:
        schedule = {}
    return schedule


def get_today_schedule():
    today = datetime.now().strftime("%Y-%m-%d")
    schedule = load_schedule()
    return schedule.get(today, [])


if __name__ == "__main__":
    save_schedule("10:00 AM - Meeting with the team")
    print(get_today_schedule())
