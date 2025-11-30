from flask import Blueprint, jsonify, request
import subprocess
import sys
import os
import json
from pathlib import Path

scraper_blueprint = Blueprint('scraper', __name__)

# Path to the scraper script
SCRAPER_DIR = Path(__file__).parent.parent / 'indeed-pwd'
SCRAPER_SCRIPT = SCRAPER_DIR / 'run.py'
JOBS_FILE = SCRAPER_DIR / 'output' / 'jobs.json'


@scraper_blueprint.route('/run', methods=['POST'])
def run_scraper():
    """
    Run the Indeed scraper with custom parameters.
    
    Request Body (JSON):
        - search_query (str, optional): Job search query (e.g., "python developer")
        - location (str, optional): Job location (e.g., "Remote", "New York")
        - headless (bool, optional): Run browser in headless mode (default: false)
    
    Example:
        POST /api/scraper/run
        {
            "search_query": "react developer",
            "location": "Remote",
            "headless": true
        }
    """
    try:
        # Get parameters from request body
        data = request.get_json() or {}
        
        search_query = data.get('search_query', '')
        location = data.get('location', '')
        headless = data.get('headless', False)
        
        # Build command arguments
        cmd = [sys.executable, str(SCRAPER_SCRIPT)]
        
        if search_query:
            cmd.extend(['--search', search_query])
        
        if location:
            cmd.extend(['--location', location])
        
        if headless:
            cmd.append('--headless')
        
        # Run the scraper as a subprocess
        result = subprocess.run(
            cmd,
            cwd=str(SCRAPER_DIR),
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        # Check if jobs.json was created/updated
        if JOBS_FILE.exists():
            with open(JOBS_FILE, 'r') as f:
                jobs_data = json.load(f)
            
            return jsonify({
                'success': True,
                'message': 'Scraper completed successfully',
                'total_jobs': jobs_data.get('total_jobs', 0),
                'search_query': jobs_data.get('search_query'),
                'search_location': jobs_data.get('search_location'),
                'scraped_at': jobs_data.get('scraped_at'),
                'output': result.stdout[-1000:] if result.stdout else ''  # Last 1000 chars
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Scraper completed but no jobs file found',
                'stdout': result.stdout,
                'stderr': result.stderr
            }), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'error': 'Scraper timed out after 5 minutes'
        }), 504
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@scraper_blueprint.route('/run-async', methods=['POST'])
def run_scraper_async():
    """
    Start the Indeed scraper asynchronously (non-blocking).
    Returns immediately and scraper runs in background.
    
    Request Body (JSON):
        - search_query (str, optional): Job search query
        - location (str, optional): Job location
        - headless (bool, optional): Run browser in headless mode (default: true for async)
    """
    try:
        data = request.get_json() or {}
        
        search_query = data.get('search_query', '')
        location = data.get('location', '')
        headless = data.get('headless', True)  # Default to headless for async
        
        # Build command arguments
        cmd = [sys.executable, str(SCRAPER_SCRIPT)]
        
        if search_query:
            cmd.extend(['--search', search_query])
        
        if location:
            cmd.extend(['--location', location])
        
        if headless:
            cmd.append('--headless')
        
        # Start scraper in background (non-blocking)
        subprocess.Popen(
            cmd,
            cwd=str(SCRAPER_DIR),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        return jsonify({
            'success': True,
            'message': 'Scraper started in background',
            'params': {
                'search_query': search_query or '(from config)',
                'location': location or '(from config)',
                'headless': headless
            }
        }), 202
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@scraper_blueprint.route('/status', methods=['GET'])
def get_scraper_status():
    """
    Get the status of the last scraper run.
    Returns info from the most recent jobs.json file.
    """
    try:
        progress_file = SCRAPER_DIR / 'output' / 'progress.json'
        
        status = {
            'jobs_file_exists': JOBS_FILE.exists(),
            'last_run': None,
            'total_jobs': 0,
            'search_query': None,
            'search_location': None
        }
        
        if JOBS_FILE.exists():
            with open(JOBS_FILE, 'r') as f:
                jobs_data = json.load(f)
            
            status.update({
                'last_run': jobs_data.get('scraped_at'),
                'total_jobs': jobs_data.get('total_jobs', 0),
                'search_query': jobs_data.get('search_query'),
                'search_location': jobs_data.get('search_location'),
                'details_extracted_at': jobs_data.get('details_extracted_at'),
                'emails_extracted_at': jobs_data.get('emails_extracted_at'),
                'c2c_jobs_found': jobs_data.get('c2c_jobs_found', 0),
                'emails_found': jobs_data.get('emails_found', 0)
            })
        
        # Check progress file for current state
        if progress_file.exists():
            with open(progress_file, 'r') as f:
                progress = json.load(f)
            status['progress'] = progress
        
        return jsonify(status), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500
