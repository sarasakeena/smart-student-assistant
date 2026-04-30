import unittest
from unittest.mock import patch, MagicMock
from resume_parser import ResumeParser

class TestResumeParser(unittest.TestCase):
    def setUp(self):
        self.parser = ResumeParser()
        self.sample_text = """
        John Doe
        Email: john.doe@example.com
        Phone: 123-456-7890
        
        Skills: Python, JavaScript, SQL, AWS, Leadership.
        
        Experience:
        Software Engineer
        Tech Corp
        2020 - Present
        
        Education:
        B.S. in Computer Science
        Stanford University
        """

    def test_contact_extraction(self):
        contact = self.parser.extract_contact_info(self.sample_text)
        self.assertEqual(contact['email'], "john.doe@example.com")
        self.assertEqual(contact['phone'], "123-456-7890")

    def test_skill_extraction(self):
        skills = self.parser.extract_skills(self.sample_text)
        self.assertIn("Python", skills)
        self.assertIn("Sql", skills)
        self.assertIn("Aws", skills)

    @patch('resume_parser.PdfReader')
    def test_pdf_parsing_flow(self, mock_reader):
        # Mocking PDF content
        mock_page = MagicMock()
        mock_page.extract_text.return_value = self.sample_text
        mock_reader.return_value.pages = [mock_page]
        
        # We need to mock existence of file
        with patch('os.path.exists', return_value=True):
            result = self.parser.parse("fake_resume.pdf")
            self.assertEqual(result['contact']['email'], "john.doe@example.com")
            self.assertIn("Python", result['skills'])

    def test_error_handling_missing_file(self):
        result = self.parser.parse("non_existent.pdf")
        self.assertEqual(result['error'], "File not found")

if __name__ == "__main__":
    unittest.main()
