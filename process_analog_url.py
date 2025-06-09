from bs4 import BeautifulSoup
from desc_generator import new_desc
from to_html import format_to_html_from_text
from meta_info import extract_info
from scrapper import scrape_desc 

def process_competitor_url(competitor_url: str, my_url: str) -> dict | None:
    try:
        print(f"Обрабатываем: {competitor_url}")

        raw_html = scrape_desc(competitor_url)
        raw_text = BeautifulSoup(raw_html, 'html.parser').get_text()

        generated_text = new_desc(raw_text)
        formatted_html = format_to_html_from_text(generated_text)
        meta = extract_info(generated_text)

        return {
            "my_url": my_url,
            "competitor_url": competitor_url,
            "title": meta["title"],
            "description": meta["description"],
            "keywords": meta["keywords"],
            "html": formatted_html,
        }

    except Exception as e:
        print(f"[Ошибка обработки] {competitor_url}: {e}")
        return None
