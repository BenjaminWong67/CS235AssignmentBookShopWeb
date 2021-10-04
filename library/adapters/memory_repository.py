from bisect import bisect, bisect_left, insort_left

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
