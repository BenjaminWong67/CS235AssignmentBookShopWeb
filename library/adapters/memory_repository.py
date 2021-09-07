"""Name: Benjamin Wong UPI:BLU378 last-Modified:1:07pm 2/8/2021"""
from pathlib import Path

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
        if isinstance(book, Book):
            self.__books.append(book)
            self.__books_index[book.book_id] = book
        else:
            raise ValueError

    def get_book(self, book_id: int) -> Book:
        book = None

        try:
            book = self.__books_index[book_id]
        except KeyError:
            pass

        return book

    def get_book_catalogue(self):
        return self.__books


# populates the memory repository with the provided json files
def populate(data_path: Path, repo: MemoryRepository):
    authors_data_path = str(Path(data_path) / "comic_books_excerpt.json")
    book_data_path = str(Path(data_path) / "book_authors_excerpt.json")

    data_set_of_books = BooksJSONReader(authors_data_path, book_data_path)
    data_set_of_books.read_json_files()
    for book in data_set_of_books.dataset_of_books:
        repo.add_book(book)
