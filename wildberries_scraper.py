import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import quote
import time

class WildberriesScraper:
    def __init__(self):
        # Updated API endpoint
        self.base_url = "https://search.wb.ru/exactmatch/ru/common/v4/search"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Origin": "https://www.wildberries.ru",
            "Referer": "https://www.wildberries.ru/"
        }

    def get_products(self, query, limit=50):
        try:
            encoded_query = quote(query)
            url = f"{self.base_url}?query={encoded_query}&resultset=catalog&limit={limit}&sort=popular&page=1&appType=1&curr=rub&dest=-1257786"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            # Navigate through the correct data structure
            products = data.get('data', {}).get('products', [])
            
            if not products:
                print(f"Debug - Response structure: {data['data'].keys() if 'data' in data else 'No data key'}")
            return products
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return []

    def generate_html(self, products, query):
        html_head = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wildberries Search Results</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>'''

        html_body = f'''<body>
    <div class="container py-4">
        <h1 class="mb-4">Search Results for: {query}</h1>
        <div class="row row-cols-1 row-cols-md-3 g-4">'''

        html_end = '''</div>
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const cards = document.querySelectorAll('.product-card');
            cards.forEach(card => {
                card.style.transition = 'transform 0.2s';
                card.addEventListener('mouseenter', () => card.style.transform = 'scale(1.02)');
                card.addEventListener('mouseleave', () => card.style.transform = 'scale(1)');
            });
        });
    </script>
</body>
</html>'''

        product_card_template = '''<div class="col">
    <div class="card h-100 product-card">
        <img src="https://images.wbstatic.net/c246x328/new/{image_id}.jpg" class="card-img-top" alt="{name}">
        <div class="card-body">
            <h5 class="card-title">{name}</h5>
            <p class="card-text">Price: {price} ₽</p>
            <a href="https://www.wildberries.ru/catalog/{id}/detail.aspx" class="btn btn-primary" target="_blank">View Product</a>
        </div>
    </div>
</div>'''

        product_cards = []
        for product in products:
            try:
                # Handle potential missing fields more gracefully
                name = str(product.get('name', 'No name available'))
                price = int(product.get('salePriceU', 0)) // 100
                product_id = str(product.get('id', ''))
                image_id = product_id.zfill(5)

                product_cards.append(product_card_template.format(
                    name=name,
                    price=price,
                    id=product_id,
                    image_id=image_id
                ))
            except Exception as e:
                print(f"Error processing product: {e}")
                continue

        cards_html = '\n'.join(product_cards) if product_cards else 'No products found'
        return html_head + html_body + cards_html + html_end

def main():
    scraper = WildberriesScraper()
    
    try:
        while True:
            query = input("\nEnter search query (or 'quit' to exit): ").strip()
            if query.lower() == 'quit':
                break

            print("Fetching products...")
            products = scraper.get_products(query)

            if not products:
                print("No products found or an error occurred.")
                continue

            html_content = scraper.generate_html(products, query)
            
            filename = "wildberries_results.html"
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"Results saved to {filename}")
            except IOError as e:
                print(f"Error saving results: {e}")

            time.sleep(1)  # Rate limiting
    except KeyboardInterrupt:
        print("\nProgram terminated by user. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()