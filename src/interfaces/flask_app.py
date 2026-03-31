"""
Flask API for Image Enhancement
RESTful API for image processing and enhancement operations
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import cv2
import numpy as np
import os
import sys
from io import BytesIO
from PIL import Image
import json

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from modules.web_scraper import WebScraper
from modules.blur_detector import BlurDetector
from modules.image_enhancer import ImageEnhancer


# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize modules
web_scraper = WebScraper(output_dir='temp_images')
blur_detector = BlurDetector(threshold=100)
image_enhancer = ImageEnhancer(output_dir='output')

# Ensure directories exist
os.makedirs('temp_images', exist_ok=True)
os.makedirs('output', exist_ok=True)


# ==================== Routes ====================

@app.route('/', methods=['GET'])
def home():
    """Health check and API documentation"""
    return jsonify({
        'status': 'running',
        'app': 'Image Enhancement API',
        'version': '1.0.0',
        'endpoints': {
            'scraper': {
                'POST /api/scrape': 'Scrape images from URL',
                'POST /api/scrape-multiple': 'Scrape from multiple URLs'
            },
            'detector': {
                'POST /api/detect-blur': 'Detect blur in single image',
                'POST /api/detect-blur-batch': 'Batch blur detection'
            },
            'enhancer': {
                'POST /api/enhance': 'Enhance single image',
                'POST /api/enhance-batch': 'Batch image enhancement',
                'POST /api/compare': 'Compare original and enhanced'
            }
        }
    }), 200


# ==================== Web Scraper Endpoints ====================

@app.route('/api/scrape', methods=['POST'])
def scrape_images():
    """Scrape images from a URL"""
    try:
        data = request.get_json()
        url = data.get('url')
        limit = data.get('limit', 10)
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        images = web_scraper.scrape_images(url, limit)
        
        return jsonify({
            'status': 'success',
            'downloaded': len(images),
            'images': images
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/scrape-multiple', methods=['POST'])
def scrape_multiple():
    """Scrape images from multiple URLs"""
    try:
        data = request.get_json()
        urls = data.get('urls', [])
        images_per_url = data.get('images_per_url', 5)
        
        if not urls:
            return jsonify({'error': 'URLs list is required'}), 400
        
        images = web_scraper.scrape_multiple_urls(urls, images_per_url)
        
        return jsonify({
            'status': 'success',
            'total_downloaded': len(images),
            'images': images
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== Blur Detection Endpoints ====================

@app.route('/api/detect-blur', methods=['POST'])
def detect_blur():
    """Detect blur in uploaded image"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Image file is required'}), 400
        
        file = request.files['file']
        threshold = request.form.get('threshold', 100, type=float)
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save temporary file
        temp_path = os.path.join('temp_images', file.filename)
        file.save(temp_path)
        
        # Detect blur
        detector = BlurDetector(threshold=threshold)
        result = detector.is_blur(temp_path)
        
        return jsonify({
            'status': 'success',
            'image': file.filename,
            'variance': float(result['variance']) if result['variance'] else None,
            'is_blurry': result['is_blur'],
            'threshold': result['threshold']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/detect-blur-batch', methods=['POST'])
def detect_blur_batch():
    """Batch blur detection"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'Image files are required'}), 400
        
        files = request.files.getlist('files')
        threshold = request.form.get('threshold', 100, type=float)
        
        image_paths = []
        for file in files:
            if file.filename != '':
                temp_path = os.path.join('temp_images', file.filename)
                file.save(temp_path)
                image_paths.append(temp_path)
        
        # Batch detection
        detector = BlurDetector(threshold=threshold)
        results = detector.detect_blur_batch(image_paths)
        
        return jsonify({
            'status': 'success',
            'summary': {
                'total': results['total'],
                'blurry': results['blurry_count'],
                'clear': results['clear_count']
            },
            'blurry_images': [{'path': b['path'], 'variance': float(b['variance'])} 
                             for b in results['blurry']],
            'clear_images': [{'path': c['path'], 'variance': float(c['variance'])} 
                            for c in results['clear']]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== Image Enhancement Endpoints ====================

@app.route('/api/enhance', methods=['POST'])
def enhance_image():
    """Enhance single image"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Image file is required'}), 400
        
        file = request.files['file']
        apply_sharpen = request.form.get('sharpen', 'true').lower() == 'true'
        apply_histogram = request.form.get('histogram', 'true').lower() == 'true'
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save temporary file
        temp_path = os.path.join('temp_images', file.filename)
        file.save(temp_path)
        
        # Enhance
        result = image_enhancer.enhance_image(temp_path, apply_sharpen, apply_histogram)
        
        return jsonify({
            'status': 'success',
            'image': file.filename,
            'output_path': result['output_path'],
            'sharpen_applied': apply_sharpen,
            'histogram_applied': apply_histogram
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/enhance-batch', methods=['POST'])
def enhance_batch():
    """Batch image enhancement"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'Image files are required'}), 400
        
        files = request.files.getlist('files')
        apply_sharpen = request.form.get('sharpen', 'true').lower() == 'true'
        apply_histogram = request.form.get('histogram', 'true').lower() == 'true'
        
        image_paths = []
        for file in files:
            if file.filename != '':
                temp_path = os.path.join('temp_images', file.filename)
                file.save(temp_path)
                image_paths.append(temp_path)
        
        # Batch enhance
        results = image_enhancer.enhance_batch(image_paths, apply_sharpen, apply_histogram)
        
        return jsonify({
            'status': 'success',
            'total_processed': len(results),
            'success_count': sum(1 for r in results if r['success']),
            'results': results
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/compare', methods=['POST'])
def compare_enhancement():
    """Compare original and enhanced image"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Image file is required'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save temporary file
        temp_path = os.path.join('temp_images', file.filename)
        file.save(temp_path)
        
        # Compare
        comparison = image_enhancer.compare_enhancement(temp_path)
        
        return jsonify({
            'status': 'success',
            'image': file.filename,
            'statistics': {
                'brightness_change': float(comparison['brightness_change']),
                'contrast_change': float(comparison['contrast_change']),
                'original_brightness': float(comparison['original_mean']),
                'enhanced_brightness': float(comparison['enhanced_mean'])
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== Configuration Endpoints ====================

@app.route('/api/settings/blur-threshold', methods=['GET', 'POST'])
def blur_threshold():
    """Get or set blur detection threshold"""
    if request.method == 'GET':
        return jsonify({
            'threshold': blur_detector.threshold
        }), 200
    
    else:  # POST
        try:
            data = request.get_json()
            new_threshold = data.get('threshold')
            
            if new_threshold is None:
                return jsonify({'error': 'Threshold value required'}), 400
            
            blur_detector.set_threshold(new_threshold)
            
            return jsonify({
                'status': 'success',
                'threshold': blur_detector.threshold
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500


# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


# ==================== Application Entry ====================

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
