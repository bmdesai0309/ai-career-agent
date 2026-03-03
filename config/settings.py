import os

# ==========================================
# 1. JOB SEARCH PARAMETERS
# ==========================================
# The exact search queries the agent will type into LinkedIn
TARGET_ROLES = [
    "AI Engineer GCP",
    "Machine Learning Engineer Google Cloud",
    "MLOps Engineer"
]

LOCATION = "United States"

# ==========================================
# 2. THE AI CONTEXT (YOUR PROFILE)
# ==========================================
# Llama 3.2 uses this exact prompt to evaluate if a job is worth applying to.
CANDIDATE_PROFILE = """
- 6+ years of experience as a Data Engineer.
- Masters in Computer Science.
- Currently authorized to work in the US on an OPT visa.
- Primary Career Goal: Transitioning to an AI Engineer role, with a strong preference for Google Cloud Platform (GCP) ecosystems.
"""

# ==========================================
# 3. FILTERING RULES (THE GUARDRAILS)
# ==========================================
# If a job description lacks these, the agent scores it lower
MUST_HAVE_KEYWORDS = ["GCP", "Google Cloud", "Vertex", "AI", "Python", "Machine Learning", "LLM"]

# Instantly reject jobs with these keywords (saves AI processing time)
# E.g., skipping defense jobs since they require citizenship/clearances
EXCLUDE_KEYWORDS = ["Top Secret", "Clearance Required", "US Citizen Only", "Green Card Only"]

# ==========================================
# 4. SAFETY & STEALTH LIMITS (CRITICAL)
# ==========================================
# Do NOT increase these numbers dramatically. 
# LinkedIn will flag the account if it behaves too fast.
MAX_DAILY_APPLICATIONS = 2    # Start low to warm up the script
MAX_PAGE_SCROLLS = 3           # How deep to scroll on the search page
MIN_HUMAN_DELAY_SEC = 3        # Minimum wait time between clicks
MAX_HUMAN_DELAY_SEC = 9        # Maximum wait time between clicks

# ==========================================
# 5. LOCAL AI CONFIGURATION
# ==========================================
OLLAMA_MODEL = "llama3.2"
OLLAMA_URL = "http://localhost:11434"