import os
import re
import json
import spacy
from PyPDF2 import PdfReader
from docx import Document
from spacy.matcher import Matcher

# Load NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

class ResumeParser:
    def __init__(self):
        self.matcher = Matcher(nlp.vocab)

    def extract_text_from_pdf(self, pdf_path):
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception(f"Corrupted or invalid PDF: {str(e)}")

    def extract_text_from_docx(self, docx_path):
        try:
            doc = Document(docx_path)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            raise Exception(f"Corrupted or invalid DOCX: {str(e)}")

    def extract_contact_info(self, text):
        email = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        phone = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        return {
            "email": email[0] if email else "",
            "phone": phone[0] if phone else ""
        }

    def extract_name(self, doc):
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return ""

    def extract_skills(self, text):
        # A small sample list of common skills for matching
        skill_db = [
            "python", "java", "javascript", "sql", "react", "node.js", "aws", "docker",
            "communication", "leadership", "management", "problem solving", "scrum", "git"
        ]
        found_skills = []
        for skill in skill_db:
            if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
                found_skills.append(skill.capitalize())
        return list(set(found_skills))

    def parse(self, file_path):
        if not os.path.exists(file_path):
            return {"error": "File not found"}

        _, ext = os.path.splitext(file_path)
        try:
            if ext.lower() == '.pdf':
                text = self.extract_text_from_pdf(file_path)
            elif ext.lower() == '.docx':
                text = self.extract_text_from_docx(file_path)
            else:
                return {"error": "Unsupported file format"}
            
            doc = nlp(text)
            
            return {
                "name": self.extract_name(doc),
                "contact": self.extract_contact_info(text),
                "skills": self.extract_skills(text),
                "experience": self.extract_experience(text),
                "education": self.extract_education(text),
                "certifications": self.extract_certifications(text)
            }
        except Exception as e:
            return {"error": str(e)}

    def extract_experience(self, text):
        # Heuristic approach for experience
        experience = []
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if any(kw in line.lower() for kw in ["engineer", "developer", "manager", "intern"]):
                experience.append({
                    "title": line.strip(),
                    "company": lines[i+1].strip() if i+1 < len(lines) else "",
                    "duration": ""
                })
        return experience[:3] # Limit to top 3 for demo

    def extract_education(self, text):
        education = []
        if re.search(r'university|college|school|institute', text, re.I):
            match = re.search(r'([A-Z][a-z]+ (?:University|College|Institute))', text)
            if match:
                education.append({"degree": "", "school": match.group(1)})
        return education

    def extract_certifications(self, text):
        certs = ["AWS", "Azure", "GCP", "PMP", "Scrum Master", "CompTIA"]
        found = []
        for c in certs:
            if c in text:
                found.append(c)
        return found

if __name__ == "__main__":
    parser = ResumeParser()
    # Example usage (place a file called resume.pdf in the folder to test)
    # print(json.dumps(parser.parse("resume.pdf"), indent=2))
