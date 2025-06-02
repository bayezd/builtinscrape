#!/usr/bin/env python3
"""
SDR Job Listings Analyzer

This script analyzes the scraped markdown files from builtin.com job listings
using OpenRouter with Gemini 2.5 Pro to extract company information.
"""

import os
import json
import glob
import requests
import argparse
from typing import List, Dict, Any, Optional
import time
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Default directory containing the scraped markdown files
DEFAULT_SCRAPE_DIR = "scraped_content/sdr_scrape"

# OpenRouter API key - get from environment variable or set directly
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# OpenRouter API endpoint
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def read_markdown_file(file_path: str) -> str:
    """Read the content of a markdown file.
    
    Args:
        file_path: Path to the markdown file
        
    Returns:
        The content of the file as a string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

def get_markdown_files(directory: str) -> List[str]:
    """Get all markdown files in a directory.
    
    Args:
        directory: Directory to search for markdown files
        
    Returns:
        List of paths to markdown files
    """
    return glob.glob(os.path.join(directory, "*.md"))

def analyze_with_gemini(content: str, api_key: str) -> Dict[str, Any]:
    """Analyze markdown content using Gemini 2.5 Pro via OpenRouter.
    
    Args:
        content: Markdown content to analyze
        api_key: OpenRouter API key
        
    Returns:
        Dictionary containing the analysis results
    """
    # Prepare the prompt for Gemini
    prompt = """
    Analyze the following job listing content from builtin.com and extract a list of all companies mentioned.
    For each company, provide:
    1. Company name
    2. Number of job listings for this company (count how many times it appears)
    3. Job titles associated with this company
    
    Format your response as a JSON object with the following structure:
    {
        "companies": [
            {
                "name": "Company Name",
                "job_count": 3,
                "job_titles": ["Sales Development Representative", "SDR Team Lead", "etc"]
            },
            ...
        ],
        "total_companies": 15,
        "total_jobs": 25
    }
    
    Only include companies that are hiring for jobs, not companies mentioned in other contexts.
    Here's the content:
    
    """
    
    # Truncate content if it's too long (Gemini has context limits)
    max_content_length = 100000  # Adjust based on model limits
    if len(content) > max_content_length:
        content = content[:max_content_length] + "...[content truncated due to length]"
    
    full_prompt = prompt + content
    
    try:
        response = requests.post(
            url=OPENROUTER_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "google/gemini-2.5-pro-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": full_prompt
                            }
                        ]
                    }
                ],
            }),
            timeout=60  # Set a timeout for the request
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse the response
        result = response.json()
        
        # Extract the content from the response
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
            
            # Try to parse the JSON from the content
            try:
                # Find JSON in the response (it might be surrounded by markdown code blocks)
                json_start = content.find('{')
                json_end = content.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = content[json_start:json_end]
                    return json.loads(json_str)
                else:
                    print("No JSON found in the response")
                    return {"error": "No JSON found in the response", "raw_response": content}
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON from response: {e}")
                return {"error": f"JSON parsing error: {e}", "raw_response": content}
        else:
            print("Unexpected response format")
            return {"error": "Unexpected response format", "raw_response": result}
            
    except requests.exceptions.RequestException as e:
        print(f"Error making request to OpenRouter: {e}")
        return {"error": f"Request error: {e}"}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": f"Unexpected error: {e}"}

def analyze_files(files: List[str], api_key: str, output_file: str = "company_analysis.json") -> None:
    """Analyze multiple markdown files and save the results.
    
    Args:
        files: List of markdown files to analyze
        api_key: OpenRouter API key
        output_file: Path to save the analysis results
    """
    all_results = {
        "files_analyzed": len(files),
        "analyses": []
    }
    
    # Process each file
    for i, file_path in enumerate(files):
        print(f"Analyzing file {i+1}/{len(files)}: {os.path.basename(file_path)}")
        
        # Read the file content
        content = read_markdown_file(file_path)
        if not content:
            print(f"Skipping empty file: {file_path}")
            continue
        
        # Analyze the content
        result = analyze_with_gemini(content, api_key)
        
        # Add the result to the list
        all_results["analyses"].append({
            "file": os.path.basename(file_path),
            "result": result
        })
        
        # Save intermediate results after each file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2)
        
        # Add a delay to avoid rate limiting
        if i < len(files) - 1:
            print("Waiting 2 seconds before next analysis...")
            time.sleep(2)
    
    print(f"Analysis complete. Results saved to {output_file}")
    
    # Aggregate results across all files
    aggregate_results(all_results, output_file.replace('.json', '_aggregated.json'))

def aggregate_results(all_results: Dict[str, Any], output_file: str) -> None:
    """Aggregate results from multiple file analyses.
    
    Args:
        all_results: Dictionary containing all analysis results
        output_file: Path to save the aggregated results
    """
    company_data = {}
    total_jobs = 0
    
    # Process each file's analysis
    for analysis in all_results["analyses"]:
        result = analysis["result"]
        
        # Skip if there was an error or no companies
        if "error" in result or "companies" not in result:
            continue
        
        # Process each company
        for company in result["companies"]:
            name = company["name"]
            job_count = company.get("job_count", 0)
            job_titles = company.get("job_titles", [])
            
            # Add or update company data
            if name in company_data:
                company_data[name]["job_count"] += job_count
                company_data[name]["job_titles"].extend(job_titles)
                # Remove duplicates from job titles
                company_data[name]["job_titles"] = list(set(company_data[name]["job_titles"]))
            else:
                company_data[name] = {
                    "job_count": job_count,
                    "job_titles": job_titles
                }
            
            total_jobs += job_count
    
    # Create the aggregated results
    aggregated = {
        "companies": [
            {
                "name": name,
                "job_count": data["job_count"],
                "job_titles": data["job_titles"]
            }
            for name, data in company_data.items()
        ],
        "total_companies": len(company_data),
        "total_jobs": total_jobs
    }
    
    # Sort companies by job count (descending)
    aggregated["companies"].sort(key=lambda x: x["job_count"], reverse=True)
    
    # Save the aggregated results
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(aggregated, f, indent=2)
    
    print(f"Aggregated results saved to {output_file}")
    print(f"Found {aggregated['total_companies']} companies with {aggregated['total_jobs']} job listings")

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Analyze scraped job listings using Gemini 2.5 Pro')
    parser.add_argument('--dir', '-d', default=DEFAULT_SCRAPE_DIR, help='Directory containing scraped markdown files')
    parser.add_argument('--api-key', '-k', default=OPENROUTER_API_KEY, help='OpenRouter API key')
    parser.add_argument('--output', '-o', default="company_analysis.json", help='Output file for analysis results')
    parser.add_argument('--limit', '-l', type=int, default=0, help='Limit the number of files to analyze (0 for all)')
    return parser.parse_args()

def main():
    """Main function."""
    args = parse_arguments()
    
    # Check if API key is provided
    if not args.api_key:
        print("Error: OpenRouter API key is required")
        print("Set it using the --api-key parameter or OPENROUTER_API_KEY environment variable")
        return 1
    
    # Get markdown files
    files = get_markdown_files(args.dir)
    if not files:
        print(f"Error: No markdown files found in {args.dir}")
        return 1
    
    print(f"Found {len(files)} markdown files in {args.dir}")
    
    # Limit the number of files if requested
    if args.limit > 0 and args.limit < len(files):
        print(f"Limiting analysis to {args.limit} files")
        files = files[:args.limit]
    
    # Analyze the files
    analyze_files(files, args.api_key, args.output)
    
    return 0

if __name__ == "__main__":
    exit(main())
