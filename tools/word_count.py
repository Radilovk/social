import os
import re

CHAPTERS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'chapters')
GOAL_WORDS = 60000

WORD_RE = re.compile(r"\b[\w'-]+\b", flags=re.UNICODE)


def count_words_in_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return len(WORD_RE.findall(text))


def main():
    if not os.path.isdir(CHAPTERS_DIR):
        print(f'Папката {CHAPTERS_DIR} не съществува.')
        return

    total = 0
    for name in os.listdir(CHAPTERS_DIR):
        file_path = os.path.join(CHAPTERS_DIR, name)
        if os.path.isfile(file_path):
            total += count_words_in_file(file_path)

    progress = total / GOAL_WORDS * 100
    print(f'Общ брой думи: {total}')
    print(f'Прогрес спрямо целта от {GOAL_WORDS} думи: {progress:.2f}%')


if __name__ == '__main__':
    main()
