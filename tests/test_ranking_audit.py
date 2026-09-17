"""Tests for ranking_audit module."""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ranking_audit import score_name, score_description, score_topics, score_readme, score_stars, score_activity


class TestScoreName(unittest.TestCase):
    def test_exact_match(self):
        self.assertEqual(score_name("cloudflare-turnstile-solver", {"cloudflare", "turnstile", "solver"}), 100)

    def test_partial_match(self):
        result = score_name("my-solver-tool", {"cloudflare", "turnstile", "solver"})
        self.assertGreater(result, 0)
        self.assertLess(result, 100)

    def test_no_match(self):
        self.assertEqual(score_name("unrelated-project", {"cloudflare", "turnstile", "solver"}), 0)

    def test_empty_query(self):
        self.assertEqual(score_name("any-repo", set()), 100)


class TestScoreDescription(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(score_description(""), 0)
        self.assertEqual(score_description(None), 0)

    def test_short(self):
        self.assertEqual(score_description("Short"), 30)

    def test_medium(self):
        self.assertEqual(score_description("A decent description of the project"), 60)

    def test_optimal(self):
        desc = "A complete description that explains what the project does and why it matters for developers"
        self.assertEqual(score_description(desc), 100)


class TestScoreTopics(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(score_topics([]), 0)

    def test_few(self):
        self.assertEqual(score_topics(["python", "cli"]), 40)

    def test_good(self):
        self.assertEqual(score_topics(["a", "b", "c", "d", "e", "f", "g"]), 70)

    def test_optimal(self):
        topics = [f"topic-{i}" for i in range(12)]
        self.assertEqual(score_topics(topics), 100)


class TestScoreReadme(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(score_readme(""), 0)

    def test_short(self):
        self.assertEqual(score_readme("Just a few words here"), 20)

    def test_good(self):
        text = " ".join(["word"] * 300)
        self.assertEqual(score_readme(text), 75)

    def test_long(self):
        text = " ".join(["word"] * 600)
        self.assertEqual(score_readme(text), 100)


class TestScoreStars(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(score_stars(0), 0)

    def test_low(self):
        self.assertEqual(score_stars(5), 15)

    def test_medium(self):
        self.assertEqual(score_stars(75), 50)

    def test_high(self):
        self.assertEqual(score_stars(500), 70)

    def test_very_high(self):
        self.assertEqual(score_stars(5000), 100)


class TestScoreActivity(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(score_activity(""), 0)
        self.assertEqual(score_activity(None), 0)

    def test_recent(self):
        from datetime import datetime, timezone, timedelta
        recent = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
        self.assertEqual(score_activity(recent), 100)

    def test_stale(self):
        self.assertEqual(score_activity("2024-01-01T00:00:00Z"), 10)


if __name__ == "__main__":
    unittest.main()
