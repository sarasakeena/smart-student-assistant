import os
import json
import logging
from dotenv import load_dotenv
from resume_parser import ResumeParser
from resume_scorer import ResumeScorer
from job_matcher import JobMatcher
from job_matcher import JobMatcher

# Load environment variables (API Keys)
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class ResumeAssistant:
    def __init__(self):
        self.parser = ResumeParser()
        self.scorer = ResumeScorer()
        self.matcher = JobMatcher()
        self.current_analysis = None
        self.current_match = None

    def analyze_resume(self, file_path):
        parsed_data = self.parser.parse(file_path)
        if "error" in parsed_data:
            logger.error(f"Analysis failed: {parsed_data['error']}")
            return None
        
        raw_text = self.parser.extract_text_from_pdf(file_path) if file_path.endswith('.pdf') else self.parser.extract_text_from_docx(file_path)
        score_data = self.scorer.score_resume(parsed_data)
        
        self.current_analysis = {"parsed": parsed_data, "scoring": score_data, "raw_text": raw_text}
        return self.current_analysis

    def match_job(self, job_description):
        if not self.current_analysis:
            return {"error": "Please re-upload your resume. The AI server was recently updated and its memory was cleared."}
        
        # We'll use Mistral AI as the primary brain
        if os.getenv("MISTRAL_API_KEY") or os.getenv("GEMINI_API_KEY"):
            return self.get_ai_smart_match(job_description)
            
        # Fallback to local matcher
        match_score = self.matcher.calculate_match_score(self.current_analysis['raw_text'], job_description)
        missing_keywords = self.matcher.get_missing_keywords(self.current_analysis['raw_text'], job_description)
        self.current_match = {"match_score": round(match_score, 1), "missing_keywords": missing_keywords}
        return self.current_match

    def get_ai_smart_match(self, job_description):
        """Uses Mistral AI to provide a smart match score and improvement suggestions."""
        from mistralai import Mistral
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key: return None
        
        client = Mistral(api_key=api_key)
        
        prompt = f"""
        Analyze this Resume against the Job Description.
        
        RESUME:
        {self.current_analysis['raw_text'][:3000]}
        
        JOB DESCRIPTION:
        {job_description[:2000]}
        
        Return ONLY a JSON object with:
        {{
            "match_score": (0-100),
            "missing_keywords": ["kw1", "kw2"],
            "smart_suggestions": ["specific tip 1", "specific tip 2"],
            "tailored_summary": "one sentence on why this is or isn't a good fit"
        }}
        """
        try:
            response = client.chat.complete(
                model="mistral-large-latest",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            # Mistral response is already structured
            self.current_match = json.loads(response.choices[0].message.content)
            return self.current_match
        except Exception as e:
            logger.error(f"Mistral Matching failed: {e}")
            return {"match_score": 0, "smart_suggestions": ["AI Connection error."], "missing_keywords": []}

    def generate_report(self):
        if not self.current_analysis: return "No data."
        report = f"""
=========================================
      RESUME INSIGHTS REPORT
=========================================
NAME: {self.current_analysis['parsed'].get('name', 'N/A')}
OVERALL QUALITY SCORE: {self.current_analysis['scoring']['overall_score']}/100

STRENGTHS:
- """ + "\n- ".join(self.current_analysis['scoring']['strengths']) + """

AREAS FOR IMPROVEMENT:
- """ + "\n- ".join(self.current_analysis['scoring']['improvements']) + """
"""
        if self.current_match:
            report += f"""
JOB MATCH SCORE: {self.current_match['match_score']}%
CRITICAL MISSING KEYWORDS: {', '.join(self.current_match['missing_keywords'][:5])}
"""
        return report

def main():
    assistant = ResumeAssistant()
    print("\n" + "="*40)
    print("   🚀 SMART RESUME ASSISTANT ACTIVE")
    print("="*40)
    
    resume_path = input("\n📄 Enter path to your resume (PDF or DOCX): ").strip('"')
    if not os.path.exists(resume_path):
        print("❌ File not found! Please check the path.")
        return

    assistant.analyze_resume(resume_path)
    
    job_desc = input("\n💼 Paste the Job Description here (or press Enter to skip): ")
    if job_desc:
        assistant.match_job(job_desc)
    
    print(assistant.generate_report())

    save_choice = input("\n📊 Save to Google Sheets? (y/n): ").lower()
    if save_choice == 'y':
        sheet_id = input("🔗 Enter your Google Spreadsheet ID: ")
        company = input("🏢 Company Name: ")
        role = input("👨‍💻 Job Role: ")
        assistant.save_tracking(sheet_id, company, role)
        print("✅ Success! Check your Google Sheet.")

if __name__ == "__main__":
    main()
