from datetime import datetime, date
from typing import List, Dict, Any


def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        return None


def urgency_score(due: date, today: date):
    if due is None:
        return 5
    
    days_left = (due - today).days

    if days_left < 0:
        return 10
    elif days_left == 0:
        return 9
    elif days_left <= 3:
        return 7
    elif days_left <= 7:
        return 5
    else:
        return 3


def effort_score(hours: float):
    if hours <= 2:
        return 10
    elif hours <= 5:
        return 7
    elif hours <= 8:
        return 5
    else:
        return 3


def compute_dependency_counts(tasks):
    counts = {}
    for t in tasks:
        tid = t.get("id")
        if tid is not None:
            counts[tid] = 0

    for t in tasks:
        deps = t.get("dependencies", [])
        for dep in deps:
            if dep in counts:
                counts[dep] += 1

    return counts


def score_tasks(tasks: List[Dict[str, Any]], today=None):
    if today is None:
        today = date.today()

    dep_counts = compute_dependency_counts(tasks)
    scored = []

    for task in tasks:
        tid = task.get("id")

        due = parse_date(task.get("due_date"))
        importance = float(task.get("importance", 5))
        hours = float(task.get("estimated_hours", 4))
        dependents = dep_counts.get(tid, 0)

        u = urgency_score(due, today)
        i = importance
        e = effort_score(hours)
        d = min(dependents * 2, 10)

        total = u + i + e + d

        # Build reason
        reasons = []

        # urgency text
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

        # importance text
        if importance >= 8:
            reasons.append("High importance.")
        elif importance <= 3:
            reasons.append("Low importance.")
        else:
            reasons.append("Medium importance.")

        # effort text
        if hours <= 2:
            reasons.append("Quick task (low effort).")
        elif hours >= 8:
            reasons.append("High effort task.")

        # dependent text
        if dependents > 0:
            reasons.append(f"Blocks {dependents} other task(s).")

        scored.append({
            **task,
            "score": total,
            "reason": " ".join(reasons)
        })

    scored.sort(key=lambda t: t["score"], reverse=True)
    return scored
