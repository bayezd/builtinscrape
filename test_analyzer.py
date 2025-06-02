#!/usr/bin/env python3
"""
Test script for the SDR Job Listings Analyzer

This script demonstrates how to use the analyzer with a single file.
"""

import os
import sys
from analyze import analyze_with_gemini, read_markdown_file
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Get the OpenRouter API key from environment variable
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

def main():
    """Main function."""
    # Check if API key is provided
    if not OPENROUTER_API_KEY:
        print("Error: OpenRouter API key is required")
        print("Set it in the .env file or as an environment variable")
        return 1
    
    # Path to a sample markdown file
    sample_file = "scraped_content/sdr_scrape/builtin.com_jobs_search_Sales_20Development_20Representative_country_USA_allLocations_true_20250513_145447.md"
    
    # Check if the file exists
    if not os.path.isfile(sample_file):
        print(f"Error: Sample file not found: {sample_file}")
        print("Please provide a valid path to a markdown file")
        return 1
    
    print(f"Reading file: {sample_file}")
    content = read_markdown_file(sample_file)
    
    print("Analyzing content with Gemini 2.5 Pro...")
    result = analyze_with_gemini(content, OPENROUTER_API_KEY)
    
    print("\nAnalysis Result:")
    if "error" in result:
        print(f"Error: {result['error']}")
        return 1
    
    print(f"Found {result.get('total_companies', 0)} companies with {result.get('total_jobs', 0)} job listings")
    
    # Print the top 5 companies by job count
    companies = result.get("companies", [])
    if companies:
        print("\nTop Companies:")
        for i, company in enumerate(companies[:5]):
            print(f"{i+1}. {company['name']} - {company['job_count']} job(s)")
            print(f"   Job Titles: {', '.join(company['job_titles'][:3])}")
            if len(company['job_titles']) > 3:
                print(f"   ... and {len(company['job_titles']) - 3} more")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
