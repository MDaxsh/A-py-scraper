from flask import Blueprint, jsonify, request
import json
import os

jobs_blueprint = Blueprint('jobs', __name__)

# Path to the jobs.json file
JOBS_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'indeed-pwd', 'output', 'jobs.json')


def load_jobs_data():
    """Load jobs data from jobs.json file"""
    try:
        with open(JOBS_FILE_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


@jobs_blueprint.route('/', methods=['GET'])
def get_all_jobs():
    """Get all job listings with metadata"""
    data = load_jobs_data()
    if data is None:
        return jsonify({'error': 'Jobs data not found or invalid'}), 404
    return jsonify(data), 200


@jobs_blueprint.route('/list', methods=['GET'])
def get_jobs_list():
    """Get only the jobs array with optional pagination"""
    data = load_jobs_data()
    if data is None:
        return jsonify({'error': 'Jobs data not found or invalid'}), 404
    
    jobs = data.get('jobs', [])
    
    # Optional pagination
    page = request.args.get('page', type=int)
    per_page = request.args.get('per_page', type=int, default=10)
    
    if page is not None:
        start = (page - 1) * per_page
        end = start + per_page
        paginated_jobs = jobs[start:end]
        return jsonify({
            'jobs': paginated_jobs,
            'total': len(jobs),
            'page': page,
            'per_page': per_page,
            'total_pages': (len(jobs) + per_page - 1) // per_page
        }), 200
    
    return jsonify({'jobs': jobs, 'total': len(jobs)}), 200


@jobs_blueprint.route('/c2c', methods=['GET'])
def get_c2c_jobs():
    """Get only jobs that allow C2C (Corp-to-Corp)"""
    data = load_jobs_data()
    if data is None:
        return jsonify({'error': 'Jobs data not found or invalid'}), 404
    
    jobs = data.get('jobs', [])
    c2c_jobs = [job for job in jobs if job.get('allows_c2c', False)]
    
    return jsonify({
        'jobs': c2c_jobs,
        'total': len(c2c_jobs),
        'c2c_jobs_found': data.get('c2c_jobs_found', len(c2c_jobs))
    }), 200


@jobs_blueprint.route('/search', methods=['GET'])
def search_jobs():
    """
    Search jobs by title and company name with filters.
    
    Query Parameters:
        - q (str, optional): Search query for job title or company name
        - c2c (bool, optional): Filter by C2C allowed (true/false)
        - has_email (bool, optional): Filter by email present (true/false)
    
    Example: /api/jobs/search?q=python&c2c=true&has_email=true
    """
    data = load_jobs_data()
    if data is None:
        return jsonify({'error': 'Jobs data not found or invalid'}), 404
    
    # Get query parameters
    query = request.args.get('q', '').lower()
    c2c_filter = request.args.get('c2c', '').lower()
    has_email_filter = request.args.get('has_email', '').lower()
    
    jobs = data.get('jobs', [])
    filtered_jobs = []
    
    for job in jobs:
        # Search by title and company name (if query provided)
        if query:
            title = job.get('job_title', '').lower()
            company_name = job.get('company', {}).get('name', '').lower()
            if query not in title and query not in company_name:
                continue
        
        # Filter by C2C
        if c2c_filter:
            allows_c2c = job.get('allows_c2c', False)
            if c2c_filter == 'true' and not allows_c2c:
                continue
            if c2c_filter == 'false' and allows_c2c:
                continue
        
        # Filter by email present
        if has_email_filter:
            contact_email = job.get('company', {}).get('contact_email', '')
            has_email = bool(contact_email and contact_email.strip())
            if has_email_filter == 'true' and not has_email:
                continue
            if has_email_filter == 'false' and has_email:
                continue
        
        filtered_jobs.append(job)
    
    return jsonify({
        'jobs': filtered_jobs,
        'total': len(filtered_jobs),
        'filters': {
            'query': query or None,
            'c2c': c2c_filter or None,
            'has_email': has_email_filter or None
        }
    }), 200


@jobs_blueprint.route('/stats', methods=['GET'])
def get_jobs_stats():
    """Get statistics about the scraped jobs"""
    data = load_jobs_data()
    if data is None:
        return jsonify({'error': 'Jobs data not found or invalid'}), 404
    
    jobs = data.get('jobs', [])
    
    # Count jobs with salary info
    jobs_with_salary = len([job for job in jobs if job.get('salary')])
    
    # Count unique companies
    unique_companies = len(set(job.get('company', {}).get('name', '') for job in jobs))
    
    return jsonify({
        'search_query': data.get('search_query'),
        'search_location': data.get('search_location'),
        'scraped_at': data.get('scraped_at'),
        'total_jobs': data.get('total_jobs'),
        'c2c_jobs_found': data.get('c2c_jobs_found'),
        'emails_found': data.get('emails_found'),
        'jobs_with_salary': jobs_with_salary,
        'unique_companies': unique_companies,
        'details_extracted_at': data.get('details_extracted_at'),
        'emails_extracted_at': data.get('emails_extracted_at')
    }), 200
