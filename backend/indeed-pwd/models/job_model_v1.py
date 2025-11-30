"""
Job Model v1 - TypedDict definitions for individual job entries
===============================================================
Defines the structure for a single job listing extracted from Indeed.
All properties are optional (NotRequired) since not all fields may be available.
"""

from typing import TypedDict, NotRequired


class CompanyModel(TypedDict):
    """
    Company information extracted from job detail page.
    All fields are optional as they may not always be available.
    
    Attributes:
        name: Company name from job listing
        description: Company description (first 250 chars from detail page)
        company_link: Link to company's Indeed profile or website
        contact_email: Contact email if found on job page
        phone_number: Phone number if found on job page
    """
    name: NotRequired[str]
    description: NotRequired[str]
    company_link: NotRequired[str]
    contact_email: NotRequired[str]
    phone_number: NotRequired[str]


class JobModel(TypedDict):
    """
    Single job listing with all extracted information.
    All fields are optional as they may not always be available.
    
    Attributes:
        job_title: Title of the job position
        company: Nested company information object
        job_location: Location or work type (Remote, Hybrid, etc.)
        job_id: Indeed's unique job identifier
        job_link: Full URL to the job posting
        salary: Salary information if available
        allows_c2c: Whether the job allows Corp-to-Corp arrangements
    """
    job_title: NotRequired[str]
    company: NotRequired[CompanyModel]
    job_location: NotRequired[str]
    job_id: NotRequired[str]
    job_link: NotRequired[str]
    salary: NotRequired[str]
    allows_c2c: NotRequired[bool]
