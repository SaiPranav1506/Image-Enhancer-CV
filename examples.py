"""
Examples demonstrating usage of Image Enhancement modules
Run these examples to understand the project capabilities
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from modules.web_scraper import WebScraper
from modules.blur_detector import BlurDetector
from modules.image_enhancer import ImageEnhancer


# ==================== Example 1: Web Scraping ====================

def example_web_scraping():
    """
    Example: Download images from a website
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Web Scraping")
    print("="*70)
    
    scraper = WebScraper(output_dir='data')
    
    # Scrape images from a website
    url = "https://unsplash.com"
    print(f"\nScraping images from: {url}")
    
    images = scraper.scrape_images(url, image_limit=3)
    print(f"Downloaded: {len(images)} images")
    print(f"Saved to: data/")


# ==================== Example 2: Blur Detection ====================

def example_blur_detection():
    """
    Example: Detect blur in images
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Blur Detection")
    print("="*70)
    
    detector = BlurDetector(threshold=100)
    
    # Single image detection
    print("\n--- Single Image Detection ---")
    image_path = "data/example.jpg"
    
    if os.path.exists(image_path):
        result = detector.is_blur(image_path)
        print(f"Image: {image_path}")
        print(f"Variance: {result['variance']:.2f}")
        print(f"Blurry: {result['is_blur']}")
    else:
        print(f"Image not found: {image_path}")
    
    # Batch detection
    print("\n--- Batch Detection ---")
    image_paths = ["data/image1.jpg", "data/image2.jpg", "data/image3.jpg"]
    available_images = [img for img in image_paths if os.path.exists(img)]
    
    if available_images:
        results = detector.detect_blur_batch(available_images)
        print(f"Total: {results['total']}")
        print(f"Blurry: {results['blurry_count']}")
        print(f"Clear: {results['clear_count']}")


# ==================== Example 3: Image Enhancement ====================

def example_image_enhancement():
    """
    Example: Enhance image quality
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Image Enhancement")
    print("="*70)
    
    enhancer = ImageEnhancer(output_dir='output')
    
    image_path = "data/blurry_image.jpg"
    
    if os.path.exists(image_path):
        print(f"\nEnhancing: {image_path}")
        
        # Enhance with both sharpening and histogram equalization
        result = enhancer.enhance_image(
            image_path,
            apply_sharpen=True,
            apply_histogram=True,
            kernel_strength=1.0,
            save=True
        )
        
        if result['enhanced'] is not None:
            print(f"✅ Enhancement successful!")
            print(f"Output: {result['output_path']}")
            
            # Compare original and enhanced
            comparison = enhancer.compare_enhancement(image_path)
            print(f"\nEnhancement Statistics:")
            print(f"  Brightness change: {comparison['brightness_change']:.2f}")
            print(f"  Contrast change: {comparison['contrast_change']:.2f}")
    else:
        print(f"Image not found: {image_path}")


# ==================== Example 4: Batch Processing ====================

def example_batch_processing():
    """
    Example: Process multiple images in batch
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Batch Processing")
    print("="*70)
    
    enhancer = ImageEnhancer(output_dir='output')
    
    image_paths = [
        "data/image1.jpg",
        "data/image2.jpg",
        "data/image3.jpg"
    ]
    
    available_images = [img for img in image_paths if os.path.exists(img)]
    
    if available_images:
        print(f"\nProcessing {len(available_images)} images...")
        results = enhancer.enhance_batch(available_images)
        
        successful = sum(1 for r in results if r['success'])
        print(f"\n✅ Successfully processed: {successful} images")
    else:
        print("No images found to process")


# ==================== Example 5: Complete Pipeline ====================

def example_complete_pipeline():
    """
    Example: Complete workflow from scraping to enhancement
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Complete Pipeline")
    print("="*70)
    
    print("\nStep 1: Web Scraping")
    print("-" * 70)
    scraper = WebScraper(output_dir='data')
    url = "https://pexels.com"
    images = scraper.scrape_images(url, image_limit=3)
    print(f"Downloaded {len(images)} images")
    
    if not images:
        print("No images found. Skipping pipeline.")
        return
    
    print("\n\nStep 2: Blur Detection")
    print("-" * 70)
    detector = BlurDetector(threshold=100)
    blur_results = detector.detect_blur_batch(images)
    print(f"Blurry: {blur_results['blurry_count']}")
    print(f"Clear: {blur_results['clear_count']}")
    
    print("\n\nStep 3: Image Enhancement")
    print("-" * 70)
    enhancer = ImageEnhancer(output_dir='output')
    clear_images = [img['path'] for img in blur_results['clear']]
    
    if clear_images:
        results = enhancer.enhance_batch(clear_images)
        print(f"Enhanced {len(results)} images")
    else:
        print("No clear images to enhance")
    
    print("\n" + "="*70)
    print("✅ Pipeline completed!")
    print("="*70)


