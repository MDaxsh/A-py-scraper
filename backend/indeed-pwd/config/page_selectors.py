"""
============================================================
PAGE SELECTORS
============================================================
This file contains all CSS selectors used to find elements
on the Indeed website. Update these if Indeed changes their
page structure.
============================================================
"""


class IndeedSelectors:
    """
    CSS selectors for Indeed website elements.
    Each selector may have multiple options separated by commas
    to handle different page layouts.
    """
    
    # ---------------------------------------------------------
    # HOMEPAGE SELECTORS
    # ---------------------------------------------------------
    
    # Search input field for job title/keywords
    SEARCH_INPUT = 'input[id="text-input-what"], input[name="q"]'
    
    # Location input field
    LOCATION_INPUT = 'input[id="text-input-where"], input[name="l"]'
    
    # Search submit button
    SEARCH_BUTTON = 'button[type="submit"]'
    
    # ---------------------------------------------------------
    # SEARCH RESULTS PAGE SELECTORS
    # ---------------------------------------------------------
    
    # Job card container (each job listing)
    JOB_CARD = 'div.job_seen_beacon, div[data-jk], li.css-5lfssm'
    
    # Job title within a card
    JOB_TITLE = 'h2.jobTitle span, a.jcs-JobTitle span, h2 a span'
    
    # Company name within a card
    COMPANY_NAME = 'span[data-testid="company-name"], span.companyName, span.company'
    
    # Company/job location within a card
    COMPANY_LOCATION = 'div[data-testid="text-location"], div.companyLocation, span.location'
    
    # Job link (anchor tag containing the job URL)
    JOB_LINK = 'h2.jobTitle a, a.jcs-JobTitle'
    
    # ---------------------------------------------------------
    # OPTIONAL SELECTORS (for future use)
    # ---------------------------------------------------------
    
    # Salary information
    SALARY = 'div.salary-snippet-container, span.salary-snippet, div.metadata.salary-snippet-container'
    
    # Job snippet/description preview
    JOB_SNIPPET = 'div.job-snippet, td.snip, ul li'
    
    # Posted date
    POSTED_DATE = 'span.date, span[data-testid="myJobsStateDate"]'
    
    # Pagination - next page button
    NEXT_PAGE = 'a[data-testid="pagination-page-next"], a[aria-label="Next Page"]'
    
    # Contact email (extracted from page text using regex pattern)
    # Note: Email is typically not in a specific element, so we search the entire card text
    EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
