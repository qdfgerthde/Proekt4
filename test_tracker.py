import json
import os
import tempfile
import unittest
from unittest.mock import patch

# Перенаправляем BOOKS_FILE перед импортом main
import main as tracker


class TestBookTracker(unittest.TestCase):

    def setUp(self):
        """Создаём временный файл books.json для каждого теста."""
        self.tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        )
        self.tmp.write("[]")
        self.tmp.close()
        tracker.BOOKS_FILE = self.tmp.name

    def tearDown(self):
        os.unlink(self.tmp.name)

    # --- load_books / save_books ---

    def test_load_books_empty_file(self):
        books = tracker.load_books()
        self.assertEqual(books, [])

    def test_save_and_load_books(self):
        sample = [{"author": "Толстой", "title": "Война и мир", "rating": 5, "date": "01.01.2024"}]
        tracker.save_books(sample)
        loaded = tracker.load_books()
        self.assertEqual(loaded, sample)

    def test_load_books_missing_file(self):
        tracker.BOOKS_FILE = "nonexistent_file.json"
        books = tracker.load_books()
        self.assertEqual(books, [])

    # --- add_book ---

    def test_add_book_success(self):
        books = []
        inputs = ["Пушкин", "Евгений Онегин", "4", "12.05.2024"]
        with patch("builtins.input", side_effect=inputs):
            tracker.add_book(books)
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]["title"], "Евгений Онегин")
        self.assertEqual(books[0]["rating"], 4)

    def test_add_book_duplicate_rejected(self):
        books = [{"author": "Пушкин", "title": "Евгений Онегин", "rating": 4, "date": "01.01.2024"}]
        inputs = ["Пушкин", "Евгений Онегин"]
        with patch("builtins.input", side_effect=inputs):
            tracker.add_book(books)
        self.assertEqual(len(books), 1)  # дубликат не добавлен

    def test_add_book_invalid_rating_then_valid(self):
        books = []
        inputs = ["Чехов", "Палата №6", "0", "6", "abc", "3", "15.03.2023"]
        with patch("builtins.input", side_effect=inputs):
            tracker.add_book(books)
        self.assertEqual(books[0]["rating"], 3)

    def test_add_book_empty_author_rejected(self):
        books = []
        inputs = ["", "Какое-то название"]
        with patch("builtins.input", side_effect=inputs):
            tracker.add_book(books)
        self.assertEqual(len(books), 0)

    def test_add_book_default_date(self):
        books = []
        inputs = ["Булгаков", "Мастер и Маргарита", "5", ""]
        with patch("builtins.input", side_effect=inputs):
            tracker.add_book(books)
        from datetime import datetime
        today = datetime.today().strftime("%d.%m.%Y")
        self.assertEqual(books[0]["date"], today)

    # --- list_books ---

    def test_list_books_empty(self, capsys=None):
        books = []
        with patch("builtins.print") as mock_print:
            tracker.list_books(books)
            output = " ".join(str(c) for call in mock_print.call_args_list for c in call.args)
            self.assertIn("пуст", output)

    def test_list_books_shows_entries(self):
        books = [{"author": "Достоевский", "title": "Идиот", "rating": 5, "date": "10.10.2023"}]
        with patch("builtins.print") as mock_print:
            tracker.list_books(books)
            output = " ".join(str(c) for call in mock_print.call_args_list for c in call.args)
            self.assertIn("Достоевский", output)
            self.assertIn("Идиот", output)

    # --- average_rating ---

    def test_average_rating_correct(self):
        books = [
            {"author": "А", "title": "Книга 1", "rating": 4, "date": "01.01.2024"},
            {"author": "Б", "title": "Книга 2", "rating": 2, "date": "01.01.2024"},
        ]
        with patch("builtins.print") as mock_print:
            tracker.average_rating(books)
            output = " ".join(str(c) for call in mock_print.call_args_list for c in call.args)
            self.assertIn("3.00", output)

    def test_average_rating_empty(self):
        with patch("builtins.print") as mock_print:
            tracker.average_rating([])
            output = " ".join(str(c) for call in mock_print.call_args_list for c in call.args)
            self.assertIn("Нет книг", output)

    # --- author_stats ---

    def test_author_stats_counts(self):
        books = [
            {"author": "Толстой", "title": "Война и мир", "rating": 5, "date": "01.01.2024"},
            {"author": "Толстой", "title": "Анна Каренина", "rating": 4, "date": "02.01.2024"},
            {"author": "Чехов", "title": "Вишнёвый сад", "rating": 3, "date": "03.01.2024"},
        ]
        with patch("builtins.print") as mock_print:
            tracker.author_stats(books)
            output = " ".join(str(c) for call in mock_print.call_args_list for c in call.args)
            self.assertIn("Толстой", output)
            self.assertIn("2", output)

    # --- delete_book ---

    def test_delete_book_valid(self):
        books = [{"author": "Гоголь", "title": "Ревизор", "rating": 4, "date": "01.01.2024"}]
        with patch("builtins.input", return_value="1"):
            tracker.delete_book(books)
        self.assertEqual(len(books), 0)

    def test_delete_book_invalid_index(self):
        books = [{"author": "Гоголь", "title": "Ревизор", "rating": 4, "date": "01.01.2024"}]
        with patch("builtins.input", return_value="99"):
            tracker.delete_book(books)
        self.assertEqual(len(books), 1)

    def test_delete_book_empty_list(self):
        books = []
        with patch("builtins.print") as mock_print:
            tracker.delete_book(books)
            output = " ".join(str(c) for call in mock_print.call_args_list for c in call.args)
            self.assertIn("пуст", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
