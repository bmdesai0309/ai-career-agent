import asyncio
import random
from playwright.async_api import async_playwright
from config import settings

class LinkedInNavigator:
    def __init__(self):
        self.playwright = None
        self.context = None
        self.page = None

    async def human_delay(self, min_sec=settings.MIN_HUMAN_DELAY_SEC, max_sec=settings.MAX_HUMAN_DELAY_SEC):
        """Mimics unpredictable human hesitation using parameters from settings.py."""
        delay = random.uniform(min_sec, max_sec)
        await asyncio.sleep(delay)

    async def human_scroll(self):
        """Mimics human reading behavior by scrolling unevenly."""
        print("[Action] Scrolling through page like a human...")
        for _ in range(random.randint(2, settings.MAX_PAGE_SCROLLS)):
            scroll_amount = random.randint(300, 800)
            await self.page.mouse.wheel(0, scroll_amount)
            await self.human_delay(1, 3)
        
        # Randomly scroll back up a little bit (humans often do this)
        await self.page.mouse.wheel(0, -random.randint(100, 300))
        await self.human_delay(1, 2)

    async def start_browser(self):
        """Launches the persistent, stealthy browser."""
        self.playwright = await async_playwright().start()
        
        # We load the persistent profile from the data folder to keep your cookies safe
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir="./data/linkedin_profile",
            headless=False, # CRITICAL: LinkedIn detects headless browsers instantly
            viewport={"width": 1280, "height": 800},
            args=["--disable-blink-features=AutomationControlled"] # Hides the bot flag
        )
        
        # A persistent context might already have a blank page open, so we use that or create a new one
        pages = self.context.pages
        self.page = pages[0] if pages else await self.context.new_page()
        
        print("[System] Browser launched in stealth mode.")

    async def login_check(self):
        """Navigates to LinkedIn and allows manual login on the first run."""
        print("[System] Checking LinkedIn session...")
        await self.page.goto("https://www.linkedin.com")
        await self.human_delay(3, 5)

        # Check if the URL indicates we are logged out
        if "login" in self.page.url or "guest" in self.page.url or "signup" in self.page.url:
            print("\n" + "="*60)
            print("🚨 MANUAL ACTION REQUIRED 🚨")
            print("You are not logged in. Please log in manually in the open browser.")
            print("The script will pause for 90 seconds to let you do this...")
            print("="*60 + "\n")
            await asyncio.sleep(90) 
        else:
            print("[System] Active login session verified.")

    async def search_jobs(self, query):
        """Constructs the search URL and navigates to it."""
        print(f"[Action] Searching for: '{query}' in {settings.LOCATION}")
        
        # Format the URL properly for LinkedIn
        encoded_query = query.replace(" ", "%20")
        encoded_location = settings.LOCATION.replace(" ", "%20")
        url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_query}&location={encoded_location}"
        
        await self.page.goto(url)
        await self.human_delay(4, 7)
        await self.human_scroll()
        
        # Find all the job cards on the left-hand side
        job_cards = await self.page.locator(".job-card-container").all()
        print(f"[System] Found {len(job_cards)} job listings on this page.")
        return job_cards

    async def close(self):
        """Gracefully shuts down the browser to save cookies properly."""
        print("[System] Shutting down browser gracefully...")
        if self.context:
            await self.context.close()
        if self.playwright:
            await self.playwright.stop()