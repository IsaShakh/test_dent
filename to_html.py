import re

def clean_text(text):
    replacements = [
        (r'[–—]', '-'),
        (r'[‘’“”]', '"'),
        (r'[®©™]', ''),
        (r'\bм²\b|\bсм³\b|\bмм²\b', ''),
        (r'°C', 'C'),
        (r'°', ' градус'),
        (r'\bx\b', '*'),
        (r'#', 'около'),
        (r'≤', 'меньше или равно'),
        (r'≥', 'больше или равно'),
        (r'\s+', ' '),
        (r'&nbsp;', ' ')
    ]
    for pattern, repl in replacements:
        text = re.sub(pattern, repl, text)
    return text.strip()

def format_to_html_from_text(text: str) -> str:
    lines = text.strip().splitlines()
    html = []
    buffer = []
    mode = 'paragraph'

    def flush_paragraph_block(paragraph_lines):
        if paragraph_lines:
            paragraph = ' '.join(paragraph_lines).strip()
            if paragraph:
                paragraph = clean_text(paragraph)
                html.append(f'<p style="text-align: justify; font-size: 13px;">{paragraph}</p>')

    def flush_list_block(list_items):
        if list_items:
            html.append('<ul style="text-align: justify; font-size: 13px; list-style-type: disc;">')
            for item in list_items:
                item = clean_text(item.strip('-•—– ').strip())
                html.append(f'<li>{item}</li>')
            html.append('</ul>')

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.endswith(':'):
            flush_paragraph_block(buffer)
            flush_list_block(buffer)
            buffer = []
            heading = clean_text(line.rstrip(':'))
            html.append(f'<h3 style="text-align: justify; font-size: 13px;">{heading}</h3>')
            mode = 'paragraph'
        elif re.match(r'^[-•—–]', line):
            if mode != 'list':
                flush_paragraph_block(buffer)
                buffer = []
                mode = 'list'
            buffer.append(line)
        else:
            if mode != 'paragraph':
                flush_list_block(buffer)
                buffer = []
                mode = 'paragraph'
            buffer.append(line)

    if mode == 'list':
        flush_list_block(buffer)
    else:
        flush_paragraph_block(buffer)

    return '\n'.join(html)


