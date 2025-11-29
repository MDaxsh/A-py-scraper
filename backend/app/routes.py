from flask import Blueprint, jsonify
import os
import psycopg2
from psycopg2.extras import RealDictCursor

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Backend is running'}), 200

@api_blueprint.route('/info', methods=['GET'])
def info():
    """API info endpoint"""
    return jsonify({
        'name': 'Python API',
        'version': '1.0.0',
        'description': 'Python Flask API Backend'
    }), 200


@api_blueprint.route('/app-info', methods=['GET'])
def app_info():
    """Return application metadata from the database's app_info table"""
    # Read database URL from environment (created by docker-compose)
    db_url = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@py-scraper-db:5432/myapp')
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT id, name, version, status, created_at, updated_at FROM app_info LIMIT 1')
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return jsonify(row), 200
        else:
            return jsonify({'message': 'no app_info found'}), 404
    except Exception as e:
        return jsonify({'error': 'db_error', 'details': str(e)}), 500
