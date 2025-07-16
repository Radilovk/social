import json
import sys
import os

INPUT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bookData.json')
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'book.txt')

ROMAN_MAP = [
    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
    (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
    (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
]

def to_roman(num):
    result = ''
    for val, sym in ROMAN_MAP:
        while num >= val:
            result += sym
            num -= val
    return result


def main():
    with open(INPUT_FILE, encoding='utf-8') as f:
        data = json.load(f)

    lines = []
    current_page = None

    for part in data.get('parts', []):
        lines.append('')
        lines.append(f'ЧАСТ {to_roman(part.get("partNumber", 0))} · {part.get("partTitle", "")}')
        chapter_num = 0
        for chapter in part.get('chapters', []):
            chapter_num += 1
            if chapter.get('pageNumber') != current_page:
                current_page = chapter['pageNumber']
                lines.append('')
                lines.append(f'Страница {current_page}')
            lines.append('')
            lines.append(f'Глава {chapter_num}. {chapter.get("chapterTitle", "")}')
            if 'epigraph' in chapter:
                epi = chapter['epigraph']
                if epi.get('pageNumber') != current_page:
                    current_page = epi['pageNumber']
                    lines.append('')
                    lines.append(f'Страница {current_page}')
                lines.append('')
                lines.append(f'„{epi.get("text", "")}“')
                lines.append(f'– {epi.get("source", "")}')
            for block in chapter.get('contentBlocks', []):
                if block.get('pageNumber') != current_page:
                    current_page = block['pageNumber']
                    lines.append('')
                    lines.append(f'Страница {current_page}')
                lines.append('')
                lines.append(block.get('content', ''))
    content = '\n'.join(lines).strip() + '\n'
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Записан файл: {OUTPUT_FILE}')

if __name__ == '__main__':
    main()
