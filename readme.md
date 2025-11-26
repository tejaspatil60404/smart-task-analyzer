Smart Task Analyzer – Prioritize Tasks Intelligently

This project is built as part of the Singularium Internship Assignment 2025, where the objective is to create an intelligent system that analyzes tasks, scores them based on priority, and provides visual insights to help users decide what to work on first.

The system uses a combination of deadline urgency, task importance, estimated effort, and dependency analysis to generate useful insights.

🧠 Overview

Smart Task Analyzer is a lightweight task-prioritization engine with:

A Django REST API backend

A responsive HTML/CSS/JS frontend

A clean scoring algorithm

Task suggestions (Top 3)

Unit tests

Dependency validation

The goal is to help users prioritize tasks based on impact, urgency, bottlenecks, and effort.

📌 Problem Statement (as per PDF)

Modern productivity tools often fail to provide personalized task prioritization. People manually decide which tasks to do first without data-driven insights.
This project aims to solve this problem by:

Automatically ranking tasks

Detecting dependencies

Suggesting the most impactful next actions


🚀 Features
✅ 1. Smart Scoring Algorithm

Scores each task based on:

Urgency (deadline proximity)

Importance (1–10 scale)

Effort (hours)

Dependency impact (tasks blocked by it)

✅ 2. Task Suggestion Engine

Returns the top 3 tasks you should do next based on your entire task network.

✅ 3. Fully Responsive Frontend

Clean, minimal UI with:

Live task preview

JSON input support

Smooth scroll

2-panel layout

✅ 4. Unit Testing

Covers:

Scoring logic

Clamping

API endpoints

Dependency counting

🛠️ Tech Stack
Backend

Django

Django REST Framework

Python 3

Frontend

Vanilla HTML

CSS (fully responsive)

JavaScript

Other

JSON-based communication

REST API

Unit Tests

📂 Folder Structure
task-analyzer/
├── backend/
│   ├── task_analyzer/
│   ├── tasks/
│   │   ├── scoring.py
│   │   ├── views.py
│   │   ├── tests.py
│   ├── manage.py
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│
├── README.md
└── requirements.txt

⚙️ Installation & Setup
1. Clone the Repository
git clone https://github.com/tejaspatil60404/smart-task-analyzer.git
cd smart-task-analyzer

2. Create Virtual Environment
python -m venv venv


Activate:

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Run Django Server
cd backend
python manage.py runserver

5. Run Frontend (Localhost)
cd frontend
python -m http.server 5500


Open:
👉 http://localhost:5500/index.html

🔌 API Endpoints
POST /api/tasks/analyze/

Returns scored tasks sorted by priority.

Request Body Example:

[
  {
    "id": 1,
    "title": "Fix login bug",
    "importance": 8,
    "due_date": "2025-11-30",
    "estimated_hours": 3,
    "dependencies": []
  }
]


Response Example:

[
    {
        "id": 1,
        "title": "Fix login bug",
        "score": 24.5,
        "reason": "Due within a week. High importance. Quick task (low effort)."
    }
]

POST /api/tasks/suggest/

Returns Top 3 recommended tasks.

🧮 Scoring Algorithm Explanation

Your algorithm considers 4 core factors:

🎯 1. Urgency (0–10)

Depending on days left before deadline:

Overdue → 10

Due today → 9

Due in 1–3 days → 7

Due in 4–7 days → 5

⭐ 2. Importance (1–10)

User-defined, clamped to:
✔ Min = 1
✔ Max = 10

⚡ 3. Effort (0–10)

≤2 hours → 10

≤5 hours → 7

≤8 hours → 5

8 hours → 3

🔗 4. Dependency Impact (0–10)

Each task that depends on this task adds +2 score (max 10).

Final Score:
score = urgency + importance + effort + dependency_score


The system then sorts tasks descending by score.


🧪 Unit Tests Included

Includes tests for:

✔ Overdue logic
✔ Importance clamping
✔ Dependency scoring
✔ Analyze endpoint
✔ Suggest endpoint

Run:

python manage.py test


Expected:

Ran 5 tests — OK

📸 Screenshots:
![alt text](<Screenshot 2025-11-26 180748.png>) ![alt text](<Screenshot 2025-11-26 180453.png>) ![alt text](<Screenshot 2025-11-26 180605.png>) ![alt text](<Screenshot 2025-11-26 180627.png>) ![alt text](<Screenshot 2025-11-26 180716.png>)

🔮 Future Improvements

Add drag-and-drop task updates

Dark mode toggle

AI-based re-ranking of tasks

Persistent storage with DB

Authentication + multiple users

Detailed dependency graph visualization

👤 Author

Tejas
B.Tech AIML (2026)
Smart Task Analyzer — Singularium Internship Assignment 2025
