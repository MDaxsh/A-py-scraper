#!/usr/bin/env python3
"""
============================================================
EXTRACT JOB DETAILS
============================================================
Reads jobs.json and visits each job page to extract:
- Company description
- Company link
- Salary information
- Phone number
- C2C (Corp-to-Corp) availability

Usage:
    python3 extract_details.py
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
from config import PlaywrightConfig
from utils import Logger, MouseHelper


async def extract_details():
    """Extract detailed information from each job page."""
    
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
    logger.start("EXTRACT JOB DETAILS")
    
    print("\n" + "=" * 60)
    print("📋 EXTRACT JOB DETAILS")
    print(f"   Processing {len(jobs)} jobs...")
    print("=" * 60)
    
    c2c_found = 0
    
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
                company_name = job.get("company", {}).get("name", "Unknown")
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
                    page_text_lower = page_text.lower()
                    
                    # Extract Salary
                    salary_patterns = [
                        r'\$[\d,]+(?:\.\d{2})?\s*[-–to]+\s*\$[\d,]+(?:\.\d{2})?\s*(?:per\s+)?(?:year|annually|a\s+year|yr)?',
                        r'\$[\d,]+(?:\.\d{2})?\s*[-–to]+\s*\$[\d,]+(?:\.\d{2})?\s*(?:per\s+)?(?:hour|hr|hourly)?',
                        r'\$[\d,]+(?:\.\d{2})?\s*(?:per\s+)?(?:year|annually|a\s+year|hour|hr)',
                        r'\$[\d,]+\s*-\s*\$[\d,]+',
                    ]
                    for pattern in salary_patterns:
                        match = re.search(pattern, page_text, re.IGNORECASE)
                        if match:
                            job["salary"] = match.group(0).strip()
                            logger.log("SALARY", f"{job['salary']}", "💰")
                            break
                    
                    # Extract Company Link
                    try:
                        link_elem = page.locator('a[data-testid="inlineHeader-companyName"], a[data-tn-element="companyName"], div.jobsearch-CompanyInfoWithoutHeaderImage a').first
                        if await link_elem.count() > 0:
                            href = await link_elem.get_attribute('href')
                            if href:
                                job["company"]["company_link"] = f"https://www.indeed.com{href}" if href.startswith('/') else href
                                logger.log("LINK", "Company link found", "🔗")
                    except:
                        pass
                    
                    # Extract Company Description
                    try:
                        desc_selectors = [
                            'div[data-testid="jobDescriptionText"]',
                            'div#jobDescriptionText',
                            'div.jobsearch-jobDescriptionText'
                        ]
                        for selector in desc_selectors:
                            desc_elem = page.locator(selector).first
                            if await desc_elem.count() > 0:
                                full_desc = await desc_elem.text_content()
                                if full_desc:
                                    job["company"]["description"] = full_desc.strip()[:500]
                                    logger.log("DESC", f"{len(job['company']['description'])} chars", "📝")
                                    break
                    except:
                        pass
                    
                    # Extract Phone Number
                    phone_patterns = [
                        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
                        r'\+1[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
                    ]
                    for pattern in phone_patterns:
                        match = re.search(pattern, page_text)
                        if match:
                            job["company"]["phone_number"] = match.group(0).strip()
                            logger.log("PHONE", f"{job['company']['phone_number']}", "📞")
                            break
                    
                    # Check for C2C
                    c2c_keywords = ['c2c', 'corp to corp', 'corp-to-corp', 'c-2-c', '1099', 'corp 2 corp']
                    for keyword in c2c_keywords:
                        if keyword in page_text_lower:
                            job["allows_c2c"] = True
                            c2c_found += 1
                            logger.log("C2C", "Allowed!", "✅")
                            break
                    
                except Exception as e:
                    logger.log("ERROR", f"{str(e)[:40]}", "❌")
                    continue
                
                # Quick scroll between jobs
                await mouse.scroll_naturally()
                await asyncio.sleep(0.5)
            
            await browser.close()
        
        # Save updated data
        data["jobs"] = jobs
        data["details_extracted_at"] = datetime.now().isoformat()
        data["c2c_jobs_found"] = c2c_found
        
        with open(jobs_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.stop(success=True)
        
        print(f"\n✅ Details extracted!")
        print(f"🤝 C2C jobs found: {c2c_found}/{len(jobs)}")
        
    except Exception as e:
        logger.log("ERROR", f"{str(e)}", "❌")
        logger.stop(success=False)
        raise


if __name__ == "__main__":
    print("\n🚀 Starting Job Details Extractor...\n")
    asyncio.run(extract_details())
