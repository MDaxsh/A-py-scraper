"""
Job Results v1 - TypedDict definitions for the complete output JSON file
========================================================================
Defines the structure for the jobs.json output file containing all scraped results.
"""

from typing import TypedDict, List
from .job_model_v1 import JobModel


class JobResultsModel(TypedDict):
    """
    Complete structure of the jobs.json output file.
    
    Attributes:
        search_query: The job search term used (e.g., "python developer")
        search_location: The location filter used (e.g., "Remote")
        scraped_at: ISO timestamp when initial scraping was performed
        total_jobs: Total number of jobs found in search results
        emails_extracted_at: ISO timestamp when email extraction was completed
        emails_found: Count of jobs where contact emails were found
        details_extracted_at: ISO timestamp when detail extraction was completed
        c2c_jobs_found: Count of jobs that allow Corp-to-Corp arrangements
        jobs: List of all extracted job entries
    """
    search_query: str
    search_location: str
    scraped_at: str
    total_jobs: int
    emails_extracted_at: str
    emails_found: int
    details_extracted_at: str
    c2c_jobs_found: int
    jobs: List[JobModel]
