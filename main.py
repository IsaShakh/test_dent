from bs4 import BeautifulSoup

from desc_generator import new_desc
from to_google import upload_to_google_sheets
from meta_info import extract_info
from scrapper import scrape_desc
from to_html import format_to_html_from_text


urls = [
    "https://el-dent.ru/id/all-bond3-adgeziv-bisko.html",
    "https://el-dent.ru/id/adper-single-bond2-odnokomponentnaya-adgezivnaya-sistema-6ml-3m.html",
    "https://el-dent.ru/id/adper-single-bond2-odnokomponentnaya-adgezivnaya-sistema-6ml-3m.html",
    "https://el-dent.ru/id/filtek-z550-filtek-nabor-7050-IK-3m.html",
]

def process_url(url: str) -> dict:
    try:
        raw_html = scrape_desc(url)
        raw_text = BeautifulSoup(raw_html, 'html.parser').get_text()
        generated_text = new_desc(raw_text)
        formatted_html = format_to_html_from_text(generated_text)
        meta = extract_info(generated_text)

        return {
            'url': url,
            'html': formatted_html,
            'title': meta['title'],
            'description': meta['description'],
            'keywords': meta['keywords'],
        }

    except Exception as e:
        print(f"[erroe] {url}: {e}")
        return None

all_results = []
for url in urls:
    result = process_url(url)
    if result:
        all_results.append(result)

upload_to_google_sheets(
    data_list=all_results,
    creds_path="D:/google_cred.json",
    spreadsheet_name="test" 
)  
