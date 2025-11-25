from datetime import datetime, date
from typing import List, Dict, Any

# Helper: Safe parse date
def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        return None


# Urgency Score
def urgency_score(due: date, today: date):
    if due is None:
        return 5  # Medium urgency

    days_left = (due - today).days

    if days_left < 0:
        return 10  # overdue
    elif days_left == 0:
        return 9   # due today
    elif days_left <= 3:
        return 7   # due soon
    elif days_left <= 7:
        return 5   # due this week
    else:
        return 3   # far deadline


# Effort Score
def effort_score(hours: float):
    if hours <= 2:
        return 10
    elif hours <= 5:
        return 7
    elif hours <= 8:
        return 5
    else:
        return 3 


# Dependency Count
def compute_dependency_counts(tasks):
    counts = {t["id"]: 0 for t in tasks}

    for t in tasks:
        for dep in t.get("dependencies", []):
            if dep in counts:
                counts[dep] += 1

    return counts

# Validating Dependencies
def validate_dependencies(tasks):
    task_ids = {t["id"] for t in tasks}

    for task in tasks:
        for dep in task.get("dependencies", []):
            if dep not in task_ids:
                raise ValueError(f"Task {task['id']} has invalid dependency ID: {dep}")


# MAIN SCORING FUNCTION

def score_tasks(tasks: List[Dict[str, Any]], today: date = None):

    # Apply todays date
    if today is None:
        today = date.today()

    # Auto generate IDs if missing
    for idx, t in enumerate(tasks):
        if "id" not in t:
            t["id"] = idx

    # Validate dependency IDs
    validate_dependencies(tasks)

    # Count dependents
    dep_counts = compute_dependency_counts(tasks)

    scored = []

    for task in tasks:
        tid = task["id"]

        # Safe parsing
        due = parse_date(task.get("due_date"))

        # Importance clamped 1-10
        importance_raw = task.get("importance", 5)
        try:
            importance = float(importance_raw)
        except:
            importance = 5
        importance = max(1, min(10, importance))

        # Estimated hours with minimum 0.1
        hours_raw = task.get("estimated_hours", 4)
        try:
            hours = float(hours_raw)
        except:
            hours = 4
        hours = max(0.1, hours)

        dependents = dep_counts.get(tid, 0)

        # Computing sub-scores
        u = urgency_score(due, today)
        i = importance
        e = effort_score(hours)
        d = min(dependents * 2, 10) 

        total = u + i + e + d

##### Reason Text
        reasons = []

        # urgency reason
        if due is None:
            reasons.append("No due date (medium urgency).")
        else:
            days_left = (due - today).days
            if days_left < 0:
                reasons.append("Task is overdue.")
            elif days_left == 0:
                reasons.append("Task is due today.")
            elif days_left <= 3:
                reasons.append(f"Due soon in {days_left} day(s).")
            elif days_left <= 7:
                reasons.append("Due within a week.")
            else:
                reasons.append("Due later (low urgency).")

        # importance reason
        if importance >= 8:
            reasons.append("High importance.")
        elif importance <= 3:
            reasons.append("Low importance.")
        else:
            reasons.append("Medium importance.")

        # effort reason
        if hours <= 2:
            reasons.append("Quick task (low effort).")
        elif hours >= 8:
            reasons.append("High effort task.")

        # dependency reason
        if dependents > 0:
            reasons.append(f"Blocks {dependents} other task(s).")

        scored.append({
            **task,
            "importance": importance,          # clamped
            "estimated_hours": hours,          # clamped
            "score": total,
            "reason": " ".join(reasons)
        })

    # Sorted by score highest first
    scored.sort(key=lambda t: t["score"], reverse=True)
    return scored
