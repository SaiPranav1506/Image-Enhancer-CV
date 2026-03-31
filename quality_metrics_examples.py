"""
Quality Metrics Example
Demonstrates how to measure image enhancement quality and improvement percentage
"""

import sys
import os
import cv2
import numpy as np

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from modules.image_enhancer import ImageEnhancer
from modules.quality_metrics import QualityMetrics


def example_basic_metrics():
    """Example 1: Basic quality metrics for an image"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Image Quality Metrics")
    print("="*70)
    
    metrics = QualityMetrics()
    
    # Create a sample image (or use existing)
    image_path = "data/sample.jpg"
    
    if os.path.exists(image_path):
        image = cv2.imread(image_path)
        
        print(f"\nAnalyzing: {image_path}")
        
        sharpness = metrics.calculate_sharpness(image)
        contrast = metrics.calculate_contrast(image)
        brightness = metrics.calculate_brightness(image)
        entropy = metrics.calculate_entropy(image)
        edge_density = metrics.calculate_edge_density(image)
        quality_score = metrics.get_quality_score(image)
        
        print(f"\n📊 Image Metrics:")
        print(f"  Sharpness........ {sharpness:.2f}")
        print(f"  Contrast........ {contrast:.2f}")
        print(f"  Brightness...... {brightness:.2f}")
        print(f"  Entropy......... {entropy:.2f}")
        print(f"  Edge Density.... {edge_density:.2f}%")
        print(f"  Quality Score... {quality_score:.2f}/100")
    else:
        print(f"⚠️  Sample image not found: {image_path}")
        print("   Create a sample image first")


def example_enhancement_comparison():
    """Example 2: Compare original vs enhanced"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Enhancement Quality Comparison")
    print("="*70)
    
    enhancer = ImageEnhancer()
    metrics = QualityMetrics()
    
    image_path = "data/blurry_sample.jpg"
    
    if os.path.exists(image_path):
        print(f"\nProcessing: {image_path}")
        
        # Enhance the image
        result = enhancer.enhance_image(image_path, apply_sharpen=True, 
                                       apply_histogram=True, save=False)
        
        if result['enhanced'] is not None:
            # Compare
            report = metrics.compare_images(result['original'], result['enhanced'])
            metrics.print_report(report)
            
            # Show specific improvements
            print("\n🎯 KEY IMPROVEMENTS:")
            improvements = report['improvements']
            print(f"  ✨ Sharpness improved by: {improvements['sharpness_improvement_%']}%")
            print(f"  📊 Contrast improved by: {improvements['contrast_improvement_%']}%")
            print(f"  💾 Detail added (entropy): {improvements['entropy_improvement_%']}%")
            print(f"  🔍 Edge detection: {improvements['edge_improvement_%']}%")
            print(f"\n  🎉 OVERALL IMPROVEMENT: {report['overall_improvement_%']}%")
        else:
            print("Enhancement failed")
    else:
        print(f"⚠️  Sample image not found: {image_path}")


def example_batch_quality_analysis():
    """Example 3: Analyze quality of multiple images"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Batch Quality Analysis")
    print("="*70)
    
    metrics = QualityMetrics()
    enhancer = ImageEnhancer()
    
    # Get all images from data directory
    data_dir = "data"
    if not os.path.exists(data_dir):
        print(f"⚠️  Directory not found: {data_dir}")
        return
    
    image_files = [f for f in os.listdir(data_dir) 
                   if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
    
    if not image_files:
        print(f"⚠️  No images found in {data_dir}")
        return
    
    print(f"\nAnalyzing {len(image_files)} images...")
    print("\n" + "-"*70)
    
    results = []
    for idx, filename in enumerate(image_files[:5], 1):  # First 5 images
        filepath = os.path.join(data_dir, filename)
        image = cv2.imread(filepath)
        
        if image is None:
            continue
        
        quality_score = metrics.get_quality_score(image)
        sharpness = metrics.calculate_sharpness(image)
        
        results.append({
            'filename': filename,
            'quality': quality_score,
            'sharpness': sharpness
        })
        
        print(f"{idx}. {filename}")
        print(f"   Quality Score: {quality_score:.2f}/100")
        print(f"   Sharpness: {sharpness:.2f}")
    
    print("\n" + "-"*70)
    if results:
        avg_quality = np.mean([r['quality'] for r in results])
        print(f"\n📊 Average Quality: {avg_quality:.2f}/100")


def example_enhancement_percentage():
    """Example 4: Show enhancement percentage improvement"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Enhancement Percentage Improvement")
    print("="*70 + "\n")
    
    enhancer = ImageEnhancer()
    metrics = QualityMetrics()
    
    # Create sample blurry image for demo
    print("Creating sample blurry image for demonstration...")
    
    # Generate a simple test image
    sample_image = np.random.randint(0, 256, (300, 300, 3), dtype=np.uint8)
    sample_path = "sample_blur_demo.jpg"
    cv2.imwrite(sample_path, sample_image)
    
    try:
        # Enhance it
        print("Enhancing image...")
        result = enhancer.enhance_image(sample_path, apply_sharpen=True, 
                                       apply_histogram=True, save=False)
        
        if result['enhanced'] is not None:
            # Get quality scores
            original_score = metrics.get_quality_score(result['original'])
            enhanced_score = metrics.get_quality_score(result['enhanced'])
            
            # Calculate percentage improvement
            improvement = ((enhanced_score - original_score) / original_score) * 100
            
            print("\n📈 ENHANCEMENT RESULTS:")
            print(f"  Original Quality Score: {original_score:.2f}/100")
            print(f"  Enhanced Quality Score: {enhanced_score:.2f}/100")
            print(f"  Improvement: {improvement:.2f}%")
            
            # Detailed metrics
            report = metrics.compare_images(result['original'], result['enhanced'])
            
            print("\n  Detailed Improvements:")
            print(f"    • Sharpness: ↑ {report['improvements']['sharpness_improvement_%']:.2f}%")
            print(f"    • Contrast: ↑ {report['improvements']['contrast_improvement_%']:.2f}%")
            print(f"    • Detail (Entropy): ↑ {report['improvements']['entropy_improvement_%']:.2f}%")
            print(f"    • Edges: ↑ {report['improvements']['edge_improvement_%']:.2f}%")
            
            # Visual representation
            print("\n  Quality Improvement:")
            bar_length = 40
            filled = int(bar_length * min(improvement, 100) / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"    [{bar}] {improvement:.1f}%")
        
    finally:
        # Cleanup
        if os.path.exists(sample_path):
            os.remove(sample_path)


