import os
from flask import Flask, request, send_from_directory

app = Flask(__name__)

# Configure user file cache
USER_CACHE_DIR = '/app/user_cache'
os.makedirs(USER_CACHE_DIR, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    # Generate a unique filename
    filename = os.secure_filename(file.filename)
    file_path = os.path.join(USER_CACHE_DIR, filename)
    file.save(file_path)
    
    return 'File uploaded successfully', 200

@app.route('/user_cache/<filename>')
def serve_file(filename):
    return send_from_directory(USER_CACHE_DIR, filename)