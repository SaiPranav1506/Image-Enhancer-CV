"""
Image Enhancement Module
Enhances images using sharpening convolution and histogram equalization
"""

import cv2
import numpy as np
import os
from PIL import Image
from PIL import ImageEnhance as PILEnhance


class QualityMetrics:
    """Quick quality calculation for enhancement feedback"""
    
    @staticmethod
    def calculate_sharpness(image):
        """Calculate sharpness using Laplacian variance"""
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(image, cv2.CV_64F)
        return np.var(laplacian)
    
    @staticmethod
    def calculate_contrast(image):
        """Calculate contrast using standard deviation"""
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return np.std(image)
    
    @staticmethod
    def calculate_improvement(original, enhanced):
        """Calculate percentage improvement"""
        orig_sharp = QualityMetrics.calculate_sharpness(original)
        enh_sharp = QualityMetrics.calculate_sharpness(enhanced)
        
        orig_contrast = QualityMetrics.calculate_contrast(original)
        enh_contrast = QualityMetrics.calculate_contrast(enhanced)
        
        sharp_improve = ((enh_sharp - orig_sharp) / (orig_sharp + 1e-10)) * 100
        contrast_improve = ((enh_contrast - orig_contrast) / (orig_contrast + 1e-10)) * 100
        
        overall = (sharp_improve + contrast_improve) / 2
        return max(0, overall)


class ImageEnhancer:
    """Enhancer for improving image quality through sharpening and contrast"""
    
    def __init__(self, output_dir='output'):
        """
        Initialize the image enhancer
        
        Args:
            output_dir (str): Directory to save enhanced images
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Sharpening kernel for 2D convolution
        self.sharpening_kernel = np.array([
            [-1, -1, -1],
            [-1,  9, -1],
            [-1, -1, -1]
        ])
    
    def apply_sharpening(self, image_path, kernel_strength=1.0):
        """
        Apply sharpening using 2D convolution
        
        Args:
            image_path (str): Path to the image
            kernel_strength (float): Strength of sharpening (1.0 = default)
            
        Returns:
            numpy.ndarray: Sharpened image
        """
        try:
            image = cv2.imread(image_path)
            
            if image is None:
                print(f"Error: Could not read image {image_path}")
                return None
            
            # Normalize kernel based on strength
            kernel = self.sharpening_kernel * kernel_strength / 9.0
            
            # Apply 2D convolution
            sharpened = cv2.filter2D(image, -1, kernel)
            
            return sharpened
            
        except Exception as e:
            print(f"Error applying sharpening: {e}")
            return None
    
    def apply_histogram_equalization(self, image_array):
        """
        Apply histogram equalization for contrast enhancement
        
        Args:
            image_array (numpy.ndarray): Input image array (BGR)
            
        Returns:
            numpy.ndarray: Enhanced image with improved contrast
        """
        try:
            # Convert BGR to HSV for better contrast enhancement
            hsv = cv2.cvtColor(image_array, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            
            # Apply histogram equalization to V (value) channel
            v_enhanced = cv2.equalizeHist(v)
            
            # Merge channels back
            enhanced_hsv = cv2.merge([h, s, v_enhanced])
            
            # Convert back to BGR
            enhanced_bgr = cv2.cvtColor(enhanced_hsv, cv2.COLOR_HSV2BGR)
            
            return enhanced_bgr
            
        except Exception as e:
            print(f"Error applying histogram equalization: {e}")
            return image_array
    
    def enhance_image(self, image_path, apply_sharpen=True, apply_histogram=True, 
                     kernel_strength=1.0, save=True):
        """
        Enhance image with both sharpening and histogram equalization
        
        Args:
            image_path (str): Path to the input image
            apply_sharpen (bool): Whether to apply sharpening
            apply_histogram (bool): Whether to apply histogram equalization
            kernel_strength (float): Strength of sharpening kernel
            save (bool): Whether to save the enhanced image
            
        Returns:
            dict: {
                'original': numpy array,
                'enhanced': numpy array,
                'output_path': str or None,
                'improvement_%': float
            }
        """
        try:
            # Read original image
            original = cv2.imread(image_path)
            
            if original is None:
                print(f"Error: Could not read image {image_path}")
                return {'original': None, 'enhanced': None, 'output_path': None, 'improvement_%': 0}
            
            enhanced = original.copy()
            
            # Apply sharpening
            if apply_sharpen:
                enhanced = self.apply_sharpening(image_path, kernel_strength)
                if enhanced is None:
                    enhanced = original.copy()
            
            # Apply histogram equalization
            if apply_histogram:
                enhanced = self.apply_histogram_equalization(enhanced)
            
            # Calculate improvement percentage
            improvement = QualityMetrics.calculate_improvement(original, enhanced)
            
            output_path = None
            
            # Save if requested
            if save:
                filename = os.path.basename(image_path)
                name, ext = os.path.splitext(filename)
                output_filename = f"{name}_enhanced{ext}"
                output_path = os.path.join(self.output_dir, output_filename)
                
                cv2.imwrite(output_path, enhanced)
                print(f"Enhanced image saved: {output_path}")
                print(f"Quality improvement: {improvement:.2f}%")
            
            return {
                'original': original,
                'enhanced': enhanced,
                'output_path': output_path,
                'improvement_%': improvement
            }
            
        except Exception as e:
            print(f"Error enhancing image: {e}")
            return {'original': None, 'enhanced': None, 'output_path': None, 'improvement_%': 0}
    
    def enhance_batch(self, image_paths, apply_sharpen=True, apply_histogram=True):
        """
        Enhance multiple images in batch
        
        Args:
            image_paths (list): List of image paths
            apply_sharpen (bool): Whether to apply sharpening
            apply_histogram (bool): Whether to apply histogram equalization
            
        Returns:
            list: List of results for each image
        """
        results = []
        
        print(f"Enhancing {len(image_paths)} images...")
        
        for idx, image_path in enumerate(image_paths, 1):
            if not os.path.exists(image_path):
                print(f"Skipping: {image_path} (file not found)")
                continue
            
            print(f"[{idx}/{len(image_paths)}] Processing: {os.path.basename(image_path)}")
            
            result = self.enhance_image(image_path, apply_sharpen, apply_histogram)
            results.append({
                'input_path': image_path,
                'output_path': result['output_path'],
                'success': result['enhanced'] is not None
            })
        
        return results
    
    def compare_enhancement(self, image_path, display=False):
        """
        Compare original and enhanced versions of an image
        
        Args:
            image_path (str): Path to the image
            display (bool): Whether to display the comparison
            
        Returns:
            dict: Comparison statistics
        """
        try:
            result = self.enhance_image(image_path, save=False)
            
            if result['enhanced'] is None:
                return None
            
            original = result['original']
            enhanced = result['enhanced']
            
            # Calculate statistics
            original_mean = np.mean(original)
            enhanced_mean = np.mean(enhanced)
            
            original_std = np.std(original)
            enhanced_std = np.std(enhanced)
            
            return {
                'input_path': image_path,
                'original_mean': original_mean,
                'enhanced_mean': enhanced_mean,
                'original_std': original_std,
                'enhanced_std': enhanced_std,
                'brightness_change': enhanced_mean - original_mean,
                'contrast_change': enhanced_std - original_std
            }
            
        except Exception as e:
            print(f"Error in comparison: {e}")
            return None
