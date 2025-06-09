from to_google import upload_to_google_sheets

test_data = [
    {
        "my_url": "https://dental-first.ru/catalog/variolink-esthetic/",
        "competitor_url": "https://el-dent.ru/shop/UID_7263.html",
        "title": "Variolink Esthetic LC",
        "description": "Универсальный цемент для фиксации виниров.",
        "keywords": "цемент, фиксация, виниры",
        "html": "<p>Описание товара в HTML</p>"
    }
]

upload_to_google_sheets(
    data_list=test_data,
    creds_path="D:\google_cred.json",
    spreadsheet_name="desc_autogen"
)
