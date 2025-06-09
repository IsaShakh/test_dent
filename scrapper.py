import requests 
from bs4 import BeautifulSoup

def scrape_desc(url: str) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Ошибка загрузки страницы: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    domain = url.split("/")[2]

    if "dental-first.ru" in domain:
        desc = soup.find('div', class_='product-card__tabs-content order-1 active', itemprop='description')

    elif "stomatorg.ru" in domain:
        desc = soup.find("meta", itemprop="description")
        return desc["content"].strip() if desc else None

    elif "nika-dent.ru" in domain:
        desc = soup.select_one("div.short-descr p")

    elif "aveldent.ru" in domain:
        desc = soup.find("meta", itemprop="description")
        return desc["content"].strip() if desc else None

    elif "stomdevice.ru" in domain:
        desc = soup.select_one("div.ut2-gl__feature")

    elif "el-dent.ru" in domain:
        meta_desc = soup.find("meta", {"name": "description"})
        if meta_desc and meta_desc.get("content"):
            return meta_desc["content"].strip()

        desc = soup.select_one("div.product__body .product__desc")
    
    else:
        raise Exception("Неизвестный сайт")
    
    if not desc:
        raise Exception("Описание не найдено")
    
    return desc.get_text(strip=True)

