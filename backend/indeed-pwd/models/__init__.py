"""
Models Package - TypedDict definitions for Indeed scraper output
================================================================
"""

from .job_model_v1 import JobModel, CompanyModel
from .job_results_v1 import JobResultsModel

__all__ = ['JobModel', 'CompanyModel', 'JobResultsModel']
