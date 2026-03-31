"""
Main entry point for Image Enhancement project
Demonstrates core functionality of all modules
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from modules.web_scraper import WebScraper
from modules.blur_detector import BlurDetector
from modules.image_enhancer import ImageEnhancer


def main():
    """Main application flow"""
    
    print("\n" + "="*70)
    print("🖼️  IMAGE ENHANCEMENT PROJECT - MAIN ENTRY POINT")
    print("="*70)
    
    # Create output directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    os.makedirs('temp_images', exist_ok=True)
    
    # Display available operations
    print("\nAvailable Operations:")
    print("1. Web Scraping   - Download images from websites")
    print("2. Blur Detection - Analyze image sharpness")
    print("3. Enhancement   - Sharpen and improve contrast")
    print("4. Full Pipeline  - Complete workflow")
    print("5. View Results   - Check output directory")
    
    choice = input("\nSelect operation (1-5): ").strip()
    
    if choice == '1':
        web_scraping_demo()
    elif choice == '2':
        blur_detection_demo()
    elif choice == '3':
        enhancement_demo()
    elif choice == '4':
        full_pipeline_demo()
    elif choice == '5':
        show_results()
    else:
        print("Invalid selection")


def web_scraping_demo():
    """Demonstrate web scraping functionality"""
    print("\n" + "-"*70)
    print("🌐 WEB SCRAPING DEMO")
    print("-"*70)
    
    scraper = WebScraper(output_dir='data')
    
    url = input("Enter website URL (or press Enter for example): ").strip()
    if not url:
        url = "https://example.com"
    
    limit = input("Number of images to download (default 5): ").strip()
    limit = int(limit) if limit.isdigit() else 5
    
    images = scraper.scrape_images(url, limit)
    print(f"\n✅ Downloaded {len(images)} images to 'data' directory")


def blur_detection_demo():
    """Demonstrate blur detection functionality"""
    print("\n" + "-"*70)
    print("📊 BLUR DETECTION DEMO")
    print("-"*70)
    
    detector = BlurDetector(threshold=100)
    
    image_path = input("Enter path to image file: ").strip()
    
    if os.path.exists(image_path):
        result = detector.is_blur(image_path)
        
        print(f"\nImage: {image_path}")
        print(f"Laplacian Variance: {result['variance']:.2f}")
        print(f"Threshold: {result['threshold']}")
        print(f"Status: {'BLURRY ❌' if result['is_blur'] else 'CLEAR ✅'}")
    else:
        print(f"Error: File not found - {image_path}")


def enhancement_demo():
    """Demonstrate image enhancement functionality"""
    print("\n" + "-"*70)
    print("✨ IMAGE ENHANCEMENT DEMO")
    print("-"*70)
    
    enhancer = ImageEnhancer(output_dir='output')
    
    image_path = input("Enter path to image file: ").strip()
    
    if os.path.exists(image_path):
        result = enhancer.enhance_image(image_path, apply_sharpen=True, 
                                       apply_histogram=True)
        
        if result['enhanced'] is not None:
            print(f"\n✅ Image enhanced successfully!")
            print(f"Output: {result['output_path']}")
            
            # Show statistics
            comparison = enhancer.compare_enhancement(image_path)
            if comparison:
                print(f"\nEnhancement Statistics:")
                print(f"  Brightness Change: {comparison['brightness_change']:.2f}")
                print(f"  Contrast Change: {comparison['contrast_change']:.2f}")
        else:
            print("❌ Enhancement failed")
    else:
        print(f"Error: File not found - {image_path}")


def full_pipeline_demo():
    """Demonstrate complete pipeline"""
    print("\n" + "-"*70)
    print("🔄 FULL PIPELINE DEMO")
    print("-"*70)
    print("\nThis demonstrates: Scrape → Detect → Enhance\n")
    
    # Step 1: Scrape
    print("Step 1: Web Scraping")
    print("─" * 70)
    scraper = WebScraper(output_dir='data')
    url = input("Enter website URL (or press Enter for example): ").strip()
    if not url:
        url = "https://example.com"
    
    images = scraper.scrape_images(url, limit=3)
    
    if not images:
        print("No images downloaded. Exiting pipeline.")
        return
    
    # Step 2: Detect Blur
    print("\n\nStep 2: Blur Detection")
    print("─" * 70)
    detector = BlurDetector(threshold=100)
    results = detector.detect_blur_batch(images)
    
    print(f"Blurry: {results['blurry_count']} | Clear: {results['clear_count']}")
    
    # Step 3: Enhance
    print("\n\nStep 3: Image Enhancement")
    print("─" * 70)
    enhancer = ImageEnhancer(output_dir='output')
    clear_images = [img['path'] for img in results['clear']]
    
    if clear_images:
        enhance_results = enhancer.enhance_batch(clear_images)
        print(f"\n✅ Enhanced {len(enhance_results)} images")
    else:
        print("No clear images to enhance")
    
    print("\n✅ Pipeline completed!")


def show_results():
    """Display results from output directory"""
    print("\n" + "-"*70)
    print("📁 RESULTS")
    print("-"*70)
    
    output_dir = 'output'
    
    if not os.path.exists(output_dir):
        print(f"Output directory not found: {output_dir}")
        return
    
    files = os.listdir(output_dir)
    
    if not files:
        print("No files in output directory")
    else:
        print(f"\nEnhanced images in '{output_dir}':")
        for idx, file in enumerate(files, 1):
            filepath = os.path.join(output_dir, file)
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"  {idx}. {file} ({size_mb:.2f} MB)")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Application terminated by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
