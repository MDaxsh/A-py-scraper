# Indeed Page Loader

A simple Playwright-based script to load and interact with the Indeed job search website. Uses stealth mode to bypass bot detection.

## Features

- 🥷 **Stealth Mode** - Bypasses CAPTCHA and bot detection using `playwright-stealth`
- 📸 **Screenshots** - Captures screenshots at each step
- 📄 **Logging** - Detailed step-by-step logs saved to `output/log.txt`
- ⚙️ **Configurable** - Separate config files for Indeed and Playwright settings

## Project Structure

```
indeed-pwd/
├── config/
│   ├── __init__.py           # Loads env files into Python config classes
│   ├── indeed_config.env     # Indeed website settings (URL, search query, location)
│   ├── playwright_config.env # Browser settings (headless, slow_mo, viewport size)
│   └── page_selectors.py     # CSS selectors for Indeed page elements
├── utils/
│   ├── __init__.py           # Exports Logger class
│   └── logger.py             # Logger helper with documented methods
├── output/
│   ├── jobs.json             # Parsed job listings (overwritten on each run)
│   ├── log.txt               # Log file (overwritten on each run)
│   └── screenshots/          # Screenshots captured during execution
├── requirements.txt          # Python dependencies
└── run.py                    # Main script to run
```

## Installation

1. Install Python dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

2. Install Playwright browsers:
   ```bash
   python3 -m playwright install chromium
   ```

## Usage

Run the script:
```bash
python3 run.py
```

The browser will open and:
1. Navigate to Indeed homepage
2. Enter search query and location
3. Submit the search
4. Display results

## Configuration

### Indeed Settings (`config/indeed_config.env`)

| Setting | Description | Default |
|---------|-------------|---------|
| `INDEED_BASE_URL` | Indeed website URL | `https://www.indeed.com` |
| `INDEED_SEARCH_QUERY` | Job search keywords | `python developer` |
| `INDEED_LOCATION` | Job location | `Remote` |

### Playwright Settings (`config/playwright_config.env`)

| Setting | Description | Default |
|---------|-------------|---------|
| `PLAYWRIGHT_HEADLESS` | Run browser invisibly | `false` |
| `PLAYWRIGHT_SLOW_MO` | Delay between actions (ms) | `1000` |
| `PLAYWRIGHT_SCREENSHOTS` | Capture screenshots | `true` |
| `PLAYWRIGHT_VIEWPORT_WIDTH` | Browser width | `1280` |
| `PLAYWRIGHT_VIEWPORT_HEIGHT` | Browser height | `800` |

### Page Selectors (`config/page_selectors.py`)

CSS selectors used to find elements on Indeed pages. Update these if Indeed changes their page structure.

| Selector | Description |
|----------|-------------|
| `SEARCH_INPUT` | Job search input field |
| `LOCATION_INPUT` | Location input field |
| `SEARCH_BUTTON` | Search submit button |
| `JOB_CARD` | Job listing container |
| `JOB_TITLE` | Job title element |
| `COMPANY_NAME` | Company name element |
| `COMPANY_LOCATION` | Job location element |
| `JOB_LINK` | Job URL anchor tag |
| `EMAIL_PATTERN` | Regex pattern to extract contact emails |

## Output

After each run:
- **Jobs** are saved to `output/jobs.json` (parsed job listings)
- **Screenshots** are saved to `output/screenshots/`
- **Logs** are saved to `output/log.txt`

All output files are overwritten on each run to show only the latest results.

### Jobs JSON Format

```json
{
  "search_query": "python developer",
  "search_location": "Remote",
  "scraped_at": "2025-11-29T17:30:00",
  "total_jobs": 15,
  "jobs": [
    {
      "job_title": "Senior Python Developer",
      "company": "Tech Company",
      "company_location": "Remote",
      "job_id": "abc123",
      "job_link": "https://www.indeed.com/viewjob?jk=abc123",
      "contact_email": "jobs@techcompany.com"
    }
  ]
}
```
