import json
import os
from datetime import datetime

BOOKS_FILE = "books.json"


def load_books():
    """Загрузка данных из books.json."""
    if not os.path.exists(BOOKS_FILE):
        return []
    with open(BOOKS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_books(books):
    """Сохранение данных в books.json."""
    with open(BOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)


def add_book(books):
    """Добавление новой книги."""
    print("\n--- Добавить книгу ---")
    author = input("Автор: ").strip()
    title = input("Название: ").strip()

    if not author or not title:
        print("Ошибка: автор и название не могут быть пустыми.")
        return

    # Проверка на дубликаты (Closes #1)
    for book in books:
        if book["author"].lower() == author.lower() and book["title"].lower() == title.lower():
            print(f"Книга «{title}» автора {author} уже есть в трекере.")
            return

    while True:
        try:
            rating = int(input("Оценка (1–5): "))
            if 1 <= rating <= 5:
                break
            print("Оценка должна быть от 1 до 5.")
        except ValueError:
            print("Введите целое число от 1 до 5.")

    date_input = input("Дата прочтения (дд.мм.гггг, Enter — сегодня): ").strip()
    if not date_input:
        date = datetime.today().strftime("%d.%m.%Y")
    else:
        try:
            datetime.strptime(date_input, "%d.%m.%Y")
            date = date_input
        except ValueError:
            print("Неверный формат даты. Используется сегодняшняя дата.")
            date = datetime.today().strftime("%d.%m.%Y")

    books.append({"author": author, "title": title, "rating": rating, "date": date})
    save_books(books)
    print(f"✓ Книга «{title}» добавлена.")


def list_books(books):
    """Вывод всех книг."""
    print("\n--- Все книги ---")
    if not books:
        print("Список пуст.")
        return
    for i, book in enumerate(books, 1):
        stars = "★" * book["rating"] + "☆" * (5 - book["rating"])
        print(f"{i}. {book['author']} — «{book['title']}» [{stars}] ({book['date']})")


def average_rating(books):
    """Средняя оценка по всем книгам."""
    print("\n--- Средняя оценка ---")
    if not books:
        print("Нет книг для подсчёта.")
        return
    avg = sum(b["rating"] for b in books) / len(books)
    print(f"Средняя оценка: {avg:.2f} из 5 (всего книг: {len(books)})")


def author_stats(books):
    """Статистика по авторам."""
    print("\n--- Статистика по авторам ---")
    if not books:
        print("Нет данных.")
        return
    stats = {}
    for book in books:
        author = book["author"]
        if author not in stats:
            stats[author] = {"count": 0, "total_rating": 0}
        stats[author]["count"] += 1
        stats[author]["total_rating"] += book["rating"]

    sorted_authors = sorted(stats.items(), key=lambda x: x[1]["count"], reverse=True)
    for author, data in sorted_authors:
        avg = data["total_rating"] / data["count"]
        print(f"  {author}: {data['count']} кн., средняя оценка {avg:.1f}")


def delete_book(books):
    """Удаление книги по номеру."""
    print("\n--- Удалить книгу ---")
    if not books:
        print("Список пуст.")
        return
    list_books(books)
    try:
        num = int(input("\nНомер книги для удаления: "))
        if 1 <= num <= len(books):
            removed = books.pop(num - 1)
            save_books(books)
            print(f"✓ Книга «{removed['title']}» удалена.")
        else:
            print("Неверный номер.")
    except ValueError:
        print("Введите число.")


def show_menu():
    print("\n" + "=" * 35)
    print("   📚 Трекер прочитанных книг")
    print("=" * 35)
    print("  1. Добавить книгу")
    print("  2. Показать все книги")
    print("  3. Показать среднюю оценку")
    print("  4. Статистика по авторам")
    print("  5. Удалить книгу")
    print("  6. Выход")
    print("=" * 35)


def main():
    books = load_books()
    while True:
        show_menu()
        choice = input("Выберите пункт: ").strip()
        if choice == "1":
            add_book(books)
        elif choice == "2":
            list_books(books)
        elif choice == "3":
            average_rating(books)
        elif choice == "4":
            author_stats(books)
        elif choice == "5":
            delete_book(books)
        elif choice == "6":
            print("До свидания! 👋")
            break
        else:
            print("Неверный выбор. Введите число от 1 до 6.")


if __name__ == "__main__":
    main()