# ==================== Example 6: Custom Configuration ====================

def example_custom_configuration():
    """
    Example: Configure modules with custom parameters
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: Custom Configuration")
    print("="*70)
    
    # Custom blur threshold
    print("\n--- Custom Blur Threshold ---")
    detector = BlurDetector(threshold=150)  # Higher threshold = stricter
    print(f"Blur threshold set to: {detector.threshold}")
    
    # Custom output directory
    print("\n--- Custom Output Directory ---")
    enhancer = ImageEnhancer(output_dir='custom_output')
    print(f"Output directory: custom_output")
    
    # Change threshold dynamically
    print("\n--- Dynamic Configuration ---")
    detector.set_threshold(80)
    print(f"Threshold updated to: {detector.threshold}")


# ==================== Example 7: Error Handling ====================

def example_error_handling():
    """
    Example: Handling common errors
    """
    print("\n" + "="*70)
    print("EXAMPLE 7: Error Handling")
    print("="*70)
    
    print("\n--- Invalid File Path ---")
    enhancer = ImageEnhancer()
    result = enhancer.enhance_image("nonexistent/path.jpg")
    print(f"Result: {result}")
    
    print("\n--- Invalid URL ---")
    scraper = WebScraper()
    images = scraper.scrape_images("not a valid url")
    print(f"Downloaded: {len(images)} images")
    
    print("\n✅ Errors handled gracefully")


# ==================== Example 8: API Usage ====================

def example_api_usage():
    """
    Example: Using modules programmatically
    """
    print("\n" + "="*70)
    print("EXAMPLE 8: Programmatic API Usage")
    print("="*70)
    
    # Create instances
    scraper = WebScraper(output_dir='data')
    detector = BlurDetector(threshold=100)
    enhancer = ImageEnhancer(output_dir='output')
    
    print("\nModule instances created successfully:")
    print(f"  ✓ WebScraper → {type(scraper).__name__}")
    print(f"  ✓ BlurDetector → {type(detector).__name__}")
    print(f"  ✓ ImageEnhancer → {type(enhancer).__name__}")
    
    print("\nUsing modules programmatically:")
    print("""
    # Download images
    images = scraper.scrape_images(url, limit=10)
    
    # Detect blur
    results = detector.detect_blur_batch(images)
    
    # Enhance images
    enhancer.enhance_batch(results['clear'])
    """)


# ==================== Main ====================

def main():
    """Run all examples"""
    
    print("\n" + "█"*70)
    print("IMAGE ENHANCEMENT - COMPREHENSIVE EXAMPLES")
    print("█"*70)
    
    examples = [
        ("1", "Web Scraping", example_web_scraping),
        ("2", "Blur Detection", example_blur_detection),
        ("3", "Image Enhancement", example_image_enhancement),
        ("4", "Batch Processing", example_batch_processing),
        ("5", "Complete Pipeline", example_complete_pipeline),
        ("6", "Custom Configuration", example_custom_configuration),
        ("7", "Error Handling", example_error_handling),
        ("8", "API Usage", example_api_usage),
    ]
    
    print("\nAvailable Examples:")
    for num, title, _ in examples:
        print(f"  {num}. {title}")
    print(f"  0. Run all examples")
    print(f"  q. Quit")
    
    choice = input("\nSelect example (0-8, q to quit): ").strip().lower()
    
    if choice == '0':
        for num, title, func in examples:
            try:
                func()
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
