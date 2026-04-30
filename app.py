import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from assistant import ResumeAssistant

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())
    print(f"DEBUG: Receiving {request.method} request to {request.path}")

# Setup directories
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize Assistant
assistant = ResumeAssistant()

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    result = assistant.analyze_resume(file_path)
    if not result:
        return jsonify({"error": "Analysis failed"}), 500
        
    return jsonify(result)

@app.route('/api/match', methods=['POST'])
def match():
    data = request.json
    job_desc = data.get('job_description')
    if not job_desc:
        return jsonify({"error": "No job description provided"}), 400
        
    result = assistant.match_job(job_desc)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
