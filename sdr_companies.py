#!/usr/bin/env python3
"""
SDR Companies Extractor

This script extracts companies with SDR-related job titles from the company_analysis_aggregated.json file
and saves them to a CSV file.
"""

import json
import csv
import os
import re

def is_sdr_job(job_title):
    """
    Check if a job title is SDR-related.
    
    Args:
        job_title: The job title to check
        
    Returns:
        True if the job title is SDR-related, False otherwise
    """
    sdr_keywords = [
        'sales development representative',
        'sdr',
        'bdr',
        'business development representative',
        'sales development rep',
        'business development rep'
    ]
    
    job_title_lower = job_title.lower()
    
    for keyword in sdr_keywords:
        if keyword in job_title_lower:
            return True
    
    return False

def extract_sdr_companies(json_file, csv_file):
    """
    Extract companies with SDR-related job titles and save to CSV.
    
    Args:
        json_file: Path to the JSON file
        csv_file: Path to the output CSV file
    """
    try:
        # Read the JSON file
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract companies data
        all_companies = data.get('companies', [])
        
        if not all_companies:
            print(f"No companies found in {json_file}")
            return False
        
        # Filter companies with SDR-related job titles
        sdr_companies = []
        for company in all_companies:
            sdr_job_titles = [title for title in company['job_titles'] if is_sdr_job(title)]
            
            if sdr_job_titles:
                sdr_companies.append({
                    'name': company['name'],
                    'job_count': len(sdr_job_titles),
                    'job_titles': sdr_job_titles
                })
        
        # Sort by job count (descending)
        sdr_companies.sort(key=lambda x: x['job_count'], reverse=True)
        
        # Write to CSV
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            # Define CSV columns
            fieldnames = ['Company Name', 'SDR Job Count', 'SDR Job Titles']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write data
            for company in sdr_companies:
                writer.writerow({
                    'Company Name': company['name'],
                    'SDR Job Count': company['job_count'],
                    'SDR Job Titles': ', '.join(company['job_titles'])
                })
        
        print(f"Successfully extracted SDR companies to {csv_file}")
        print(f"Found {len(sdr_companies)} companies with SDR-related job titles")
        return True
    
    except Exception as e:
        print(f"Error extracting SDR companies: {e}")
        return False

def main():
    # File paths
    json_file = "company_analysis_aggregated.json"
    csv_file = "sdr_companies.csv"
    
    # Check if JSON file exists
    if not os.path.isfile(json_file):
        print(f"Error: {json_file} not found")
        return 1
    
    # Extract SDR companies and save to CSV
    success = extract_sdr_companies(json_file, csv_file)
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
