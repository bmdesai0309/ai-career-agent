import ollama
import json
from config import settings

def evaluate_job(job_title, company_name, job_description):
    """Passes the scraped job to Llama 3.2 and monitors hardware/token usage."""
    print(f"\n[Brain] Running ATS Scan for: '{job_title}' at {company_name}")
    
    prompt = f"""
    You are an enterprise Applicant Tracking System (ATS). 
    Compare the following resume against the job description.
    
    RESUME:
    {settings.RESUME_TEXT}
    
    JOB TITLE: {job_title}
    COMPANY: {company_name}
    JOB DESCRIPTION: {job_description}

    Calculate the ATS match percentage based on skills, experience, and authorization.
    If you know anything specific about the company ({company_name}) that makes it a bad fit for an OPT Visa holder, factor that into the score.

    Return ONLY a raw JSON object:
    {{
        "ats_percentage": <integer between 0 and 100>,
        "missing_critical_skills": ["<skill_1>", "<skill_2>"],
        "decision_reason": "<1 short sentence explaining the score>"
    }}
    """
    try:
        response = ollama.chat(model=settings.OLLAMA_MODEL, messages=[{'role': 'user', 'content': prompt}])
        clean_text = response['message']['content'].strip().replace("```json", "").replace("```", "")
        result = json.loads(clean_text)
        
        # Add our custom logic to decide if we should apply
        ats_score = result.get("ats_percentage", 0)
        result["should_apply"] = ats_score >= settings.MIN_ATS_SCORE
        
        return result
    except Exception as e:
        return {"error": "Llama failed to parse ATS JSON", "raw": str(e), "should_apply": False}

if __name__ == "__main__":
    evaluate_job()