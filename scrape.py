#!/usr/bin/env python3
"""
Firecrawl Web Scraper

This script uses the firecrawl-py library to scrape web pages and save the content as markdown files.
Usage:
    python scrape.py [url1] [url2] ...

If no URLs are provided, it will use the default URL.
"""

import os
import sys
import time
import argparse
from datetime import datetime
from typing import List, Dict, Any, Optional
from firecrawl import FirecrawlApp

# Default API key for FirecrawlApp
DEFAULT_API_KEY = 'fc-fe433028de91410d9107ea99bdaef872'

# Default URL to scrape if none is provided
DEFAULT_URL = 'https://builtin.com/jobs/remote/hybrid/office/51-200/201-500?search=Sales+Development+Representative&country=USA&allLocations=true'

# Default directory to save the scraped content
DEFAULT_OUTPUT_DIR = "scraped_content"

def ensure_directory_exists(directory: str) -> None:
    """Create directory if it doesn't exist.

    Args:
        directory: Path to the directory to create
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def clean_filename(url: str) -> str:
    """Create a clean filename from a URL.

    Args:
        url: The URL to convert to a filename

    Returns:
        A cleaned filename
    """
    # Remove protocol and domain parts
    filename = url.split("//")[-1]

    # Replace special characters
    for char in ['/', '?', '&', '=', ':', '#', '%', '+', ' ', '<', '>', '|', '"', '*']:
        filename = filename.replace(char, '_')

    # Limit filename length
    if len(filename) > 200:
        filename = filename[:200]

    return filename

def save_markdown_content(content: str, url: str, output_dir: str = DEFAULT_OUTPUT_DIR) -> str:
    """Save markdown content to a file.

    Args:
        content: The markdown content to save
        url: The URL that was scraped
        output_dir: Directory to save the file in

    Returns:
        The path to the saved file
    """
    # Create a filename based on the URL
    filename = clean_filename(url)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename}_{timestamp}.md"

    # Ensure the output directory exists
    ensure_directory_exists(output_dir)

    # Save the content to a file
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Saved markdown content to: {filepath}")
    return filepath

def extract_markdown_from_response(response: Any) -> Optional[str]:
    """Extract markdown content from the response.

    Args:
        response: The response from the FirecrawlApp

    Returns:
        The markdown content or None if it couldn't be extracted
    """
    if response is None:
        return None

    # Check if response is a dictionary with a 'markdown' key
    if isinstance(response, dict) and 'markdown' in response:
        return response['markdown']

    # Check if response has a markdown attribute (could be a custom object)
    if hasattr(response, 'markdown'):
        return response.markdown

    # If response is a string, it might be the markdown content directly
    if isinstance(response, str):
        return response

    # If we get here, we couldn't extract the markdown
    print("Error: Could not extract markdown content from the response")
    print(f"Response type: {type(response)}")
    print(f"Response: {response}")
    return None

def scrape_url(url: str, api_key: str, output_dir: str = DEFAULT_OUTPUT_DIR, dry_run: bool = False) -> bool:
    """Scrape a URL and save the markdown content.

    Args:
        url: The URL to scrape
        api_key: The API key for FirecrawlApp
        output_dir: Directory to save the scraped content
        dry_run: If True, only check if the URL is valid without actually scraping

    Returns:
        True if the scraping was successful, False otherwise
    """
    # If dry_run is True, just return True (assume it would succeed)
    if dry_run:
        return True

    try:
        app = FirecrawlApp(api_key=api_key)

        print(f"Scraping URL: {url}")
        response = app.scrape_url(
            url=url,
            formats=['markdown']
        )

        # Extract markdown content
        markdown_content = extract_markdown_from_response(response)
        if markdown_content:
            filepath = save_markdown_content(markdown_content, url, output_dir)
            return True
        else:
            print("Error: No markdown content could be extracted")
            return False

    except Exception as e:
        print(f"Error scraping URL: {e}")
        return False

def scrape_urls(urls: List[str], api_key: str, output_dir: str = DEFAULT_OUTPUT_DIR, dry_run: bool = False) -> Dict[str, bool]:
    """Scrape multiple URLs and save the markdown content.

    Args:
        urls: List of URLs to scrape
        api_key: The API key for FirecrawlApp
        output_dir: Directory to save the scraped content
        dry_run: If True, only check if the URLs are valid without actually scraping

    Returns:
        Dictionary mapping URLs to success status
    """
    results = {}

    for i, url in enumerate(urls):
        if not dry_run:
            print(f"\nScraping URL {i+1}/{len(urls)}: {url}")
        success = scrape_url(url, api_key, output_dir, dry_run)
        results[url] = success

        # Add a small delay between requests to avoid rate limiting
        if not dry_run and i < len(urls) - 1:
            time.sleep(1)

    return results

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Scrape web pages and save as markdown using firecrawl-py')
    parser.add_argument('urls', nargs='*', help='URLs to scrape')
    parser.add_argument('--api-key', '-k', default=DEFAULT_API_KEY, help='API key for FirecrawlApp')
    parser.add_argument('--output-dir', '-o', default=DEFAULT_OUTPUT_DIR, help='Directory to save the scraped content')
    return parser.parse_args()

def main():
    """Main function."""
    args = parse_arguments()

    # Use provided URLs or default URL
    urls = args.urls if args.urls else [DEFAULT_URL]

    # Scrape the URLs and save the content
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