def example_custom_kernel_comparison():
    """Example 5: Compare different sharpening strengths"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Compare Different Enhancement Strengths")
    print("="*70)
    
    metrics = QualityMetrics()
    
    image_path = "data/sample.jpg"
    
    if os.path.exists(image_path):
        original = cv2.imread(image_path)
        
        print(f"\nTesting different sharpening kernels on: {image_path}")
        
        original_score = metrics.get_quality_score(original)
        print(f"\nOriginal Quality Score: {original_score:.2f}/100")
        
        # Test different kernel strengths
        kernel_strengths = [0.5, 1.0, 1.5, 2.0]
        
        print("\nKernel Strength Comparison:")
        print("-" * 70)
        
        for strength in kernel_strengths:
            sharpening_kernel = np.array([
                [-1, -1, -1],
                [-1, 9, -1],
                [-1, -1, -1]
            ]) * strength / 9.0
            
            enhanced = cv2.filter2D(original, -1, sharpening_kernel)
            enhanced_score = metrics.get_quality_score(enhanced)
            improvement = ((enhanced_score - original_score) / original_score) * 100
            
            print(f"Strength {strength:>3}: Quality {enhanced_score:>6.2f}/100 "
                  f"(+{improvement:>6.2f}%)")
    else:
        print(f"⚠️  Image not found: {image_path}")


def example_real_world_scenario():
    """Example 6: Real-world enhancement workflow"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Real-World Enhancement Workflow")
    print("="*70)
    
    print("""
    Workflow Scenario:
    1. User uploads blurry image from phone
    2. System detects blur
    3. System enhances image
    4. System measures quality improvement
    5. User sees percentage improvement
    
    Let's simulate this:
    """)
    
    enhancer = ImageEnhancer()
    metrics = QualityMetrics()
    
    # Simulate workflow
    steps = [
        ("📤", "Image uploaded"),
        ("🔍", "Analyzing image..."),
        ("⚙️", "Running enhancement algorithms..."),
        ("📊", "Calculating quality metrics..."),
    ]
    
    for emoji, step in steps:
        print(f"{emoji} {step}")
    
    print(f"\n✅ Enhancement Complete!\n")
    
    print("Results Summary:")
    print("─" * 70)
    print("Original Quality:   52.34/100 ████░░░░░░░░░░░░░░░░░░░░░░░")
    print("Enhanced Quality:   78.21/100 ██████████████████░░░░░░░░░░")
    print("Improvement:        +48.68%   🎉")
    print("─" * 70)
    
    print("\nKey Metrics:")
    print("  🔫 Sharpness:      +67.32%")
    print("  📊 Contrast:       +43.15%")
    print("  💾 Detail:         +35.89%")
    print("  🔍 Edges:          +52.41%")
    
    print("\n✨ Your image is ready to use!")


# ==================== Main ====================

def main():
    """Run quality metrics examples"""
    
    print("\n" + "█"*70)
    print("IMAGE ENHANCEMENT - QUALITY METRICS EXAMPLES")
    print("█"*70)
    
    examples = [
        ("1", "Basic Quality Metrics", example_basic_metrics),
        ("2", "Enhancement Comparison", example_enhancement_comparison),
        ("3", "Batch Quality Analysis", example_batch_quality_analysis),
        ("4", "Enhancement Percentage", example_enhancement_percentage),
        ("5", "Kernel Comparison", example_custom_kernel_comparison),
        ("6", "Real-World Workflow", example_real_world_scenario),
    ]
    
    print("\nAvailable Examples:")
    for num, title, _ in examples:
        print(f"  {num}. {title}")
    print(f"  0. Run all examples")
    print(f"  q. Quit")
    
    choice = input("\nSelect example (0-6, q to quit): ").strip().lower()
    
    if choice == '0':
        for num, title, func in examples:
            try:
                func()
                input("\nPress Enter to continue...")
            except Exception as e:
                print(f"Error in example: {e}")
    
    elif choice == 'q':
        print("Goodbye!")
        return
    
    else:
        for num, title, func in examples:
            if choice == num:
                try:
                    func()
                except Exception as e:
                    print(f"Error running example: {e}")
                break
        else:
            print("Invalid selection")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
