import ollama
import json
from config import settings

def evaluate_job(job_title, job_description):
    """Passes the scraped job to Llama 3.2 and scores it against your profile."""
    print(f"\n[Brain] Evaluating: {job_title}")
    
    prompt = f"""
    You are an autonomous career agent acting on behalf of a senior engineer.
    The candidate's profile: {settings.CANDIDATE_PROFILE}
    
    Analyze this job posting:
    Title: {job_title}
    Description: {job_description}

    Return ONLY a raw JSON object:
    {{
        "match_score": <1-100 integer>,
        "reason": "<1 short sentence explaining why it fits or doesn't fit>",
        "should_apply": <boolean>
    }}
    """
    try:
        response = ollama.chat(model=settings.OLLAMA_MODEL, messages=[{'role': 'user', 'content': prompt}])
        clean_text = response['message']['content'].strip().replace("```json", "").replace("```", "")
        return json.loads(clean_text)
    except Exception as e:
        return {"error": "Llama failed to parse", "raw": str(e)}

if __name__ == "__main__":
    evaluate_job()