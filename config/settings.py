# config/settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    # Flask Settings
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # File Upload Settings
    UPLOAD_FOLDER = BASE_DIR / 'uploads' / 'word_files'
    OUTPUT_FOLDER = BASE_DIR / 'outputs' / 'presentations'
    PREVIEW_FOLDER = BASE_DIR / 'outputs' / 'previews'
    TEMP_FOLDER = BASE_DIR / 'uploads' / 'temp'
    
    # Allowed Extensions
    ALLOWED_EXTENSIONS = {'docx'}
    
    # API Settings
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')
    OPENAI_MAX_TOKENS = int(os.environ.get('OPENAI_MAX_TOKENS', 150))
    OPENAI_TEMPERATURE = float(os.environ.get('OPENAI_TEMPERATURE', 0.5))
    
    # Image Settings
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600
    PREVIEW_WIDTH = 320
    PREVIEW_HEIGHT = 180
    
    # Presentation Settings
    DEFAULT_TEMPLATE = BASE_DIR / 'assets' / 'templates' / 'professional.pptx'
    DEFAULT_THEME = 'professional'
    
    @classmethod
    def init_app(cls, app):
        """Initialize app with config"""
        for key, value in cls.__dict__.items():
            if not key.startswith('_') and not callable(value):
                app.config[key] = value
        
        # Create necessary directories
        for folder in [cls.UPLOAD_FOLDER, cls.OUTPUT_FOLDER, 
                      cls.PREVIEW_FOLDER, cls.TEMP_FOLDER]:
            folder.mkdir(parents=True, exist_ok=True)