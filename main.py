import asyncio
import json
from config import settings
from browser.linkedin_navigator import LinkedInNavigator
from agents.job_evaluator import evaluate_job # We will update this import shortly


async def run_agent():
    print(f"=== Starting SynapseDev Career Agent ===")
    print(f"Target Roles: {settings.TARGET_ROLES}")
    print(f"Daily Application Limit: {settings.MAX_DAILY_APPLICATIONS}\n")

    navigator = LinkedInNavigator()
    applications_sent_today = 0

    try:
        # 1. Wake up the body
        await navigator.start_browser()
        await navigator.login_check()

        # 2. Loop through your target job titles
        for role in settings.TARGET_ROLES:
            if applications_sent_today >= settings.MAX_DAILY_APPLICATIONS:
                print(f"[System] Reached daily safety limit of {settings.MAX_DAILY_APPLICATIONS} applications. Stopping.")
                break

            # 3. Perform the search
            job_cards = await navigator.search_jobs(role)
            
            if not job_cards:
                print(f"[Warning] No jobs found for '{role}'. Moving to next role.")
                continue

            # 4. Analyze the top 3 jobs for this role to stay under radar
            for card in job_cards[:3]:
                if applications_sent_today >= settings.MAX_DAILY_APPLICATIONS:
                    break

                # Click the job card to load the description on the right panel
                await card.click()
                await navigator.human_delay(2, 4)

                try:
                    # Extract the Title and Description
                    job_title_element = navigator.page.locator(".job-details-jobs-unified-top-card__job-title")
                    job_title = await job_title_element.text_content() if await job_title_element.count() > 0 else "Unknown Title"
                    
                    # NEW: Extract the Company Name
                    company_element = navigator.page.locator(".job-details-jobs-unified-top-card__company-name")
                    company_name = await company_element.text_content() if await company_element.count() > 0 else "Unknown Company"
                    
                    # Clean up the text (removes weird spacing and newlines)
                    job_title = job_title.strip()
                    company_name = company_name.strip()
                    
                    job_desc_element = navigator.page.locator("#job-details")
                    await job_desc_element.wait_for(timeout=5000)
                    job_description = await job_desc_element.text_content()

                    # 5. Fast Keyword Filtering (Saves AI processing time)
                    desc_upper = job_description.upper()
                    if any(exclude.upper() in desc_upper for exclude in settings.EXCLUDE_KEYWORDS):
                        print(f"[Filter] Skipping '{job_title.strip()}' - Contains Excluded Keyword.")
                        continue

                    # 6. Deep AI Evaluation
                    # Truncate description slightly to keep local inference fast
                    decision = evaluate_job(job_title, company_name, job_description.strip()[:2500])
                    
                    print(f"  -> Company: {company_name}")
                    print(f"  -> ATS Match: {decision.get('ats_percentage', 'N/A')}%")
                    print(f"  -> Missing Skills: {', '.join(decision.get('missing_critical_skills', []))}")
                    print(f"  -> Reason: {decision.get('decision_reason', 'N/A')}")
                    
                    if decision.get("should_apply"):
                        print(f"  -> [Action] Passed {settings.MIN_ATS_SCORE}% threshold! Applying...")
                        applications_sent_today += 1
                        # TODO: Add the Easy Apply click logic here
                    else:
                        print("  -> [Action] ATS score too low. Skipping.")

                except Exception as e:
                    print(f"[Error] Failed to process a job card: {e}")
                    continue

                # Pause before clicking the next job card
                await navigator.human_delay(3, 6)

    except Exception as e:
        print(f"\n[Critical Error] The agent encountered a fatal issue: {e}")
    finally:
        # 7. Go to sleep
        await navigator.close()
        print("\n=== Agent Shutdown Sequence Complete ===")

if __name__ == "__main__":
    # Ensure Ollama is running in the background before starting!
    asyncio.run(run_agent())