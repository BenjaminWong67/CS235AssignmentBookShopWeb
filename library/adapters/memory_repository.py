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
        self.__book_inventory = BooksInventory()

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
        review.user.add_review(review)

    def get_reviews(self):
        return self.__reviews

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)
    
    def get_book_inventory(self):
        return self.__book_inventory
    
    def get_number_of_books(self):
        return len(self.__books)

    def get_books_by_id(self, id_list):
        # Strip out any ids in id_list that don't represent Article ids in the repository.
        existing_ids = [id for id in id_list if id in self.__books_index]

        # Fetch the Articles.
        books = [self.__books_index[id] for id in existing_ids]
        return books


def three_random_book_discount(repo: MemoryRepository):
    book_count = repo.get_number_of_books()
    book_catalogue = repo.get_book_catalogue()
    book_inv = repo.get_book_inventory()
    quantity = 3

    if quantity >= book_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of books.
        quantity = book_count - 1
    
    random_books = random.sample(book_catalogue, quantity)

    for book in random_books:
        book_inv.discount_book(book.book_id, 50)

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
    
    three_random_book_discount(repo)
