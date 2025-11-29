#!/usr/bin/env python3
"""
============================================================
INDEED PAGE LOADER
============================================================
A simple script to load the Indeed website using Playwright.
Watch the browser open and navigate to Indeed!

Usage:
    python3 run.py
============================================================
"""

import asyncio
import sys
from pathlib import Path

# Add config directory to path
sys.path.insert(0, str(Path(__file__).parent))

from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from config import IndeedConfig, PlaywrightConfig
from utils import Logger


async def load_indeed():
    """Load the Indeed website and perform a search."""
    
    # Initialize logger
    output_dir = Path(__file__).parent / "output"
    screenshot_dir = Path(PlaywrightConfig.SCREENSHOT_DIR)
    
    logger = Logger(output_dir=str(output_dir))
    
    # Create output directories
    output_dir.mkdir(parents=True, exist_ok=True)
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    # Clear old screenshots before starting
    for old_screenshot in screenshot_dir.glob("*.png"):
        old_screenshot.unlink()
    
    # Start logging
    logger.start("INDEED PAGE LOADER")
    
    print("\n" + "=" * 60)
    print("🔍 INDEED PAGE LOADER")
    print("=" * 60)
    
    logger.log("CONFIG", f"Browser: {PlaywrightConfig.BROWSER}", "🌐")
    logger.log("CONFIG", f"Headless: {PlaywrightConfig.HEADLESS}", "👁️")
    logger.log("CONFIG", f"Slow Mo: {PlaywrightConfig.SLOW_MO}ms", "🐌")
    logger.log("CONFIG", f"Search: {IndeedConfig.SEARCH_QUERY}", "🔎")
    logger.log("CONFIG", f"Location: {IndeedConfig.LOCATION}", "📍")
    
    logger.separator("-")
    
    try:
        async with async_playwright() as p:
            # ---------------------------------------------------------
            # STEP 1: Launch Browser
            # ---------------------------------------------------------
            logger.log("STEP 1", "Launching browser...", "🚀")
            
            browser = await p.chromium.launch(
                headless=PlaywrightConfig.HEADLESS,
                slow_mo=PlaywrightConfig.SLOW_MO
            )
            
            logger.log("STEP 1", "Browser launched successfully!", "✅")
            
            # ---------------------------------------------------------
            # STEP 2: Create Browser Context & Page
            # ---------------------------------------------------------
            logger.log("STEP 2", "Creating browser context...", "📄")
            
            context = await browser.new_context(
                viewport={
                    "width": PlaywrightConfig.VIEWPORT_WIDTH,
                    "height": PlaywrightConfig.VIEWPORT_HEIGHT
                }
            )
            
            page = await context.new_page()
            
            # Apply stealth mode to bypass bot detection
            stealth = Stealth()
            await stealth.apply_stealth_async(page)
            logger.log("STEP 2", "Stealth mode applied!", "🥷")
            
            page.set_default_timeout(PlaywrightConfig.DEFAULT_TIMEOUT)
            
            logger.log("STEP 2", "Browser context ready!", "✅")
            
            # ---------------------------------------------------------
            # STEP 3: Navigate to Indeed Homepage
            # ---------------------------------------------------------
            logger.log("STEP 3", f"Navigating to {IndeedConfig.BASE_URL}...", "🌐")
            
            await page.goto(IndeedConfig.BASE_URL, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(2)  # Wait for page to settle
            
            logger.log("STEP 3", "Indeed homepage loaded!", "✅")
            
            if PlaywrightConfig.SCREENSHOTS:
                screenshot_path = screenshot_dir / "01_homepage.png"
                await page.screenshot(path=str(screenshot_path))
                logger.log("SCREENSHOT", f"Saved: {screenshot_path}", "📸")
            
            # ---------------------------------------------------------
            # STEP 4: Enter Search Query
            # ---------------------------------------------------------
            logger.log("STEP 4", f"Entering search query: '{IndeedConfig.SEARCH_QUERY}'...", "⌨️")
            
            # Find and fill the search input
            search_input = page.locator('input[id="text-input-what"], input[name="q"]').first
            await search_input.click()
            await search_input.fill(IndeedConfig.SEARCH_QUERY)
            
            logger.log("STEP 4", "Search query entered!", "✅")
            
            # ---------------------------------------------------------
            # STEP 5: Enter Location
            # ---------------------------------------------------------
            logger.log("STEP 5", f"Entering location: '{IndeedConfig.LOCATION}'...", "📍")
            
            # Find and fill the location input
            location_input = page.locator('input[id="text-input-where"], input[name="l"]').first
            await location_input.click()
            await location_input.clear()
            await location_input.fill(IndeedConfig.LOCATION)
            
            logger.log("STEP 5", "Location entered!", "✅")
            
            if PlaywrightConfig.SCREENSHOTS:
                screenshot_path = screenshot_dir / "02_search_filled.png"
                await page.screenshot(path=str(screenshot_path))
                logger.log("SCREENSHOT", f"Saved: {screenshot_path}", "📸")
            
            # ---------------------------------------------------------
            # STEP 6: Submit Search
            # ---------------------------------------------------------
            logger.log("STEP 6", "Submitting search...", "🔍")
            
            # Click the search button
            search_button = page.locator('button[type="submit"]').first
            await search_button.click()
            
            # Wait a bit for page to start loading
            await asyncio.sleep(3)
            
            logger.log("STEP 6", "Search submitted!", "✅")
            
            # ---------------------------------------------------------
            # STEP 7: Handle CAPTCHA/Human Verification
            # ---------------------------------------------------------
            title = await page.title()
            
            if "moment" in title.lower() or "verify" in title.lower() or "captcha" in title.lower():
                logger.log("STEP 7", "Human verification detected!", "🤖")
                logger.separator("-")
                print("🔐 CAPTCHA/VERIFICATION DETECTED")
                logger.separator("-")
                print("👆 Please complete the verification in the browser window!")
                print("⏳ Waiting for you to verify (up to 60 seconds)...")
                logger.separator("-")
                
                if PlaywrightConfig.SCREENSHOTS:
                    screenshot_path = screenshot_dir / "03_captcha_detected.png"
                    await page.screenshot(path=str(screenshot_path))
                    logger.log("SCREENSHOT", f"Saved: {screenshot_path}", "📸")
                
                # Wait for the verification to complete (check every 2 seconds)
                for i in range(30):  # 30 attempts x 2 seconds = 60 seconds max
                    await asyncio.sleep(2)
                    title = await page.title()
                    
                    # Check if we're past the verification
                    if "moment" not in title.lower() and "verify" not in title.lower():
                        logger.log("STEP 7", "Verification completed!", "✅")
                        break
                    
                    if i % 5 == 0:  # Every 10 seconds
                        print(f"   ⏳ Still waiting... ({(i+1)*2} seconds)")
                else:
                    logger.log("STEP 7", "Verification timeout - continuing anyway", "⚠️")
            else:
                logger.log("STEP 7", "No verification needed!", "✅")
            
            # ---------------------------------------------------------
            # STEP 8: View Search Results
            # ---------------------------------------------------------
            logger.log("STEP 8", "Viewing search results page...", "📋")
            
            # Get the page title
            title = await page.title()
            logger.log("PAGE INFO", f"Title: {title}", "📄")
            
            # Get current URL
            current_url = page.url
            logger.log("PAGE INFO", f"URL: {current_url}", "🔗")
            
            if PlaywrightConfig.SCREENSHOTS:
                screenshot_path = screenshot_dir / "04_search_results.png"
                await page.screenshot(path=str(screenshot_path), full_page=True)
                logger.log("SCREENSHOT", f"Saved: {screenshot_path}", "📸")
            
            # ---------------------------------------------------------
            # STEP 9: Keep Browser Open for Viewing
            # ---------------------------------------------------------
            logger.separator("-")
            logger.log("DONE", "Indeed loaded successfully!", "🎉")
            logger.separator("-")
            
            if not PlaywrightConfig.HEADLESS:
                print("\n👀 Browser is open - take a look!")
                print("⏳ Press Ctrl+C to close or wait 30 seconds...")
                await asyncio.sleep(30)
            
            # ---------------------------------------------------------
            # STEP 10: Cleanup
            # ---------------------------------------------------------
            logger.log("CLEANUP", "Closing browser...", "🧹")
            await browser.close()
            logger.log("CLEANUP", "Browser closed!", "✅")
        
        # Stop logging (success)
        logger.stop(success=True)
        
        print("\n" + "=" * 60)
        print("✅ SCRIPT COMPLETED")
        print(f"📁 Screenshots saved to: {screenshot_dir}")
        print(f"📄 Log saved to: {logger.get_log_path()}")
        print("=" * 60 + "\n")
        
    except Exception as e:
        logger.log("ERROR", f"An error occurred: {str(e)}", "❌")
        logger.stop(success=False)
        raise


if __name__ == "__main__":
    print("\n🚀 Starting Indeed Page Loader...\n")
    asyncio.run(load_indeed())
