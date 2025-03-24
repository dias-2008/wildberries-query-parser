# Wildberries Product Scraper

A Python script that scrapes product information from Wildberries and generates a clean HTML output of search results.

## Usage
## clone repository: git clone https://github.com/dias-2008/wildberries-query-parser.git
1. Run the script:
   ```bash
   python wildberries_scraper.py
   ```
2. Enter your search query when prompted.
3. The results will be saved in `wildberries_results.html`.
4. Open the HTML file in your browser to view the results.

## Output
The script generates an HTML file with:

- Bootstrap-based responsive layout.
- Product cards showing:
  - Product image.
  - Product name.
  - Price in rubles.
  - Link to the product page.
- Hover animations on product cards.

## Features
- Search products on Wildberries.
- Display results in a responsive grid layout.
- Interactive product cards with hover effects.
- Direct links to product pages.
- Price display in rubles.
- Product image previews.

## Notes
- The script uses Wildberries' search API.
- Results are limited to 50 products per search.
- Rate limiting is implemented (1 second between requests).
- Error handling for API requests and data processing.

## Requirements
- Python 3.6+
- Required packages:
  - `requests`
  - `beautifulsoup4`
  - `urllib3`

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd wildberries_scraper
   ```
2. Install the required packages:
   ```bash
   pip install requests beautifulsoup4 urllib3
   

