#This is blur detection file
"""
Blur Detection Module
Detects blurry images using Laplacian Variance method
"""

import cv2
import numpy as np
import os


class BlurDetector:
    """Detector for blurry images using Laplacian Variance"""
    
    def __init__(self, threshold=100):
        """
        Initialize the blur detector
        
        Args:
            threshold (float): Laplacian variance threshold for blur detection
                              Values below threshold are considered blurry
        """
        self.threshold = threshold
    
    def calculate_laplacian_variance(self, image_path):
        """
        Calculate Laplacian variance of an image
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            tuple: (laplacian_variance, image_array) or None if error
        """
        try:
            # Read image in grayscale
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            
            if image is None:
                print(f"Error: Could not read image {image_path}")
                return None
            
            # Calculate Laplacian
            laplacian = cv2.Laplacian(image, cv2.CV_64F)
            
            # Calculate variance
            variance = np.var(laplacian)
            
            return variance, image
            
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return None
    
    def is_blur(self, image_path):
        """
        Check if an image is blurry
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            dict: {
                'is_blur': bool,
                'variance': float,
                'threshold': float,
                'image_path': str
            }
        """
        result = self.calculate_laplacian_variance(image_path)
        
        if result is None:
            return {
                'is_blur': None,
                'variance': None,
                'threshold': self.threshold,
                'image_path': image_path
            }
        
        variance, _ = result
        is_blurry = variance < self.threshold
        
        return {
            'is_blur': is_blurry,
            'variance': variance,
            'threshold': self.threshold,
            'image_path': image_path
        }
    
    def detect_blur_batch(self, image_paths):
        """
        Detect blurry images in a batch
        
        Args:
            image_paths (list): List of image file paths
            
        Returns:
            dict: Categorized results with 'blurry' and 'clear' lists
        """
        blurry_images = []
        clear_images = []
        
        print(f"Processing {len(image_paths)} images...")
        
        for image_path in image_paths:
            if not os.path.exists(image_path):
                print(f"Skipping: {image_path} (file not found)")
                continue
            
            result = self.is_blur(image_path)
            
            if result['is_blur'] is None:
                continue
            
            variance = result['variance']
            print(f"{os.path.basename(image_path)}: Variance={variance:.2f}, "
                  f"Status={'BLURRY' if result['is_blur'] else 'CLEAR'}")
            
            if result['is_blur']:
                blurry_images.append({
                    'path': image_path,
                    'variance': variance
                })
            else:
                clear_images.append({
                    'path': image_path,
                    'variance': variance
                })
        
        summary = {
            'total': len(image_paths),
            'blurry_count': len(blurry_images),
            'clear_count': len(clear_images),
            'blurry': blurry_images,
            'clear': clear_images
        }
        
        print(f"\nSummary: {len(blurry_images)} blurry, {len(clear_images)} clear")
        
        return summary
    
    def set_threshold(self, new_threshold):
        """
        Update the blur detection threshold
        
        Args:
            new_threshold (float): New threshold value
        """
        self.threshold = new_threshold
        print(f"Threshold updated to: {new_threshold}")
