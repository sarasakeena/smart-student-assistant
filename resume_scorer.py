import json

class ResumeScorer:
    def __init__(self):
        # Benchmarks for skill gap analysis (can be expanded)
        self.industry_benchmarks = {
            "Software Engineering": ["Python", "Java", "Git", "Docker", "SQL", "AWS", "Agile"],
            "Data Science": ["Python", "R", "SQL", "Machine Learning", "Pandas", "Statistics"],
            "Project Management": ["Scrum", "PMP", "Agile", "Budgeting", "Risk Management", "Leadership"]
        }

    def score_resume(self, parsed_resume, target_industry="Software Engineering"):
        scores = {
            "completeness": 0,
            "skills": 0,
            "experience": 0,
            "formatting": 0,
            "keywords": 0
        }
        
        strengths = []
        improvements = []
        
        # 1. Completeness (20 points)
        required_fields = ["name", "skills", "experience", "education"]
        found_fields = [f for f in required_fields if parsed_resume.get(f)]
        if parsed_resume.get("contact", {}).get("email") and parsed_resume.get("contact", {}).get("phone"):
            found_fields.append("contact")
            
        scores["completeness"] = (len(found_fields) / (len(required_fields) + 1)) * 20
        if scores["completeness"] < 15:
            improvements.append("Complete missing sections: Contact, Education, or Experience.")
        else:
            strengths.append("Resume is structurally complete.")

        # 2. Skills (25 points)
        skill_list = parsed_resume.get("skills", [])
        scores["skills"] = min(len(skill_list) * 3, 25) # 3 pts per skill, cap at 25
        
        if len(skill_list) < 5:
            improvements.append("Add more technical and soft skills (aim for at least 5-8).")
        else:
            strengths.append(f"Strong skill set with {len(skill_list)} identified skills.")

        # 3. Experience (25 points)
        exp_list = parsed_resume.get("experience", [])
        scores["experience"] = min(len(exp_list) * 8, 25) # 8 pts per job, cap at 25
        
        if not exp_list:
            improvements.append("Detailed work experience is missing or not clearly parsed.")
        else:
            strengths.append(f"Clear career progression with {len(exp_list)} roles.")

        # 4. Formatting & Grammar Heuristic (15 points)
        # Check for sentence case and average word lengths as a proxy
        all_text = " ".join(skill_list) + str(exp_list)
        if len(all_text) > 100:
            scores["formatting"] = 15
        else:
            scores["formatting"] = 5
            improvements.append("Resume content is too brief; expand on your achievements.")

        # 5. Keywords & Industry Alignment (15 points)
        benchmark_skills = self.industry_benchmarks.get(target_industry, [])
        matches = [s for s in skill_list if s.capitalize() in [b.capitalize() for b in benchmark_skills]]
        scores["keywords"] = (len(matches) / max(len(benchmark_skills), 1)) * 15
        
        # Skill Gap Identification
        gaps = [s for s in benchmark_skills if s.capitalize() not in [sk.capitalize() for sk in skill_list]]
        if gaps:
            improvements.append(f"Industry Skill Gap identified: Consider learning {', '.join(gaps[:3])}.")
        else:
            strengths.append(f"Excellent alignment with {target_industry} standards.")

        overall_score = sum(scores.values())

        return {
            "overall_score": round(overall_score, 1),
            "section_scores": {k: round(v, 1) for k, v in scores.items()},
            "strengths": strengths,
            "improvements": improvements,
            "skill_gaps": gaps
        }

if __name__ == "__main__":
    # Example usage with mock data
    scorer = ResumeScorer()
    mock_resume = {
        "name": "John Doe",
        "contact": {"email": "john@doe.com", "phone": "123-456-7890"},
        "skills": ["Python", "SQL", "Git"],
        "experience": [{"title": "Software Engineer", "company": "Tech", "duration": "2 years"}],
        "education": [{"degree": "BS CS", "school": "Stanford"}],
        "certifications": ["AWS"]
    }
    print(json.dumps(scorer.score_resume(mock_resume), indent=2))
