import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, 'chapters')
WORD_GOAL = 60000

def count_words(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    return len(text.split())

def main():
    total = 0
    for name in os.listdir(CHAPTERS_DIR):
        if name.endswith('.txt'):
            total += count_words(os.path.join(CHAPTERS_DIR, name))
    progress = total / WORD_GOAL * 100
    print(f'Общ брой думи: {total}')
    print(f'Прогрес: {progress:.2f}% от {WORD_GOAL}')

if __name__ == '__main__':
    main()
