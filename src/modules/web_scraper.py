"""
Web Scraper Module
Handles web scraping of images using requests and BeautifulSoup
"""

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse


class WebScraper:
    """Web scraper for downloading images from web pages"""
    
    def __init__(self, output_dir='data'):
        """
        Initialize the web scraper
        
        Args:
            output_dir (str): Directory to save downloaded images
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_images(self, url, image_limit=10):
        """
        Scrape images from a given URL
        
        Args:
            url (str): URL of the webpage to scrape
            image_limit (int): Maximum number of images to download
            
        Returns:
            list: List of downloaded image file paths
        """
        downloaded_images = []
        
        try:
            print(f"Fetching webpage: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            img_tags = soup.find_all('img')
            
            print(f"Found {len(img_tags)} images on the page")
            
            for idx, img in enumerate(img_tags[:image_limit]):
                try:
                    img_url = img.get('src') or img.get('data-src')
                    
                    if not img_url:
                        continue
                    
                    # Convert relative URLs to absolute
                    img_url = urljoin(url, img_url)
                    
                    # Download the image
                    img_response = self.session.get(img_url, timeout=10)
                    img_response.raise_for_status()
                    
                    # Extract filename from URL
                    parsed_url = urlparse(img_url)
                    filename = os.path.basename(parsed_url.path)
                    
                    if not filename or '.' not in filename:
                        filename = f"image_{idx}.jpg"
                    
                    filepath = os.path.join(self.output_dir, filename)
                    
                    # Save image
                    with open(filepath, 'wb') as f:
                        f.write(img_response.content)
                    
                    downloaded_images.append(filepath)
                    print(f"Downloaded: {filename}")
                    
                except Exception as e:
                    print(f"Error downloading image: {e}")
                    continue
            
            print(f"Successfully downloaded {len(downloaded_images)} images")
            return downloaded_images
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching webpage: {e}")
            return []
    
    def scrape_multiple_urls(self, urls, images_per_url=5):
        """
        Scrape images from multiple URLs
        
        Args:
            urls (list): List of URLs to scrape
            images_per_url (int): Number of images to download per URL
            
        Returns:
            list: List of all downloaded image file paths
        """
        all_images = []
        
        for url in urls:
            print(f"\n--- Processing URL: {url} ---")
            images = self.scrape_images(url, images_per_url)
            all_images.extend(images)
        
        return all_images
