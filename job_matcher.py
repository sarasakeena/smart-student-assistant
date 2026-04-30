import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

class JobMatcher:
    def __init__(self):
        pass

    def calculate_match_score(self, resume_text, job_description):
        """Calculates semantic similarity between resume and job description."""
        doc_resume = nlp(resume_text.lower())
        doc_job = nlp(job_description.lower())
        
        # Simple token-based similarity fallback for small models like sm
        # In production, we'd use 'en_core_web_md' or 'en_core_web_lg' for true vectors
        return doc_resume.similarity(doc_job) * 100

    def extract_keywords(self, text):
        """Extracts key nouns and proper nouns from text."""
        doc = nlp(text)
        return list(set([token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop]))

    def get_missing_keywords(self, resume_text, job_description):
        """Identifies important keywords in the job description missing from the resume."""
        resume_keywords = set(self.extract_keywords(resume_text))
        job_keywords = set(self.extract_keywords(job_description))
        
        missing = list(job_keywords - resume_keywords)
        return missing[:10] # Return top 10 missing keywords
