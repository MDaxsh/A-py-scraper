#!/usr/bin/env python3
"""
============================================================
INDEED JOB SCRAPER - Main Entry Point
============================================================
Searches Indeed and saves basic job listings to jobs.json.
Then runs extract_details.py and extract_emails.py sequentially.

Usage:
    python3 run.py
============================================================
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

# Add config directory to path
sys.path.insert(0, str(Path(__file__).parent))

from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from config import IndeedConfig, PlaywrightConfig, IndeedSelectors
from utils import Logger, MouseHelper


async def search_indeed():
    """Search Indeed and save basic job listings."""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger = Logger(output_dir=str(output_dir))
    logger.start("INDEED JOB SEARCH")
    
    print("\n" + "=" * 60)
    print("🔍 INDEED JOB SEARCH")
    print("=" * 60)
    print(f"   Search: {IndeedConfig.SEARCH_QUERY}")
    print(f"   Location: {IndeedConfig.LOCATION}")
    print("=" * 60)
    
    try:
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(
                headless=PlaywrightConfig.HEADLESS,
                slow_mo=PlaywrightConfig.SLOW_MO
            )
            
            context = await browser.new_context(
                viewport={
                    "width": PlaywrightConfig.VIEWPORT_WIDTH,
                    "height": PlaywrightConfig.VIEWPORT_HEIGHT
                }
            )
            
            page = await context.new_page()
            
            # Apply stealth mode
            stealth = Stealth()
            await stealth.apply_stealth_async(page)
            page.set_default_timeout(PlaywrightConfig.DEFAULT_TIMEOUT)
            
            # Initialize mouse helper for human-like movements
            mouse = MouseHelper(page)
            
            logger.log("STEP 1", "Browser launched with stealth mode", "🚀")
            
            # Navigate to Indeed
            await page.goto(IndeedConfig.BASE_URL, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(1)
            
            # Brief human-like movement
            await mouse.idle_movement(0.5)
            logger.log("STEP 2", "Indeed homepage loaded", "✅")
            
            # Check for cookie consent or other overlays
            try:
                cookie_btn = page.locator('button[id="onetrust-accept-btn-handler"], button:has-text("Accept")')
                if await cookie_btn.count() > 0:
                    await mouse.human_click(cookie_btn.first)
                    await asyncio.sleep(1)
                    logger.log("INFO", "Closed cookie consent", "🍪")
            except:
                pass
            
            # Handle CAPTCHA/verification if it appears immediately
            title = await page.title()
            if "moment" in title.lower() or "verify" in title.lower() or "security" in title.lower():
                print("\n🔐 CAPTCHA detected! Please complete verification...")
                for i in range(60):
                    await asyncio.sleep(2)
                    title = await page.title()
                    if "moment" not in title.lower() and "verify" not in title.lower() and "security" not in title.lower():
                        logger.log("INFO", "Verification completed", "✅")
                        break
                    if i % 10 == 0:
                        print(f"   ⏳ Waiting... ({i*2}s)")
            
            # Random mouse movement before interacting
            await mouse.random_mouse_move()
            await asyncio.sleep(0.3)
            
            # Enter search query with human-like typing
            search_input = page.locator(IndeedSelectors.SEARCH_INPUT).first
            await mouse.human_click(search_input)
            await mouse.human_type(search_input, IndeedConfig.SEARCH_QUERY, click_first=False)
            logger.log("STEP 3", f"Search: {IndeedConfig.SEARCH_QUERY}", "⌨️")
            
            # Enter location with human-like typing
            location_input = page.locator(IndeedSelectors.LOCATION_INPUT).first
            await mouse.human_click(location_input)
            # Clear existing text
            await location_input.press("Control+a")
            await asyncio.sleep(0.05)
            await mouse.human_type(location_input, IndeedConfig.LOCATION, click_first=False)
            logger.log("STEP 4", f"Location: {IndeedConfig.LOCATION}", "📍")
            
            # Submit search with human-like click
            await asyncio.sleep(0.3)
            search_button = page.locator(IndeedSelectors.SEARCH_BUTTON).first
            await mouse.human_click(search_button)
            await asyncio.sleep(2)
            logger.log("STEP 5", "Search submitted", "🔍")
            
            # Handle CAPTCHA if needed
            title = await page.title()
            if "moment" in title.lower() or "verify" in title.lower():
                print("\n🔐 CAPTCHA detected! Please complete verification...")
                for i in range(30):
                    await asyncio.sleep(2)
                    title = await page.title()
                    if "moment" not in title.lower() and "verify" not in title.lower():
                        logger.log("STEP 6", "Verification completed", "✅")
                        break
            
            await asyncio.sleep(2)
            
            # Parse job listings
            jobs = []
            job_cards = await page.locator(IndeedSelectors.JOB_CARD).all()
            logger.log("STEP 7", f"Found {len(job_cards)} job cards", "📋")
            
            for idx, card in enumerate(job_cards):
                try:
                    # Job title
                    title_elem = card.locator(IndeedSelectors.JOB_TITLE).first
                    job_title = await title_elem.text_content() if await title_elem.count() > 0 else ""
                    job_title = job_title.strip() if job_title else ""
                    
                    # Company name
                    company_elem = card.locator(IndeedSelectors.COMPANY_NAME).first
                    company_name = await company_elem.text_content() if await company_elem.count() > 0 else ""
                    company_name = company_name.strip() if company_name else ""
                    
                    # Location
                    location_elem = card.locator(IndeedSelectors.COMPANY_LOCATION).first
                    job_location = await location_elem.text_content() if await location_elem.count() > 0 else ""
                    job_location = job_location.strip() if job_location else ""
                    
                    # Job link and ID
                    link_elem = card.locator(IndeedSelectors.JOB_LINK).first
                    job_link = ""
                    job_id = ""
                    
                    if await link_elem.count() > 0:
                        href = await link_elem.get_attribute('href')
                        if href:
                            job_link = f"{IndeedConfig.BASE_URL}{href}" if href.startswith('/') else href
                            if 'jk=' in href:
                                job_id = href.split('jk=')[1].split('&')[0]
                            elif 'vjk=' in href:
                                job_id = href.split('vjk=')[1].split('&')[0]
                    
                    if job_title:
                        jobs.append({
                            "job_title": job_title,
                            "job_location": job_location,
                            "job_id": job_id,
                            "job_link": job_link,
                            "salary": "",
                            "allows_c2c": False,
                            "company": {
                                "name": company_name,
                                "description": "",
                                "company_link": "",
                                "contact_email": "",
                                "phone_number": ""
                            }
                        })
                        logger.log("JOB", f"{idx+1}. {job_title} @ {company_name}", "💼")
                
                except Exception as e:
                    logger.log("ERROR", f"Parse error: {str(e)[:30]}", "⚠️")
                    continue
            
            # Save to JSON
            json_path = output_dir / "jobs.json"
            output = {
                "search_query": IndeedConfig.SEARCH_QUERY,
                "search_location": IndeedConfig.LOCATION,
                "scraped_at": datetime.now().isoformat(),
                "total_jobs": len(jobs),
                "details_extracted_at": "",
                "emails_extracted_at": "",
                "emails_found": 0,
                "c2c_jobs_found": 0,
                "jobs": jobs
            }
            
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            
            logger.log("SAVED", f"{len(jobs)} jobs saved to jobs.json", "✅")
            
            # Close browser
            await browser.close()
        
        logger.stop(success=True)
        
        print(f"\n✅ Search complete! Found {len(jobs)} jobs.")
        print(f"📊 Saved to: {output_dir / 'jobs.json'}")
        
        return True
        
    except Exception as e:
        logger.log("ERROR", f"{str(e)}", "❌")
        logger.stop(success=False)
        print(f"\n❌ Error: {str(e)}")
        return False


async def run_all():
    """Run all scripts sequentially with wait time between each."""
    
    print("\n" + "=" * 60)
    print("🚀 INDEED SCRAPER - FULL PIPELINE")
    print("=" * 60)
    
    # Step 1: Search Indeed
    print("\n📌 STEP 1/3: Searching Indeed...")
    success = await search_indeed()
    
    if not success:
        print("❌ Search failed. Stopping pipeline.")
        return
    
    # Wait before next step
    print("\n⏳ Waiting 5 seconds before extracting details...")
    await asyncio.sleep(5)
    
    # Step 2: Extract job details
    print("\n📌 STEP 2/3: Extracting job details...")
    from scripts.extract_details import extract_details
    await extract_details()
    
    # Wait before next step
    print("\n⏳ Waiting 5 seconds before extracting emails...")
    await asyncio.sleep(5)
    
    # Step 3: Extract emails
    print("\n📌 STEP 3/3: Extracting emails...")
    from scripts.extract_emails import extract_emails
    await extract_emails()
    
    print("\n" + "=" * 60)
    print("✅ PIPELINE COMPLETE!")
    print("📊 Results saved to: output/jobs.json")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(run_all())
