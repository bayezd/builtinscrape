#!/usr/bin/env python3
"""
JSON to CSV Converter

This script converts the company_analysis_aggregated.json file to a CSV file.
"""

import json
import csv
import os

def json_to_csv(json_file, csv_file):
    """
    Convert JSON data to CSV format.
    
    Args:
        json_file: Path to the JSON file
        csv_file: Path to the output CSV file
    """
    try:
        # Read the JSON file
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract companies data
        companies = data.get('companies', [])
        
        if not companies:
            print(f"No companies found in {json_file}")
            return False
        
        # Write to CSV
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            # Define CSV columns
            fieldnames = ['Company Name', 'Job Count', 'Job Titles']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write data
            for company in companies:
                writer.writerow({
                    'Company Name': company['name'],
                    'Job Count': company['job_count'],
                    'Job Titles': ', '.join(company['job_titles'])
                })
        
        print(f"Successfully converted {json_file} to {csv_file}")
        print(f"Wrote data for {len(companies)} companies")
        return True
    
    except Exception as e:
        print(f"Error converting JSON to CSV: {e}")
        return False

def main():
    # File paths
    json_file = "company_analysis_aggregated.json"
    csv_file = "company_analysis.csv"
    
    # Check if JSON file exists
    if not os.path.isfile(json_file):
        print(f"Error: {json_file} not found")
        return 1
    
    # Convert JSON to CSV
    success = json_to_csv(json_file, csv_file)
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
