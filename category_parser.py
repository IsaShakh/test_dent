import requests
from bs4 import BeautifulSoup

BASE_URL = "https://dental-first.ru"

def get_products_from_category(category_url: str) -> list:
    headers = {'User-Agent': 'Mozilla/5.0'}
    product_links = []
    page = 1
    seen_pages = set()

    while True:
        paginated_url = f"{category_url}?PAGEN_1={page}"
        print(f"Загружаем страницу {page}: {paginated_url}")
        response = requests.get(paginated_url, headers=headers)

        if response.status_code != 200:
            print(f"Ошибка: статус {response.status_code}")
            break

        if paginated_url in seen_pages:
            print(f"Повтор страницы: {paginated_url}, прекращаем")
            break

        seen_pages.add(paginated_url)

        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.select("a.di_b.c_b")

        if not cards:
            print("Нет карточек на странице, выходим")
            break

        for card in cards:
            href = card.get("href")
            if href and "/catalog/" in href:
                full_url = "https://dental-first.ru" + href
                product_links.append(full_url)

        page += 1

        if page > 20:
            print("Превышен лимит страниц (20)")
            break

    print(f"Найдено товаров: {len(product_links)}\n")
    return list(set(product_links))


