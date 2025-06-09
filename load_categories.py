def load_categories_from_file(filepath: str) -> list:
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip()]
