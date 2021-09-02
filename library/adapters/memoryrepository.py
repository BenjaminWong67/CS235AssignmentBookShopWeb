"""Name: Benjamin Wong UPI:BLU378 last-Modified:1:07pm 2/8/2021"""
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
        self.__books_index[book.title] = book

    def get_book(self, book_title: str) -> Book:
        book = None

        try:
            book = self.__books_index[book_title]
        except KeyError:
            pass

        return book

    def add_users(self, user: User):
        pass

    def get_user(self, username: str) -> User:
        pass

    def add_review(self, review: Review):
        pass

    def get_review(self, username: str, book_id: int):
        pass


def populate(authors_file_name: str, books_file_name: str, repo: MemoryRepository):
    data_set_of_books = BooksJSONReader(authors_file_name, books_file_name)
    data_set_of_books.read_json_files()
    for book in data_set_of_books.dataset_of_books:
        repo.add_book(book)
