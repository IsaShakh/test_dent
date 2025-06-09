import re
from multi_rake import Rake

def extract_info(text):
    clean_text = re.sub(r'<[^>]+>', '', text).strip()
    lines = [line.strip() for line in clean_text.splitlines() if line.strip()]

    title = ''
    description_lines = []
    found_title = False
    found_description = False

    for i, line in enumerate(lines):
        if not found_title and re.search(r'\*\*.*?—.*?\*\*', line):
            title = re.sub(r'\*\*', '', line)
            found_title = True
            continue

        if found_title and not found_description:
            if re.search(r'\*\*.*?:\*\*', line): 
                continue
            if re.match(r'^(Назначение|Инструкция|Состав|Характеристики|Преимущества|Хранение|Применение)', line, re.IGNORECASE):
                break
            description_lines.append(line)

    description = ' '.join(description_lines).strip()

    if description.lower() in {"", "описание", "описание:"}:
        description = title


    rake = Rake(language_code="ru")
    keywords = [phrase for phrase, _ in rake.apply(clean_text)[:5]]

    return {
        'title': title,
        'description': description,
        'keywords': ', '.join(keywords)
    }
