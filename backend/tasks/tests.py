from django.test import TestCase
from datetime import date, timedelta
from .scoring import score_tasks
from rest_framework.test import APIClient
from django.urls import reverse


class ScoringAlgorithmTests(TestCase):

    def test_urgency_overdue(self):
        """Overdue tasks should get urgency score = 10."""
        tasks = [{
            "id": 1,
            "title": "Overdue task",
            "due_date": "2020-01-01",
            "estimated_hours": 3,
            "importance": 5,
            "dependencies": []
        }]

        scored = score_tasks(tasks, today=date(2025, 1, 1))
        self.assertEqual(scored[0]["score"], 10 + 5 + 7 + 0)  # urgency=10, importance=5, effort=7


    def test_importance_clamp(self):
        """Importance must stay in range 1–10."""
        tasks = [{
            "id": 1,
            "title": "Test importance",
            "due_date": "",
            "estimated_hours": 3,
            "importance": 50,   # invalid high
            "dependencies": []
        }]

        scored = score_tasks(tasks)
        self.assertLessEqual(scored[0]["importance"], 10)

    def test_dependency_counting(self):
        """Tasks that are depended on should get correct dependency score."""
        tasks = [
            {"id": 1, "title": "A", "due_date": "", "estimated_hours": 2, "importance": 5, "dependencies": []},
            {"id": 2, "title": "B", "due_date": "", "estimated_hours": 2, "importance": 5, "dependencies": [1]},
            {"id": 3, "title": "C", "due_date": "", "estimated_hours": 2, "importance": 5, "dependencies": [1]}
        ]

        scored = score_tasks(tasks)
        task1 = next(t for t in scored if t["id"] == 1)

        # depends: task 2 and task 3 => 2 tasks → dependency_score = min(2*2, 10) = 4
        dependency_score = task1["score"] - (5 + 5 + 10)  # urgency=5, importance=5, effort=10
        self.assertEqual(dependency_score, 4)


class AnalyzeEndpointTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_analyze_endpoint(self):
        """POST /api/tasks/analyze/ should return sorted scored tasks."""
        data = [
            {"id": 1, "title": "A", "due_date": "", "estimated_hours": 2, "importance": 5, "dependencies": []},
            {"id": 2, "title": "B", "due_date": "2020-01-01", "estimated_hours": 2, "importance": 5, "dependencies": []}
        ]

        response = self.client.post("/api/tasks/analyze/", data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("score", response.json()[0])
        self.assertIn("reason", response.json()[0])


class SuggestEndpointTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_suggest_top_three(self):
        """POST /api/tasks/suggest/ should return only top 3 tasks."""
        data = [
            {"id": 1, "title": "A", "due_date": "", "estimated_hours": 3, "importance": 5, "dependencies": []},
            {"id": 2, "title": "B", "due_date": "", "estimated_hours": 3, "importance": 5, "dependencies": []},
            {"id": 3, "title": "C", "due_date": "", "estimated_hours": 3, "importance": 5, "dependencies": []},
            {"id": 4, "title": "D", "due_date": "", "estimated_hours": 3, "importance": 5, "dependencies": []}
        ]

        response = self.client.post("/api/tasks/suggest/", data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        self.assertIn("suggest_reason", response.json()[0])
