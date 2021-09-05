"""Name: Benjamin Wong UPI:BLU378 last-Modified:1:07pm 2/8/2021"""
from pathlib import Path
from typing import Type

from library.adapters.jsondatareader import BooksJSONReader
from library.adapters.repository import AbstractRepository
from library.domain.model import Book, User, BooksInventory, Author, Publisher, Review


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__books = list()
        self.__books_index = dict()
        self.__reviews = list()
        self.__users = list()

    def add_book(self, book: Book):
        self.__books.append(book)
        self.__books_index[book.book_id] = book

    def get_book(self, book_title: str) -> Book:
        book = None

        try:
            book = self.__books_index[book_title]
        except KeyError:
            pass

        return book

    def get_book_catalogue(self):
        return self.__books

    def add_users(self, user: User):
        pass

    def get_user(self, username: str) -> User:
        pass

    def add_review(self, review: Review):
        pass

    def get_review(self, username: str, book_id: int):
        pass

    def get_publisher(self, publisher_id: int) -> Publisher:
        pass

    def get_author(self, author_id: int) -> Author:
        pass


def populate(data_path: Path, repo: MemoryRepository):
    authors_data_path = str(Path(data_path) / "comic_books_excerpt.json")
    book_data_path = str(Path(data_path) / "book_authors_excerpt.json")
    data_set_of_books = BooksJSONReader(authors_data_path, book_data_path)
    data_set_of_books.read_json_files()
    for book in data_set_of_books.dataset_of_books:
        repo.add_book(book)

