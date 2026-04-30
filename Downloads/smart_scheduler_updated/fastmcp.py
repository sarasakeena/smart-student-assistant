from datetime import datetime, timedelta
import random

MOTIVATIONAL_QUOTES = [
    "Keep pushing, you're doing great! 💪",
    "Small steps every day lead to big results.",
    "Stay focused and never give up!",
    "Success is built on daily effort.",
    "One task at a time. Keep going!",
    "Your future self will thank you!",
    "Discipline is the bridge between goals and success.",
    "You’ve got this! Keep moving forward.",
    "Progress, not perfection.",
    "Hard work always pays off."
]

class FastMCP:
    def __init__(self):
        self.schedule = {}

    def create_schedule(self, tasks: list, daily_hours: float) -> dict:
        # Convert minutes to hours and sort tasks by priority and deadline
        tasks_sorted = sorted(tasks, key=lambda x: (x.get("priority", 3), x["deadline"]))
        today = datetime.today().date()
        self.schedule = {}

        max_deadline = max(datetime.strptime(t["deadline"], "%Y-%m-%d").date() for t in tasks)

        current_day = today
        while current_day <= max_deadline:
            day_str = str(current_day)
            self.schedule[day_str] = {
                "quote": random.choice(MOTIVATIONAL_QUOTES),
                "tasks": [],
                "summary": {
                    "total_hours": 0,
                    "total_tasks": 0
                }
            }
            current_day += timedelta(days=1)

        for task in tasks_sorted:
            task_name = task["name"]
            hours_required = task["hours"] + (task.get("minutes", 0) / 60)
            deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
            priority = task.get("priority", 3)

            current_day = today
            while hours_required > 0 and current_day <= deadline:
                day_str = str(current_day)
                day_schedule = self.schedule[day_str]

                remaining_time = daily_hours - day_schedule["summary"]["total_hours"]
                if remaining_time > 0:
                    hours_to_assign = min(remaining_time, hours_required)
                    day_schedule["tasks"].append({
                        "task": task_name,
                        "hours": round(hours_to_assign, 2),
                        "priority": priority
                    })
                    day_schedule["summary"]["total_hours"] += hours_to_assign
                    day_schedule["summary"]["total_tasks"] += 1
                    hours_required -= hours_to_assign

                current_day += timedelta(days=1)

        # Cleanup: remove any day that has 0 tasks
        self.schedule = {day: content for day, content in self.schedule.items() if content["tasks"]}

        return self.schedule
