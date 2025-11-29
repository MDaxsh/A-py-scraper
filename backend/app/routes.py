from flask import Blueprint, jsonify

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
