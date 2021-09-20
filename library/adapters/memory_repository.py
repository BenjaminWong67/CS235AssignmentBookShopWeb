"""Name: Benjamin Wong UPI:BLU378 last-Modified:1:07pm 2/8/2021"""
import random

from pathlib import Path

from bisect import bisect, bisect_left, insort_left

from library.adapters.jsondatareader import BooksJSONReader
from library.adapters.repository import AbstractRepository
from library.domain.model import Book, User, BooksInventory, Author, Publisher, Review


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__books = list()
        self.__books_index = dict()
        self.__reviews = list()
        self.__users = list()
        self.__book_inventory = BooksInventory

    def add_book(self, book: Book):

        if isinstance(book, Book):
            if book.book_id not in self.__books_index.keys():
                insort_left(self.__books, book)
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

    def add_review(self, review: Review):
        super().add_review(review)
        self.__reviews.append(review)

    def get_reviews(self):
        return self.__reviews

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)
    
    def get_book_inventory(self):
        return self.__book_inventory



def random_book_price_and_stock_count():
    price = random.randint(3, 200)
    stock_count = random.randint(0, 20)

    return price, stock_count


# populates the memory repository with the provided json files
def populate(data_path: Path, repo: MemoryRepository):
    authors_data_path = str(Path(data_path) / "comic_books_excerpt.json")
    book_data_path = str(Path(data_path) / "book_authors_excerpt.json")

    books_data = BooksJSONReader(authors_data_path, book_data_path)
    books_data.read_json_files()

    book_inventory = repo.get_book_inventory()

    for book in books_data.dataset_of_books:
        price, stock_count = random_book_price_and_stock_count()
        book_inventory.add_book(book, price, stock_count)
        repo.add_book(book)
