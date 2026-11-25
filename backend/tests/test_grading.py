import unittest

from app.services.grading_service import grade


class GradingTests(unittest.TestCase):
    def test_grade_tracks_score_and_concept_performance(self):
        questions = [
            {"id": "one", "correct_answer": "A", "concept_id": "cells", "explanation": "Cell basics"},
            {"id": "two", "correct_answer": "B", "concept_id": "cells"},
        ]
        result = grade(questions, {"one": "A"})
        self.assertEqual((result["score"], result["total"], result["percentage"]), (1, 2, 50))
        self.assertEqual(result["concept_performance"]["cells"], {"total": 2, "correct": 1})

    def test_empty_assessment_returns_zero_percent(self):
        self.assertEqual(grade([], {})["percentage"], 0)


if __name__ == "__main__":
    unittest.main()
