import requests
import os
from dotenv import load_dotenv

load_dotenv()



IAM_TOKEN = os.getenv("YANDEX_IAM_TOKEN") 
FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")

def new_desc(text: str) -> str:
    prompt = f"""
Представь, что ты профессиональный контент-редактор в области стоматологических товаров. Я предоставлю тебе описание товара с магазина-конкурента.
Сгенерируй новое уникальное описание, соответствующее стилю магазина Dental First:
- Язык: экспертный, структурированный, понятный стоматологам.
- Стиль: чёткий, без воды.
- Раздели текст на смысловые блоки: Название и слоган через дефис, Описание, Показания к применению, Предупреждения, Хранение, Состав, Характеристики, Преимущества (если это уместно).
- Избегай копирования текста, пиши своими словами.
- Не упоминай название магазина конкурента.
- Пиши исключительно на русском языке.
Вот тебе ссылка товара с Dental First для понимания стиля https://dental-first.ru/catalog/boston-glaze-glazur-dlya-kompozitov/ .
Вот сам текст:
{text}
"""

    headers = {
        "Authorization": f"Bearer {IAM_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": 700
        },
        "messages": [
            {"role": "system", "text": "Ты профессиональный копирайтер для стоматологической продукции."},
            {"role": "user", "text": prompt}
        ]
    }

    response = requests.post(
        "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
        headers=headers,
        json=data
    )

    if response.status_code != 200:
        raise Exception(f"YandexGPT error: {response.status_code} - {response.text}")

    return response.json()['result']['alternatives'][0]['message']['text'].strip()
