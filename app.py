# app.py
import os
import traceback
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import logging
from dotenv import load_dotenv

from word_to_presentation import convert_word_to_pptx
from src.utils import setup_logging, clean_temp_files

# Load environment variables from .env
load_dotenv()

# Setup logging
logger = setup_logging()

# Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/word_files'
app.config['OUTPUT_FOLDER'] = 'outputs/presentations'
app.config['PREVIEW_FOLDER'] = 'outputs/previews'
app.config['ALLOWED_EXTENSIONS'] = {'docx'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key')

# Debug: check keys
print("OpenAI API Key:", os.getenv("OPENAI_API_KEY"))
print("Unsplash Access Key:", os.getenv("UNSPLASH_ACCESS_KEY"))

# Ensure folders exist
for folder in [
    app.config['UPLOAD_FOLDER'], 
    app.config['OUTPUT_FOLDER'], 
    app.config['PREVIEW_FOLDER'],
    'uploads/temp',
    'logs'
]:
    os.makedirs(folder, exist_ok=True)

# Helper to check allowed file type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Error handlers
@app.errorhandler(413)
@app.errorhandler(RequestEntityTooLarge)
def too_large(e):
    flash('File too large. Maximum size is 16MB.', 'error')
    return redirect(url_for('index'))

@app.errorhandler(Exception)
def handle_error(e):
    logger.error(f"Unhandled error: {str(e)}\n{traceback.format_exc()}")
    flash(f'An error occurred: {str(e)}', 'error')
    return redirect(url_for('index'))

# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    previews = []
    ppt_file = None

    if request.method == 'POST':
        # Clean temp files from previous runs
        clean_temp_files()
        
        if 'word_file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        file = request.files['word_file']
        
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        if not allowed_file(file.filename):
            flash('Only .docx files are allowed', 'error')
            return redirect(request.url)
        
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            logger.info(f"Processing file: {filename}")
            
            # Convert Word to PPTX
            output_filename = filename.rsplit('.', 1)[0] + '.pptx'
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            convert_word_to_pptx(filepath, output_path)
            
            ppt_file = output_filename
            
            # Optionally: generate previews if your PresentationBuilder has it
            previews = [ppt_file]  # simple preview placeholder
            
            flash('Presentation created successfully!', 'success')
            
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}\n{traceback.format_exc()}")
            flash(f'Error processing file: {str(e)}', 'error')
            return redirect(request.url)
    
    return render_template('index.html', previews=previews, ppt_file=ppt_file)

# Download route
@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if not os.path.exists(file_path):
            flash('File not found', 'error')
            return redirect(url_for('index'))
        
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}")
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('index'))

# Route to view previews
@app.route('/preview/<filename>')
def preview_file(filename):
    file_path = os.path.join(app.config['PREVIEW_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return "Preview not found", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
