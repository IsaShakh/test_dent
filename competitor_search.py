import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_product_title(url: str) -> str | None:
    try:
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, 'html.parser')
        title_tag = soup.find('h1')
        return title_tag.get_text(strip=True) if title_tag else None
    except Exception as e:
        print(f"[Ошибка get_product_title] {url}: {e}")
        return None


def search_on_site(title: str, site_url: str) -> str | None:
    query = title.replace(' ', '+')
    search_url = f"https://{site_url}/search/?words={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        resp = requests.get(search_url, headers=headers)
        if resp.status_code != 200:
            print(f"Ошибка загрузки {search_url}: {resp.status_code}")
            return None

        soup = BeautifulSoup(resp.text, 'html.parser')

        link = soup.select_one('a.product__caption')
        if link and link.get('href'):
            href = link['href']
            if not href.startswith('http'):
                href = f"https://{site_url}{href}"
            return href

        return None

    except Exception as e:
        print(f"[Ошибка поиска на сайте {site_url}]: {e}")
        return None



def search_on_all_competitors(title: str, competitor_sites: list[str]) -> str | None:
    for site in competitor_sites:
        print(f"Ищем на {site}...")
        result = search_on_site(title, site)
        if result:
            print(f"Найдено: {result}")
            return result
    print("Аналог не найден ни на одном сайте")
    return None
