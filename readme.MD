# Resume Optimizer & Job Match Assistant 🚀

## Overview
An AI-powered assistant that analyzes resumes, scores quality, and matches jobs based on skills and experience.

## Vertical
**Career Development Assistant** - Helps job seekers optimize resumes and find best-fit opportunities

## Approach & Logic

### How It Works:
1. **Resume Parser** - Extracts skills, experience, education from resume files
2. **Resume Scorer** - Rates resume quality (0-100) with improvement suggestions
3. **Job Matcher** - Calculates match percentage between resume and job postings
4. **Main Assistant** - Orchestrates all modules with user-friendly interface

### Smart Decision Making:
- Uses NLP to identify relevant skills
- Calculates match score based on skill overlap, experience level, and domain alignment
- Provides specific recommendations for improvements
- Prioritizes job matches by compatibility

## Solution Features
✅ Parse PDF/DOCX resumes  
✅ Score resume quality with detailed feedback  
✅ Match resumes to job descriptions  
✅ Generate improvement recommendations  
✅ Simple CLI interface  
✅ Unit tests included  

## Assumptions
- Resume files are in PDF or DOCX format
- Job descriptions provided as plain text
- English language content
- Standard resume format (name, contact, skills, experience, education)

## Code Quality
- **Modular design** - Separate modules for each functionality
- **Error handling** - Robust exception handling for file parsing
- **Type hints** - Clear function signatures
- **Documentation** - Docstrings on all functions
- **Testing** - Unit tests for core modules
- **Maintainable** - Clean, readable code structure

## Project Structure
```bash
resume-optimizer-assistant/
├── resume_parser.py        # Resume file parsing
├── resume_scorer.py        # Quality scoring logic
├── job_matcher.py          # Job matching engine
├── assistant.py            # Main orchestrator
├── config.py              # Configuration
├── tests/                 # Unit tests
├── requirements.txt       # Dependencies
└── README.md             # This file
```

## How to Run

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Run the assistant:
```bash
python assistant.py
```

### Run tests:
```bash
python -m pytest tests/
```

## Example Usage
```python
from assistant import ResumeAssistant

# Initialize
assistant = ResumeAssistant()

# Analyze resume
resume_data = assistant.analyze_resume('resume.pdf')
print(f"Resume Score: {resume_data['overall_score']}/100")

# Match with job
job_description = "Senior Python developer with 5+ years experience..."
match = assistant.match_job(job_description)
print(f"Match Score: {match['match_score']}%")
```

## Files Included
- **resume_parser.py** - Extracts text and data from resumes
- **resume_scorer.py** - Calculates resume quality score
- **job_matcher.py** - Matches resume skills to job requirements
- **assistant.py** - Main interface combining all modules
- **requirements.txt** - Python dependencies
- **tests/** - Unit tests for validation

## Implementation Highlights
- Efficient text parsing without external APIs
- Semantic skill matching algorithm
- Comprehensive scoring rubric
- Clear error messages and logging
- Easy to extend with new features
