"""Integration checks for hosting, adaptive quizzes, and real recommendations.

Run from the repository root:
python3 -m venv .venv
.venv/bin/python -m pip install -r club_recommender/requirements-dev.txt
.venv/bin/python -m unittest discover -s club_recommender/tests -v"""
import contextlib
import io
from pathlib import Path
import sys
import unittest

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend.main import app


class ClubsideIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    """
    Check that the app and dataset load
    and that the quiz and recommendation endpoints work together."""
    def test_page_assets_and_real_dataset_are_served_together(self):
        for path, expected_type in [("/", "text/html"), ("/assets/app.js", "javascript"), ("/assets/styles.css", "text/css")]:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, path)
            self.assertIn(expected_type, response.headers["content-type"])
        health = self.client.get("/health").json()
        clubs = self.client.get("/clubs").json()
        self.assertEqual(health["clubs_loaded"], len(clubs))
        self.assertGreater(len(clubs), 0)
        self.assertEqual(len({club["club_id"] for club in clubs}), len(clubs))

    """
    Check that quiz questions adapt to selected interests
    and that the recommendation endpoint returns real clubs."""
    def test_quiz_changes_followups_when_categories_change(self):
        self.assertEqual(self.client.get("/quiz/start").json()["question"]["id"], "categories")
        result = self.client.post("/quiz/next", json={"answers": {"categories": ["music", "outdoors"]}}).json()
        self.assertEqual(result["question"]["id"], "music")
        self.assertIn("outdoors", result["remaining"])
        result = self.client.post("/quiz/next", json={"answers": {"categories": ["outdoors"]}}).json()
        self.assertEqual(result["question"]["id"], "outdoors")
        self.assertNotIn("music", result["remaining"])

    """
    Check that a completed quiz produces recommendations
    and that the output does not print sensitive answers."""
    def test_complete_quiz_produces_real_club_results_without_printing_answers(self):
        answers = {"categories": ["music"], "music": ["a_cappella"], "vibe": ["social"], "time": "flexible", "beginner": "somewhat", "requirements": "either", "size": "any", "days": ["wednesday"], "goals": ["meet_people"], "free_text": "PRIVATE_TEST_NOTE_01"}
        self.assertIsNone(self.client.post("/quiz/next", json={"answers": answers}).json()["question"])
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            response = self.client.post("/recommend", json={"answers": answers, "top_n": 12})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("PRIVATE_TEST_NOTE_01", output.getvalue())
        self.assertNotIn("Normalized profile", output.getvalue())
        rows = response.json()["recommendations"]
        self.assertTrue(rows)
        self.assertLessEqual(len(rows), 12)
        ids = {c["club_id"] for c in self.client.get("/clubs").json()}
        for row in rows:
            self.assertIn(row["club_id"], ids)
            self.assertEqual(row["category"], "Music & Singing")
            self.assertEqual(row["subcategory"], "A Cappella")
            self.assertTrue(row["reasons"])
            self.assertGreaterEqual(row["match_percent"], 0)
            self.assertLessEqual(row["match_percent"], 100)


if __name__ == "__main__":
    unittest.main()
