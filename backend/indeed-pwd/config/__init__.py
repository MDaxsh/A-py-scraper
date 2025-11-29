"""
============================================================
CONFIGURATION LOADER
============================================================
This module loads settings from the .env files and makes them
available as Python classes for easy access in the code.
============================================================
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Get the directory where this file is located
CONFIG_DIR = Path(__file__).parent

# Load Indeed settings from indeed_config.env
load_dotenv(CONFIG_DIR / "indeed_config.env")

# Load Playwright settings from playwright_config.env
load_dotenv(CONFIG_DIR / "playwright_config.env")


class IndeedConfig:
    """
    Indeed website settings.
    Access these values like: IndeedConfig.BASE_URL
    """
    BASE_URL = os.getenv("INDEED_BASE_URL", "https://www.indeed.com")
    SEARCH_QUERY = os.getenv("INDEED_SEARCH_QUERY", "python developer")
    LOCATION = os.getenv("INDEED_LOCATION", "Remote")
    JOB_TYPE = os.getenv("INDEED_JOB_TYPE", "")
    DATE_POSTED = os.getenv("INDEED_DATE_POSTED", "")


class PlaywrightConfig:
    """
    Playwright browser settings.
    Access these values like: PlaywrightConfig.HEADLESS
    """
    BROWSER = os.getenv("PLAYWRIGHT_BROWSER", "chromium")
    HEADLESS = os.getenv("PLAYWRIGHT_HEADLESS", "false").lower() == "true"
    SLOW_MO = int(os.getenv("PLAYWRIGHT_SLOW_MO", "1000"))
    VIEWPORT_WIDTH = int(os.getenv("PLAYWRIGHT_VIEWPORT_WIDTH", "1280"))
    VIEWPORT_HEIGHT = int(os.getenv("PLAYWRIGHT_VIEWPORT_HEIGHT", "800"))
    DEFAULT_TIMEOUT = int(os.getenv("PLAYWRIGHT_DEFAULT_TIMEOUT", "30000"))
    NAVIGATION_TIMEOUT = int(os.getenv("PLAYWRIGHT_NAVIGATION_TIMEOUT", "60000"))
    SCREENSHOTS = os.getenv("PLAYWRIGHT_SCREENSHOTS", "true").lower() == "true"
    SCREENSHOT_DIR = os.getenv("PLAYWRIGHT_SCREENSHOT_DIR", "./output/screenshots")
