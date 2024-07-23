import requests
from parsel import Selector
import pandas as pd
import pathlib

def scrape_quotes(page_number):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 AVG/122.0.0.0'}
    url = f'https://quotes.toscrape.com/page/{page_number}/'
    print('Fetching URL:', url)

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page {page_number}. Status code: {response.status_code}")
        return []

    selector = Selector(response.text)
    cards = selector.css('div[class="quote"]')

    results = []
    for card in cards:
        data = {
            'ResponseURL': response.url,
            'Quote': card.css('.text::text').get(),
            'Author': card.css('small[class="author"]::text').get(),
            'Tags': ', '.join(card.css('div[class="tags"] a[class="tag"]::text').getall())
        }
        results.append(data)
    return results

def main():
    final_data = []
    for page in range(1, 11):  # Scraping first 10 pages
        page_data = scrape_quotes(page)
        final_data.extend(page_data)

    csv_name = 'quotes.csv'
    df = pd.DataFrame(final_data)
    csvfile = pathlib.Path(f'{csv_name}.csv')
    df.to_csv(csvfile, mode='a', index=False, header=not csvfile.exists())
    print(f"Data saved to {csv_name}")

if __name__ == "__main__":
    main()
