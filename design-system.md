# Дизайн система

## Цветова палитра
- Основен акцент: `#007AFF`
- Светъл фон: `#FFFFFF`
- Тъмен фон: `#121212`
- Сепия фон: `#fbf0d9`

## Шрифтове
- Основен сериф: **Lora**
- Основен безсериф: **Inter**

## Компоненти
- Навигационен панел (`nav.nav-panel`)
- Панел с настройки (`aside.settings-panel`)
- Карти в таблото (`.dashboard-card`)

Този файл описва базовите цветове и типография, които да се използват в проекта.

## Илюстрации и инфографики
- Използвайте опростени векторни изображения.
- Единен визуален стил с палитрата отгоре.
- Съхранявайте файловете в папка `assets/`.

## Заглавия и акценти
Примерни CSS класове за заглавия, подзаглавия и подсветка:

```css
.title-main {
    font-family: var(--font-sans);
    font-size: 2.4rem;
    color: var(--accent-color);
    margin-bottom: 1rem;
}
.subtitle {
    font-family: var(--font-sans);
    font-size: 1.6rem;
    color: var(--text-color);
    margin-bottom: 0.5rem;
}
.text-highlight {
    background-color: var(--highlight-color);
}
```
