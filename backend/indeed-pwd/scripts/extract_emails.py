#!/usr/bin/env python3
"""
============================================================
EXTRACT EMAILS
============================================================
Reads jobs.json and extracts contact emails from job pages.
This is a focused script that only extracts emails.

Usage:
    python3 extract_emails.py
============================================================
"""

import asyncio
import sys
import json
import re
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from config import PlaywrightConfig, IndeedSelectors
from utils import Logger, MouseHelper


async def extract_emails():
    """Extract contact emails from each job page."""
    
    # Use parent.parent to get indeed-pwd folder
    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / "output"
    jobs_file = output_dir / "jobs.json"
    
    # Check if jobs.json exists
    if not jobs_file.exists():
        print("❌ jobs.json not found! Run 'python3 run.py' first.")
        return
    
    # Load jobs
    with open(jobs_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    jobs = data.get("jobs", [])
    if not jobs:
        print("❌ No jobs found in jobs.json")
        return
    
    logger = Logger(output_dir=str(output_dir))
    logger.start("EXTRACT EMAILS")
    
    print("\n" + "=" * 60)
    print("📧 EXTRACT EMAILS")
    print(f"   Processing {len(jobs)} jobs...")
    print("=" * 60)
    
    emails_found = 0
    
    try:
        async with async_playwright() as p:
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
            stealth = Stealth()
            await stealth.apply_stealth_async(page)
            page.set_default_timeout(PlaywrightConfig.DEFAULT_TIMEOUT)
            
            # Initialize mouse helper for human-like movements
            mouse = MouseHelper(page)
            
            logger.log("READY", "Browser launched", "🚀")
            
            for idx, job in enumerate(jobs):
                job_title = job.get("job_title", "Unknown")
                job_link = job.get("job_link", "")
                
                logger.log(f"JOB {idx+1}/{len(jobs)}", f"{job_title[:30]}", "🔍")
                
                if not job_link:
                    continue
                
                try:
                    await page.goto(job_link, wait_until="domcontentloaded", timeout=30000)
                    await asyncio.sleep(1)
                    
                    # Brief human-like movement
                    await mouse.idle_movement(0.3)
                    
                    # Handle CAPTCHA
                    title = await page.title()
                    if "moment" in title.lower() or "verify" in title.lower():
                        print("   🔐 CAPTCHA - please verify in browser...")
                        await asyncio.sleep(30)
                    
                    page_text = await page.text_content("body") or ""
                    
                    # Extract emails
                    email_pattern = IndeedSelectors.EMAIL_PATTERN
                    emails = re.findall(email_pattern, page_text)
                    
                    # Filter out false positives
                    excluded_domains = [
                        "indeed.com", "sentry.io", "example.com",
                        "email.com", "company.com", "domain.com",
                        "yourcompany.com", "youremail.com"
                    ]
                    
                    filtered_emails = []
                    for email in emails:
                        email_lower = email.lower()
                        is_valid = all(exc not in email_lower for exc in excluded_domains)
                        if is_valid and email_lower not in [e.lower() for e in filtered_emails]:
                            filtered_emails.append(email)
                    
                    if filtered_emails:
                        job["company"]["contact_email"] = filtered_emails[0]
                        emails_found += 1
                        logger.log("EMAIL", f"{filtered_emails[0]}", "📧")
                    else:
                        logger.log("EMAIL", "No email found", "➖")
                    
                except Exception as e:
                    logger.log("ERROR", f"{str(e)[:40]}", "❌")
                    continue
                
                # Quick scroll between jobs
                await mouse.scroll_naturally()
                await asyncio.sleep(0.5)
            
            await browser.close()
        
        # Save updated data
        data["jobs"] = jobs
        data["emails_extracted_at"] = datetime.now().isoformat()
        data["emails_found"] = emails_found
        
        with open(jobs_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.stop(success=True)
        
        print(f"\n✅ Email extraction complete!")
        print(f"📧 Emails found: {emails_found}/{len(jobs)}")
        
    except Exception as e:
        logger.log("ERROR", f"{str(e)}", "❌")
        logger.stop(success=False)
        raise


if __name__ == "__main__":
    print("\n🚀 Starting Email Extractor...\n")
    asyncio.run(extract_emails())
