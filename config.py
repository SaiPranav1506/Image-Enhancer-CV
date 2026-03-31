# Project Configuration
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Web Scraper Settings
SCRAPER_TIMEOUT = int(os.getenv('SCRAPER_TIMEOUT', 10))
SCRAPER_MAX_RETRIES = int(os.getenv('SCRAPER_MAX_RETRIES', 3))
SCRAPER_USER_AGENT = os.getenv('SCRAPER_USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

# Blur Detection Settings
BLUR_DETECTION_THRESHOLD = int(os.getenv('BLUR_DETECTION_THRESHOLD', 100))  # Laplacian variance threshold
MIN_BLUR_THRESHOLD = int(os.getenv('MIN_BLUR_THRESHOLD', 50))
MAX_BLUR_THRESHOLD = int(os.getenv('MAX_BLUR_THRESHOLD', 200))

# Image Enhancement Settings
ENHANCEMENT_OUTPUT_QUALITY = int(os.getenv('ENHANCEMENT_OUTPUT_QUALITY', 95))  # JPEG quality (1-100)
SHARPENING_KERNEL_STRENGTH = float(os.getenv('SHARPENING_KERNEL_STRENGTH', 1.0))

# Directory Settings
DATA_DIRECTORY = os.getenv('DATA_DIRECTORY', 'data')
TEMP_DIRECTORY = os.getenv('TEMP_DIRECTORY', 'temp_images')
OUTPUT_DIRECTORY = os.getenv('OUTPUT_DIRECTORY', 'output')

# Flask Settings
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 50 * 1024 * 1024))  # 50MB max file size

# Streamlit Settings
STREAMLIT_PORT = int(os.getenv('STREAMLIT_PORT', 8501))

# Deployment Settings
NGROK_AUTH_TOKEN = os.getenv('NGROK_AUTH_TOKEN', None)  # Set your ngrok auth token here
DEPLOYMENT_PORT = int(os.getenv('DEPLOYMENT_PORT', 5000))
DEPLOYMENT_MODE = os.getenv('DEPLOYMENT_MODE', 'development')

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'app.log')
