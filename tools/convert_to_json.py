import json
import os
import re

BOOK_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'book.txt')
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bookData.json')

PART_RE = re.compile(r'^ЧАСТ\s+([IVXLC]+)\s*·\s*(.+)$')
CHAPTER_RE = re.compile(r'^Глава\s+(\d+)\.\s*(.+)$')

# Приблизителен брой знаци на печатна страница
CHARS_PER_PAGE = 1800

def parse_book(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip() for line in f]

    parts = []
    part = None
    chapter = None
    part_counter = 0
    last_chapter_num = 0
    char_count = 0  # акумулиран брой символи за изчисляване на страници

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        part_match = PART_RE.match(line)
        if part_match:
            part_counter += 1
            part_title = part_match.group(2).strip()
            part = {
                "partNumber": part_counter,
                "partTitle": part_title,
                "chapters": []
            }
            parts.append(part)
            i += 1
            continue

        chapter_match = CHAPTER_RE.match(line)
        if chapter_match:
            chapter_id = int(chapter_match.group(1))
            last_chapter_num = chapter_id
            chapter_title = chapter_match.group(2).strip()
            epigraph = None
            char_count += len(lines[i]) + 1
            # прескачаме празни редове след заглавието на главата
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j + 1 < len(lines):
                quote_line = lines[j].strip()
                source_line = lines[j + 1].strip()
                if quote_line.startswith('„') and source_line.startswith('–'):
                    epigraph = {
                        "text": quote_line.strip('„“'),
                        "source": source_line.lstrip('– ').strip(),
                        "pageNumber": char_count // CHARS_PER_PAGE + 1
                    }
                    j += 2
            if epigraph:
                char_count += len(quote_line) + len(source_line) + 2
                i = j
            chapter = {
                "chapterId": f"ch{chapter_id:02d}",
                "chapterTitle": chapter_title,
                "pageNumber": char_count // CHARS_PER_PAGE + 1,
                "contentBlocks": []
            }
            if epigraph:
                chapter["epigraph"] = epigraph
            if part is None:
                part = {
                    "partNumber": part_counter + 1,
                    "partTitle": "",
                    "chapters": []
                }
                parts.append(part)
            part["chapters"].append(chapter)
            i += 1
            continue

        # Специални секции след последната глава
        if line == "Заключение" or line == "Приложения":
            last_chapter_num += 1
            chapter_title = line
            char_count += len(line) + 1
            chapter = {
                "chapterId": f"ch{last_chapter_num:02d}",
                "chapterTitle": chapter_title,
                "pageNumber": char_count // CHARS_PER_PAGE + 1,
                "contentBlocks": []
            }
            if part is None:
                part = {
                    "partNumber": part_counter + 1,
                    "partTitle": "",
                    "chapters": []
                }
                parts.append(part)
            part["chapters"].append(chapter)
            i += 1
            continue

        def apply_formatting(text):
            """Превръща маркировките за _курсив_ и __удебелен__ в
            Markdown-стил със звездички."""
            text = re.sub(r'__([^_]+)__', r'**\1**', text)
            text = re.sub(r'_([^_]+)_', r'*\1*', text)
            return text

        line = apply_formatting(line)

        # heading detection
        if len(line.split()) <= 10 and not line.endswith(('.', '!', '?', '"', '”')):
            char_count += len(line) + 1
            chapter["contentBlocks"].append({
                "type": "heading",
                "level": 3,
                "content": line,
                "pageNumber": char_count // CHARS_PER_PAGE + 1
            })
        else:
            char_count += len(line) + 1
            chapter["contentBlocks"].append({
                "type": "paragraph",
                "content": line,
                "pageNumber": char_count // CHARS_PER_PAGE + 1
            })
        i += 1

    return {
        "bookMeta": {"title": "Профилът не лъже", "author": "Вашият екип"},
        "parts": parts
    }

def main():
    data = parse_book(BOOK_FILE)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Генериран файл: {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
