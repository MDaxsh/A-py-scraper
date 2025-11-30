# Indeed Job Scraper

A Playwright-based job scraper for Indeed with stealth mode to bypass bot detection. Extracts job listings, company details, and contact emails.

## Features

- 🥷 **Stealth Mode** - Bypasses CAPTCHA and bot detection using `playwright-stealth`
- 📋 **Job Parsing** - Extracts job title, company, location, salary, C2C availability
- 📧 **Email Extraction** - Finds contact emails from job detail pages
- 🏢 **Company Details** - Extracts company description, link, phone number
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
├── scripts/
│   ├── __init__.py           # Exports extract functions
│   ├── extract_details.py    # Extracts company details, salary, C2C from job pages
│   └── extract_emails.py     # Extracts contact emails from job pages
├── models/
│   ├── __init__.py           # Exports TypedDict models
│   ├── job_model_v1.py       # TypedDict for JobModel and CompanyModel
│   └── job_results_v1.py     # TypedDict for JobResultsModel (output JSON)
├── utils/
│   ├── __init__.py           # Exports Logger class
│   └── logger.py             # Logger helper with documented methods
├── output/
│   ├── jobs.json             # Parsed job listings with all extracted data
│   └── log.txt               # Log file (overwritten on each run)
├── requirements.txt          # Python dependencies
├── run.py                    # Main script - runs full pipeline
└── README.md
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

### Full Pipeline
Run the main script to search Indeed and extract all data:
```bash
python3 run.py
```

This runs 3 steps sequentially:
1. **Search Indeed** - Search jobs and save basic listings
2. **Extract Details** - Visit each job page for company info, salary, C2C
3. **Extract Emails** - Find contact emails from job pages

### Individual Scripts
Run scripts separately if needed:
```bash
# Extract details only (requires jobs.json)
python3 scripts/extract_details.py

# Extract emails only (requires jobs.json)
python3 scripts/extract_emails.py
```

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

## Output

### Jobs JSON Format (`output/jobs.json`)

```json
{
  "search_query": "python developer",
  "search_location": "Remote",
  "scraped_at": "2025-11-29T17:30:00",
  "total_jobs": 15,
  "details_extracted_at": "2025-11-29T17:35:00",
  "emails_extracted_at": "2025-11-29T17:40:00",
  "emails_found": 3,
  "c2c_jobs_found": 2,
  "jobs": [
    {
      "job_title": "Senior Python Developer",
      "job_location": "Remote",
      "job_id": "abc123",
      "job_link": "https://www.indeed.com/viewjob?jk=abc123",
      "salary": "$120,000 - $150,000 a year",
      "allows_c2c": true,
      "company": {
        "name": "Tech Company",
        "description": "We are a leading technology company...",
        "company_link": "https://www.indeed.com/cmp/Tech-Company",
        "contact_email": "jobs@techcompany.com",
        "phone_number": "555-123-4567"
      }
    }
  ]
}
```

### TypedDict Models

Use the models for type hints in your code:
```python
from models import JobModel, CompanyModel, JobResultsModel
```
