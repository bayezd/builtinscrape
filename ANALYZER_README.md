# SDR Job Listings Analyzer

This script analyzes the scraped markdown files from builtin.com job listings using OpenRouter with Gemini 2.5 Pro to extract company information.

## Features

- Analyzes markdown files containing job listings
- Uses Gemini 2.5 Pro via OpenRouter to extract company information
- Aggregates results across multiple files
- Outputs detailed JSON reports

## Requirements

- Python 3.6+
- Required Python packages:
  - requests
  - python-dotenv

## Installation

1. Install the required packages:

```bash
pip install requests python-dotenv
```

2. Copy the `.env.example` file to `.env` and add your OpenRouter API key:

```bash
cp .env.example .env
```

Then edit the `.env` file and replace `your_api_key_here` with your actual OpenRouter API key.

## Usage

### Basic Usage

```bash
python analyze.py --api-key YOUR_OPENROUTER_API_KEY
```

This will analyze all markdown files in the `scraped_content/sdr_scrape` directory.

### Specifying a Different Directory

```bash
python analyze.py --dir path/to/markdown/files
```

### Limiting the Number of Files to Analyze

```bash
python analyze.py --limit 5
```

This will analyze only the first 5 files.

### Specifying an Output File

```bash
python analyze.py --output my_analysis.json
```

### Full Command-line Options

```bash
python analyze.py --help
```

## Output

The script produces two JSON files:

1. `company_analysis.json` (or the name specified with `--output`): Contains the detailed analysis of each file
2. `company_analysis_aggregated.json`: Contains the aggregated results across all files

The aggregated results file contains:
- A list of all companies found
- The number of job listings for each company
- The job titles associated with each company
- Total number of companies
- Total number of job listings

## Example

```bash
python analyze.py --limit 3
```

This will analyze the first 3 markdown files in the default directory and save the results to `company_analysis.json` and `company_analysis_aggregated.json`.

## How It Works

1. The script reads all markdown files in the specified directory
2. For each file, it sends the content to Gemini 2.5 Pro via OpenRouter
3. Gemini analyzes the content and extracts company information
4. The script aggregates the results across all files
5. The results are saved to JSON files

## License

MIT
