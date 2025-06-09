from load_categories import load_categories_from_file
from category_parser import get_products_from_category
from competitor_search import get_product_title, search_on_all_competitors
from process_analog_url import process_competitor_url
from to_google import upload_to_google_sheets
from meta_info import extract_info
import re

not_found = []


def generate_search_query(title: str) -> str:
    cleaned = re.sub(r"[^\w\s-]", "", title)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    words = cleaned.split()

    stop_words = {"refill", "kit", "xl", "ho", "ml", "g", "шт", "г", "n", "try", "in"}
    keywords = [w for w in words if len(w) > 2 and w.lower() not in stop_words]

    if not keywords:
        keywords = words[:2]

    return " ".join(keywords[:3])

competitor_sites = [
    "el-dent.ru",
    "stomatorg.ru",
    "nika-dent.ru",
    "aveldent.ru",
    "stomdevice.ru"
]

category_urls = load_categories_from_file("categories.txt")
all_results = []

for category_url in category_urls:
    print(f"\nОбрабатываем категорию: {category_url}")
    product_urls = get_products_from_category(category_url)
    print(f"Найдено товаров: {len(product_urls)}")

    for my_url in product_urls:
        print(f"\n🔹 Товар: {my_url}")
        title = get_product_title(my_url)
        print(f"Название: {title}")
        if not title:
            print("Название не найдено, пропускаем.")
            continue

        search_query = generate_search_query(title)
        print(f"Поисковый запрос: {search_query}")

        competitor_url = search_on_all_competitors(search_query, competitor_sites)
        if not competitor_url:
            print("   Аналог не найден")
            not_found.append(my_url)

            continue

        result = process_competitor_url(competitor_url, my_url)
        if result:
            print("Описание сгенерировано")
            try:
                upload_to_google_sheets(
                    data_list=[result], 
                    creds_path="D:\google_cred.json",
                    spreadsheet_name="desc_autogen"
                )
                print("   📥 Добавлено в Google Таблицу")
            except Exception as e:
                print(f"Ошибка при добавлении в Google Таблицу: {e}")
            import time
            time.sleep(1.2)
        else:
            print("Ошибка при генерации описания")
        
        
if not_found:
    with open("not_found.txt", "w", encoding="utf-8") as f:
        f.write("Ссылки на товары, для которых не найден аналог:\n\n")
        for url in not_found:
            f.write(url + "\n")
    print(f"\nСохранено {len(not_found)} ненайденных товаров в not_found.txt")
else:
    print("\nВсе товары успешно обработаны и найдены")
