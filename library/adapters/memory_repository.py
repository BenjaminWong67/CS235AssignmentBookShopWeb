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
    
    def get_number_of_books(self):
        return len(self.__books)

    def get_books_by_id(self, id_list):
        # Strip out any ids in id_list that don't represent Article ids in the repository.
        existing_ids = [id for id in id_list if id in self.__books_index]

        # Fetch the Articles.
        books = [self.__books_index[id] for id in existing_ids]
        return books

    def add_book_to_inventory(self, book : Book, price, nr_books_in_stock):
        self.__book_inventory.add_book(book, price, nr_books_in_stock)
    
    def remove_book_from_inventory(self, book_id):
        self.__book_inventory.remove_book(book_id)
    
    def find_book(self, book_id):
        return self.__book_inventory.find_book(book_id)
    
    def find_price(self, book_id):
        return self.__book_inventory.find_price(book_id)

    def find_stock_count(self, book_id):
        return self.__book_inventory.find_stock_count(book_id)
    
    def adjust_stock_count(self, book_id, amount_to_deduct):
        self.__book_inventory.adjust_stock_count(book_id, amount_to_deduct)
    
    def search_book_by_title(self, book_title):
        return self.__book_inventory.search_book_by_title(book_title)
    
    def discount_book(self, book_id, discount):
        self.__book_inventory.discount_book(book_id, discount)
    
    def get_book_discount(self, book_id):
        return self.__book_inventory.get_book_discount(book_id)
    
    # below are the shopping cart methods
    def add_book_to_user_shoppingcart(self, user_name, book: Book):
        user = self.get_user(user_name)
        user.add_book_to_cart(book)

    def remove_book_from_user_shoppingcart(self, user_name, book: Book):
        user = self.get_user(user_name)
        user.remove_book_from_cart(book)

    def purchase_books_in_user_shoppingcart(self, user_name):
        user = self.get_user(user_name)
        user.purchase_books_in_cart()
    
    def add_author(self, author_object):
        pass

    def add_publisher(self, publisher):
        pass

    def get_shopping_cart(self, user_name):
        user = self.get_user(user_name)
        return user.shoppingcart

    def get_purchased_books(self, user_name):
        user = self.get_user(user_name)
        return user.purchased_books
