# Firecrawl Web Scraper

A Python script that uses the firecrawl-py library to scrape web pages and save the content as markdown files.

## Features

- Scrape web pages and save the content as markdown files
- Support for scraping multiple URLs in a single run
- Command-line interface with customizable options
- Error handling and logging
- Saves both markdown content and the full API response

## Requirements

- Python 3.6+
- firecrawl-py library

## Installation

1. Install the firecrawl-py library:

```bash
pip install firecrawl-py
```

2. Clone this repository or download the script.

## Usage

### Basic Usage

```bash
python scrape.py
```

This will scrape the default URL and save the content to the `scraped_content` directory.

### Scraping Multiple URLs

```bash
python scrape.py "https://example.com" "https://example.org"
```

### Customizing Output Directory

```bash
python scrape.py --output-dir my_scraped_content
```

### Using a Different API Key

```bash
python scrape.py --api-key your-api-key
```

### Full Command-line Options

```bash
python scrape.py --help
```

## Output

The script saves a markdown file for each scraped URL containing the scraped content.

The files are saved in the output directory (default: `scraped_content`) with filenames based on the URL and a timestamp.

## Example

```bash
python scrape.py "https://builtin.com/jobs/remote/hybrid/office/51-200/201-500?search=Software+Engineer&country=USA&allLocations=true"
```

This will scrape the specified URL and save the content to a file like:

- `scraped_content/builtin.com_jobs_remote_hybrid_office_51-200_201-500_search_Software_Engineer_country_USA_allLocations_true_20250513_143804.md`

## License

MIT
