"""
Image Quality Metrics Module
Measures enhancement quality and provides percentage improvement
"""

import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim, peak_signal_noise_ratio as psnr


class QualityMetrics:
    """Calculate various image quality metrics for enhancement evaluation"""
    
    def __init__(self):
        """Initialize quality metrics calculator"""
        pass
    
    def calculate_sharpness(self, image):
        """
        Calculate image sharpness using Laplacian variance
        Higher value = sharper image
        
        Args:
            image: Image array (BGR or grayscale)
            
        Returns:
            float: Sharpness score
        """
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        laplacian = cv2.Laplacian(image, cv2.CV_64F)
        sharpness = np.var(laplacian)
        
        return sharpness
    
    def calculate_contrast(self, image):
        """
        Calculate contrast using standard deviation
        Higher value = more contrast
        
        Args:
            image: Image array
            
        Returns:
            float: Contrast score
        """
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        contrast = np.std(image)
        return contrast
    
    def calculate_brightness(self, image):
        """
        Calculate average brightness
        
        Args:
            image: Image array
            
        Returns:
            float: Average brightness (0-255)
        """
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        brightness = np.mean(image)
        return brightness
    
    def calculate_entropy(self, image):
        """
        Calculate image entropy (information content)
        Higher value = more information/detail
        
        Args:
            image: Image array
            
        Returns:
            float: Entropy score
        """
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Calculate histogram
        hist, _ = np.histogram(image, bins=256, range=(0, 256))
        hist = hist / hist.sum()  # Normalize
        
        # Calculate entropy
        entropy = -np.sum(hist * np.log2(hist + 1e-10))
        return entropy
    
    def calculate_edge_density(self, image):
        """
        Calculate edge density using Canny edge detection
        Higher value = more edges/details
        
        Args:
            image: Image array
            
        Returns:
            float: Edge density percentage (0-100)
        """
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        edges = cv2.Canny(image, 100, 200)
        edge_density = (np.sum(edges > 0) / edges.size) * 100
        
        return edge_density
    
    def calculate_blur_degree(self, image):
        """
        Calculate blur degree using Laplacian variance
        Lower value = more blurry
        
        Args:
            image: Image array
            
        Returns:
            float: Blur score (inverse of sharpness)
        """
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        laplacian = cv2.Laplacian(image, cv2.CV_64F)
        blur_score = np.var(laplacian)
        
        return blur_score
    
    def compare_images(self, original, enhanced):
        """
        Compare original and enhanced images
        
        Args:
            original: Original image array
            enhanced: Enhanced image array
            
        Returns:
            dict: Comparison metrics and percentage improvements
        """
        if len(original.shape) == 3:
            orig_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
            enh_gray = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
        else:
            orig_gray = original
            enh_gray = enhanced
        
        # Calculate metrics
        orig_sharpness = self.calculate_sharpness(original)
        enh_sharpness = self.calculate_sharpness(enhanced)
        
        orig_contrast = self.calculate_contrast(original)
        enh_contrast = self.calculate_contrast(enhanced)
        
        orig_brightness = self.calculate_brightness(original)
        enh_brightness = self.calculate_brightness(enhanced)
        
        orig_entropy = self.calculate_entropy(original)
        enh_entropy = self.calculate_entropy(enhanced)
        
        orig_edges = self.calculate_edge_density(original)
        enh_edges = self.calculate_edge_density(enhanced)
        
        # Calculate percentage improvements
        sharpness_improvement = ((enh_sharpness - orig_sharpness) / (orig_sharpness + 1e-10)) * 100
        contrast_improvement = ((enh_contrast - orig_contrast) / (orig_contrast + 1e-10)) * 100
        brightness_change = enh_brightness - orig_brightness
        entropy_improvement = ((enh_entropy - orig_entropy) / (orig_entropy + 1e-10)) * 100
        edge_improvement = ((enh_edges - orig_edges) / (orig_edges + 1e-10)) * 100
        
        return {
            'original': {
                'sharpness': round(orig_sharpness, 2),
                'contrast': round(orig_contrast, 2),
                'brightness': round(orig_brightness, 2),
                'entropy': round(orig_entropy, 2),
                'edge_density': round(orig_edges, 2)
            },
            'enhanced': {
                'sharpness': round(enh_sharpness, 2),
                'contrast': round(enh_contrast, 2),
                'brightness': round(enh_brightness, 2),
                'entropy': round(enh_entropy, 2),
                'edge_density': round(enh_edges, 2)
            },
            'improvements': {
                'sharpness_improvement_%': round(max(0, sharpness_improvement), 2),
                'contrast_improvement_%': round(max(0, contrast_improvement), 2),
                'brightness_change': round(brightness_change, 2),
                'entropy_improvement_%': round(max(0, entropy_improvement), 2),
                'edge_improvement_%': round(max(0, edge_improvement), 2)
            },
            'overall_improvement_%': round(
                (sharpness_improvement + contrast_improvement + entropy_improvement) / 3, 2
            )
        }
    
    def generate_report(self, original_path, enhanced_path):
        """
        Generate comprehensive quality report
        
        Args:
            original_path: Path to original image
            enhanced_path: Path to enhanced image
            
        Returns:
            dict: Complete quality report
        """
        original = cv2.imread(original_path)
        enhanced = cv2.imread(enhanced_path)
        
        if original is None or enhanced is None:
            return {'error': 'Could not load images'}
        
        comparison = self.compare_images(original, enhanced)
        
        report = {
            'files': {
                'original': original_path,
                'enhanced': enhanced_path
            },
            **comparison
        }
        
        return report
    
    def print_report(self, report):
        """
        Print formatted quality report
        
        Args:
            report: Quality report dictionary
        """
        print("\n" + "="*70)
        print("📊 IMAGE ENHANCEMENT QUALITY REPORT")
        print("="*70)
        
        if 'error' in report:
            print(f"Error: {report['error']}")
            return
        
        print("\n📁 Files:")
        print(f"  Original: {report['files']['original']}")
        print(f"  Enhanced: {report['files']['enhanced']}")
        
        print("\n🔍 Original Image Metrics:")
        for metric, value in report['original'].items():
            print(f"  {metric:.<30} {value}")
        
        print("\n✨ Enhanced Image Metrics:")
        for metric, value in report['enhanced'].items():
            print(f"  {metric:.<30} {value}")
        
        print("\n📈 Improvements:")
        for metric, value in report['improvements'].items():
            if '%' in metric:
                print(f"  {metric:.<30} {value:>6}%")
            else:
                print(f"  {metric:.<30} {value:>6}")
        
        print("\n🎯 Overall Improvement: {:<6}%".format(
            report['overall_improvement_%']))
        
        print("="*70 + "\n")
    
    def get_quality_score(self, image, max_score=100):
        """
        Calculate single quality score for an image (0-100)
        
        Args:
            image: Image array
            max_score: Maximum possible score
            
        Returns:
            float: Quality score (0-100)
        """
        sharpness = self.calculate_sharpness(image)
        contrast = self.calculate_contrast(image)
        entropy = self.calculate_entropy(image)
        
        # Normalize and combine metrics
        sharpness_norm = min(sharpness / 500, 1.0) * 100
        contrast_norm = min(contrast / 64, 1.0) * 100
        entropy_norm = min(entropy / 8, 1.0) * 100
        
        quality_score = (sharpness_norm + contrast_norm + entropy_norm) / 3
        
        return min(quality_score, max_score)
