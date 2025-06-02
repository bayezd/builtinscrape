#!/usr/bin/env python3
"""
Batch Scraper for Firecrawl

This script reads a list of URLs from a file and scrapes them using the scrape.py script.
"""

import os
import sys
import argparse
from scrape import scrape_urls, DEFAULT_API_KEY, DEFAULT_OUTPUT_DIR

def read_urls_from_file(file_path):
    """Read URLs from a file, one URL per line."""
    with open(file_path, 'r') as f:
        # Strip whitespace and skip empty lines
        urls = [line.strip() for line in f if line.strip()]
    return urls

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Batch scrape web pages from a file')
    parser.add_argument('file', help='File containing URLs to scrape (one URL per line)')
    parser.add_argument('--api-key', '-k', default=DEFAULT_API_KEY, help='API key for FirecrawlApp')
    parser.add_argument('--output-dir', '-o', default=DEFAULT_OUTPUT_DIR, help='Directory to save the scraped content')
    return parser.parse_args()

def main():
    """Main function."""
    args = parse_arguments()
    
    # Check if the file exists
    if not os.path.isfile(args.file):
        print(f"Error: File '{args.file}' not found")
        return 1
    
    # Read URLs from the file
    urls = read_urls_from_file(args.file)
    
    if not urls:
        print(f"Error: No URLs found in '{args.file}'")
        return 1
    
    print(f"Found {len(urls)} URLs in '{args.file}'")
    
    # Scrape the URLs
    results = scrape_urls(urls, args.api_key, args.output_dir)
    
    # Print summary
    print("\nScraping Summary:")
    success_count = sum(1 for success in results.values() if success)
    print(f"Successfully scraped {success_count}/{len(results)} URLs")
    
    if success_count < len(results):
        print("\nFailed URLs:")
        for url, success in results.items():
            if not success:
                print(f"- {url}")
    
    return 0 if success_count == len(results) else 1

if __name__ == "__main__":
    sys.exit(main())
