import unittest
from resume_scorer import ResumeScorer

class TestResumeScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = ResumeScorer()
        self.perfect_resume = {
            "name": "Jane Doe",
            "contact": {"email": "jane@doe.com", "phone": "111-222-3333"},
            "skills": ["Python", "Java", "Git", "Docker", "SQL", "AWS", "Agile"],
            "experience": [
                {"title": "Senior Dev", "company": "A", "duration": "3y"},
                {"title": "Junior Dev", "company": "B", "duration": "2y"},
                {"title": "Intern", "company": "C", "duration": "1y"}
            ],
            "education": [{"degree": "MS CS", "school": "MIT"}],
            "certifications": ["AWS Certified"]
        }
        
        self.poor_resume = {
            "name": "Incognito",
            "skills": ["Communication"],
            "experience": [],
            "education": []
        }

    def test_high_score_resume(self):
        result = self.scorer.score_resume(self.perfect_resume, "Software Engineering")
        self.assertGreaterEqual(result['overall_score'], 80)
        self.assertIn("Resume is structurally complete.", result['strengths'])
        self.assertEqual(len(result['skill_gaps']), 0)

    def test_poor_score_resume(self):
        result = self.scorer.score_resume(self.poor_resume, "Software Engineering")
        self.assertLess(result['overall_score'], 50)
        self.assertTrue(len(result['improvements']) > 0)
        self.assertIn("Python", result['skill_gaps'])

    def test_industry_alignment(self):
        # Testing Data Science alignment
        ds_resume = {
            "skills": ["Python", "Machine Learning", "Statistics"],
            "name": "Data Scientist",
            "experience": [{"title": "Analyst", "company": "X", "duration": "1y"}],
            "education": [{"degree": "PhD", "school": "Y"}]
        }
        result = self.scorer.score_resume(ds_resume, "Data Science")
        self.assertIn("Python", [s.capitalize() for s in ds_resume['skills']])
        self.assertNotIn("Python", result['skill_gaps'])

if __name__ == "__main__":
    unittest.main()
