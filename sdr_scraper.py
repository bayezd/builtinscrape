#!/usr/bin/env python3
"""
SDR Job Listings Scraper

This script scrapes Sales Development Representative job listings from builtin.com
and saves them as markdown files in the sdr_scrape folder.
"""

import os
import sys
import csv
import time
from scrape import scrape_url, DEFAULT_API_KEY

# Path to the CSV file containing URLs
CSV_FILE = "sdr_urls.csv"

# Output directory for the scraped content
OUTPUT_DIR = "scraped_content/sdr_scrape"

def ensure_directory_exists(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def read_urls_from_csv(csv_file):
    """Read URLs from a CSV file."""
    urls = []
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'url' in row:
                    urls.append(row['url'])
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []
    
    return urls

def main():
    """Main function."""
    # Ensure the output directory exists
    ensure_directory_exists(OUTPUT_DIR)
    
    # Read URLs from the CSV file
    urls = read_urls_from_csv(CSV_FILE)
    
    if not urls:
        print(f"Error: No URLs found in '{CSV_FILE}'")
        return 1
    
    print(f"Found {len(urls)} URLs in '{CSV_FILE}'")
    
    # Scrape each URL
    success_count = 0
    for i, url in enumerate(urls):
        print(f"\nScraping URL {i+1}/{len(urls)}: {url}")
        success = scrape_url(url, DEFAULT_API_KEY, OUTPUT_DIR)
        
        if success:
            success_count += 1
        
        # Add a delay between requests to avoid rate limiting
        if i < len(urls) - 1:
            print("Waiting 2 seconds before next request...")
            time.sleep(2)
    
    # Print summary
    print("\nScraping Summary:")
    print(f"Successfully scraped {success_count}/{len(urls)} URLs")
    
    if success_count < len(urls):
        print("\nFailed URLs:")
        for i, url in enumerate(urls):
            if not scrape_url(url, DEFAULT_API_KEY, OUTPUT_DIR, dry_run=True):
                print(f"- URL {i+1}: {url}")
    
    return 0 if success_count == len(urls) else 1

if __name__ == "__main__":
    sys.exit(main())
