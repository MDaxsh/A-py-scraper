#!/usr/bin/env python3
"""
============================================================
JOB DETAILS EXTRACTOR
============================================================
Reads jobs.json and visits each job's detail page to extract:
- Company data (name, description, link, contact_email, phone_number)
- Salary information
- C2C (Corp-to-Corp) availability

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

# Add config directory to path
sys.path.insert(0, str(Path(__file__).parent))

from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from config import PlaywrightConfig, IndeedSelectors
from utils import Logger


async def extract_emails():
    """Visit each job link and extract detailed information."""
    
    # Initialize paths
    output_dir = Path(__file__).parent / "output"
    screenshot_dir = Path(PlaywrightConfig.SCREENSHOT_DIR)
    jobs_file = output_dir / "jobs.json"
    
    # Check if jobs.json exists
    if not jobs_file.exists():
        print("❌ Error: jobs.json not found!")
        print("   Please run 'python3 run.py' first to generate jobs.json")
        return
    
    # Load jobs data
    with open(jobs_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    jobs = data.get("jobs", [])
    
    if not jobs:
        print("❌ No jobs found in jobs.json")
        return
    
    # Initialize logger
    logger = Logger(output_dir=str(output_dir))
    logger.start("JOB DETAILS EXTRACTOR")
    
    print("\n" + "=" * 60)
    print("📧 JOB DETAILS EXTRACTOR")
    print("=" * 60)
    
    logger.log("INFO", f"Found {len(jobs)} jobs to process", "📋")
    logger.separator("-")
    
    emails_found = 0
    c2c_found = 0
    
    try:
        async with async_playwright() as p:
            # Launch browser
            logger.log("STEP 1", "Launching browser...", "🚀")
            
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
            
            logger.log("STEP 1", "Browser ready!", "✅")
            logger.separator("-")
            
            # Process each job
            for idx, job in enumerate(jobs):
                job_title = job.get("job_title", "Unknown")
                company = job.get("company", "Unknown")
                job_link = job.get("job_link", "")
                
                logger.log(f"JOB {idx+1}/{len(jobs)}", f"{job_title} @ {company}", "🔍")
                
                if not job_link:
                    logger.log("SKIP", "No job link available", "⚠️")
                    continue
                
                try:
                    # Navigate to job detail page
                    await page.goto(job_link, wait_until="domcontentloaded", timeout=30000)
                    await asyncio.sleep(2)
                    
                    # Check for CAPTCHA
                    title = await page.title()
                    if "moment" in title.lower() or "verify" in title.lower():
                        logger.log("CAPTCHA", "Verification needed - waiting 30s...", "🤖")
                        print("   👆 Please complete verification in browser!")
                        await asyncio.sleep(30)
                    
                    # Get full page text
                    page_text = await page.text_content("body") or ""
                    page_text_lower = page_text.lower()
                    
                    # ---------------------------------------------------------
                    # Initialize Company Object
                    # ---------------------------------------------------------
                    company_data = {
                        "name": job.get("company", ""),
                        "description": "",
                        "link": "",
                        "contact_email": "",
                        "phone_number": ""
                    }
                    
                    # ---------------------------------------------------------
                    # Extract Salary
                    # ---------------------------------------------------------
                    salary = ""
                    # Look for salary patterns like $XX,XXX - $XX,XXX or $XX/hour
                    salary_patterns = [
                        r'\$[\d,]+(?:\.\d{2})?\s*[-–to]+\s*\$[\d,]+(?:\.\d{2})?\s*(?:per\s+)?(?:year|annually|a\s+year|yr)?',
                        r'\$[\d,]+(?:\.\d{2})?\s*[-–to]+\s*\$[\d,]+(?:\.\d{2})?\s*(?:per\s+)?(?:hour|hr|hourly)?',
                        r'\$[\d,]+(?:\.\d{2})?\s*(?:per\s+)?(?:year|annually|a\s+year|hour|hr)',
                        r'\$[\d,]+\s*-\s*\$[\d,]+',
                    ]
                    for pattern in salary_patterns:
                        salary_match = re.search(pattern, page_text, re.IGNORECASE)
                        if salary_match:
                            salary = salary_match.group(0).strip()
                            break
                    
                    if salary:
                        job["salary"] = salary
                        logger.log("SALARY", f"{salary}", "💰")
                    
                    # ---------------------------------------------------------
                    # Extract Company Link
                    # ---------------------------------------------------------
                    try:
                        # Look for company name link on Indeed job page
                        company_link_elem = page.locator('a[data-testid="inlineHeader-companyName"], a[data-tn-element="companyName"], div.jobsearch-CompanyInfoWithoutHeaderImage a').first
                        if await company_link_elem.count() > 0:
                            href = await company_link_elem.get_attribute('href')
                            if href:
                                company_data["link"] = f"https://www.indeed.com{href}" if href.startswith('/') else href
                                logger.log("COMPANY", f"Link found", "🔗")
                    except:
                        pass
                    
                    # ---------------------------------------------------------
                    # Extract Company Description
                    # ---------------------------------------------------------
                    try:
                        # Look for company description on job page
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
                                    # Get first 500 chars as description summary
                                    company_data["description"] = full_desc.strip()[:500]
                                    logger.log("DESC", f"Description extracted ({len(company_data['description'])} chars)", "📝")
                                    break
                    except:
                        pass
                    
                    # ---------------------------------------------------------
                    # Extract Phone Number
                    # ---------------------------------------------------------
                    phone_patterns = [
                        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # (123) 456-7890 or 123-456-7890
                        r'\+1[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # +1 (123) 456-7890
                        r'\d{3}[-.\s]\d{3}[-.\s]\d{4}',  # 123.456.7890
                    ]
                    for pattern in phone_patterns:
                        phone_match = re.search(pattern, page_text)
                        if phone_match:
                            company_data["phone_number"] = phone_match.group(0).strip()
                            logger.log("PHONE", f"{company_data['phone_number']}", "📞")
                            break
                    
                    # ---------------------------------------------------------
                    # Check for C2C (Corp-to-Corp) availability
                    # ---------------------------------------------------------
                    c2c_keywords = [
                        'c2c', 'corp to corp', 'corp-to-corp', 'c-2-c',
                        'contract to contract', '1099', 'corp 2 corp'
                    ]
                    allows_c2c = False
                    for keyword in c2c_keywords:
                        if keyword in page_text_lower:
                            allows_c2c = True
                            break
                    
                    job["allows_c2c"] = allows_c2c
                    if allows_c2c:
                        c2c_found += 1
                        logger.log("C2C", "Corp-to-Corp allowed!", "✅")
                    
                    # ---------------------------------------------------------
                    # Extract Contact Emails
                    # ---------------------------------------------------------
                    email_pattern = IndeedSelectors.EMAIL_PATTERN
                    emails = re.findall(email_pattern, page_text)
                    
                    # Filter out common false positives
                    filtered_emails = []
                    excluded_domains = [
                        "indeed.com", "sentry.io", "example.com", 
                        "email.com", "company.com", "domain.com",
                        "yourcompany.com", "youremail.com"
                    ]
                    
                    for email in emails:
                        email_lower = email.lower()
                        is_valid = True
                        
                        for excluded in excluded_domains:
                            if excluded in email_lower:
                                is_valid = False
                                break
                        
                        if is_valid and email_lower not in [e.lower() for e in filtered_emails]:
                            filtered_emails.append(email)
                    
                    if filtered_emails:
                        # Use the first valid email found
                        company_data["contact_email"] = filtered_emails[0]
                        emails_found += 1
                        logger.log("EMAIL", f"{filtered_emails[0]}", "📧")
                        
                        # Log additional emails if found
                        if len(filtered_emails) > 1:
                            logger.log("INFO", f"Additional emails: {', '.join(filtered_emails[1:])}", "📧")
                    else:
                        logger.log("EMAIL", "No email found on this page", "➖")
                    
                    # ---------------------------------------------------------
                    # Add Company Object to Job
                    # ---------------------------------------------------------
                    job["company"] = company_data
                    
                except Exception as e:
                    logger.log("ERROR", f"Failed to process: {str(e)[:50]}", "❌")
                    continue
                
                # Small delay between requests
                await asyncio.sleep(1)
            
            logger.separator("-")
            logger.log("CLEANUP", "Closing browser...", "🧹")
            await browser.close()
        
        # Save updated jobs data
        data["jobs"] = jobs
        data["details_extracted_at"] = datetime.now().isoformat()
        data["emails_found"] = emails_found
        data["c2c_jobs_found"] = c2c_found
        
        with open(jobs_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.log("SAVED", f"Updated jobs.json", "✅")
        logger.stop(success=True)
        
        print("\n" + "=" * 60)
        print("✅ JOB DETAILS EXTRACTION COMPLETED")
        print(f"📧 Emails found: {emails_found}/{len(jobs)}")
        print(f"🤝 C2C jobs found: {c2c_found}/{len(jobs)}")
        print(f"📊 Updated: {jobs_file}")
        print("=" * 60 + "\n")
        
    except Exception as e:
        logger.log("ERROR", f"An error occurred: {str(e)}", "❌")
        logger.stop(success=False)
        raise


if __name__ == "__main__":
    print("\n🚀 Starting Job Details Extractor...\n")
    asyncio.run(extract_emails())
