import requests 
from bs4 import BeautifulSoup

def scrape_desc(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"error, status code {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')

    desc_block = soup.find('div', class_='product-card__tabs-content order-1 active', itemprop='description')
    if not desc_block:
        raise Exception('no description has been found')
    
    return str(desc_block)