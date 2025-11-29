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
│   └── playwright_config.env # Browser settings (headless, slow_mo, viewport size)
├── utils/
│   ├── __init__.py           # Exports Logger class
│   └── logger.py             # Logger helper with documented methods
├── output/
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

## Output

After each run:
- **Screenshots** are saved to `output/screenshots/`
- **Logs** are saved to `output/log.txt`

Both are overwritten on each run to show only the latest results.
