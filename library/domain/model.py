from datetime import datetime
from typing import List


class Publisher:

    def __init__(self, publisher_name: str):
        # This makes sure the setter is called here in the initializer/constructor as well.
        self.name = publisher_name

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, publisher_name: str):
        self.__name = "N/A"
        if isinstance(publisher_name, str):
            # Make sure leading and trailing whitespace is removed.
            publisher_name = publisher_name.strip()
            if publisher_name != "":
                self.__name = publisher_name

    def __repr__(self):
        return f'<Publisher {self.name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.name == self.name

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)


class Author:

    def __init__(self, author_id: int, author_full_name: str):
        if not isinstance(author_id, int):
            raise ValueError

        if author_id < 0:
            raise ValueError

        self.__unique_id = author_id

        # Uses the attribute setter method.
        self.full_name = author_full_name

        # Initialize author colleagues data structure with empty set.
        # We use a set so each unique author is only represented once.
        self.__authors_this_one_has_worked_with = set()

    @property
    def unique_id(self) -> int:
        return self.__unique_id

    @property
    def full_name(self) -> str:
        return self.__full_name

    @full_name.setter
    def full_name(self, author_full_name: str):
        if isinstance(author_full_name, str):
            # make sure leading and trailing whitespace is removed
            author_full_name = author_full_name.strip()
            if author_full_name != "":
                self.__full_name = author_full_name
            else:
                raise ValueError
        else:
            raise ValueError

    def add_coauthor(self, coauthor: "Author"):
        if isinstance(coauthor, self.__class__) and coauthor.unique_id != self.unique_id:
            self.__authors_this_one_has_worked_with.add(coauthor)

    def check_if_this_author_coauthored_with(self, author):
        return author in self.__authors_this_one_has_worked_with

    def __repr__(self):
        return f'<Author {self.full_name}, author id = {self.unique_id}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.unique_id == other.unique_id

    def __lt__(self, other):
        return self.unique_id < other.unique_id

    def __hash__(self):
        return hash(self.unique_id)


class Book:

    def __init__(self, book_id: int, book_title: str):
        if not isinstance(book_id, int):
            raise ValueError

        if book_id < 0:
            raise ValueError

        self.__book_id = book_id

        # use the attribute setter
        self.title = book_title

        self.__description = None
        self.__publisher = None
        self.__authors = []
        self.__release_year = None
        self.__ebook = None
        self.__num_pages = None
        self.__reviews = []

    @property
    def book_id(self) -> int:
        return self.__book_id

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, book_title: str):
        if isinstance(book_title, str):
            book_title = book_title.strip()
            if book_title != "":
                self.__title = book_title
            else:
                raise ValueError
        else:
            raise ValueError

    @property
    def release_year(self) -> int:
        return self.__release_year

    @release_year.setter
    def release_year(self, release_year: int):
        if isinstance(release_year, int) and release_year >= 0:
            self.__release_year = release_year
        else:
            raise ValueError

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        if isinstance(description, str):
            self.__description = description.strip()

    @property
    def publisher(self) -> Publisher:
        return self.__publisher

    @publisher.setter
    def publisher(self, publisher: Publisher):
        if isinstance(publisher, Publisher):
            self.__publisher = publisher
        else:
            self.__publisher = None

    @property
    def authors(self) -> List[Author]:
        return self.__authors

    def add_author(self, author: Author):
        if not isinstance(author, Author):
            return

        if author in self.__authors:
            return

        self.__authors.append(author)

    def remove_author(self, author: Author):
        if not isinstance(author, Author):
            return

        if author in self.__authors:
            self.__authors.remove(author)

    @property
    def reviews(self):
        return self.__reviews

    def add_review(self, review):
        if not isinstance(review, Review):
            return
        self.__reviews.append(review)

    def remove_review(self, review):
        if not isinstance(review, Review):
            return

        if review in self.__reviews:
            self.__reviews.remove(review)

    @property
    def ebook(self) -> bool:
        return self.__ebook

    @ebook.setter
    def ebook(self, is_ebook: bool):
        if isinstance(is_ebook, bool):
            self.__ebook = is_ebook

    @property
    def num_pages(self) -> int:
        return self.__num_pages

    @num_pages.setter
    def num_pages(self, num_pages: int):
        if isinstance(num_pages, int) and num_pages >= 0:
            self.__num_pages = num_pages

    def __repr__(self):
        return f'<Book {self.title}, book id = {self.book_id}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.book_id == other.book_id

    def __lt__(self, other):
        return self.book_id < other.book_id

    def __hash__(self):
        return hash(self.book_id)


class User:

    def __init__(self, user_name: str, password: str):
        if user_name == "" or not isinstance(user_name, str):
            self.__user_name = None
        else:
            self.__user_name = user_name.strip()

        if password == "" or not isinstance(password, str) or len(password) < 7:
            self.__password = None
        else:
            self.__password = password

        self.__read_books = []
        self.__reviews = []
        self.__pages_read = 0
        self.__shoppingcart = ShoppingCart()
        self.__purchased_books = {}

    @property
    def user_name(self) -> str:
        return self.__user_name

    @property
    def password(self) -> str:
        return self.__password

    @property
    def read_books(self) -> List[Book]:
        return self.__read_books

    @property
    def reviews(self) -> List["Review"]:
        return self.__reviews

    @property
    def pages_read(self) -> int:
        return self.__pages_read

    @property
    def shoppingcart(self):
        return self.__shoppingcart

    @property
    def purchased_books(self):
        return self.__purchased_books

    def read_a_book(self, book: Book):
        if isinstance(book, Book):
            self.__read_books.append(book)
            if book.num_pages is not None:
                self.__pages_read += book.num_pages

    def add_review(self, review: "Review"):
        if isinstance(review, Review):
            # Review objects are in practice always considered different due to their timestamp.
            self.__reviews.append(review)

    def add_book_to_cart(self, book: Book):
        self.shoppingcart.add_book(book)

    def remove_book_from_cart(self, book: Book):
        self.shoppingcart.remove_book(book)

    def purchase_books_in_cart(self):
        for book_id in self.shoppingcart.books:
            if book_id in self.purchased_books:
                self.purchased_books[book_id] += self.shoppingcart.books[book_id]
            else:
                self.purchased_books[book_id] = self.shoppingcart.books[book_id]
        self.shoppingcart.clear_cart()

    def __repr__(self):
        return f'<User {self.user_name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.user_name == self.user_name

    def __lt__(self, other):
        return self.user_name.lower() < other.user_name.lower()

    def __hash__(self):
        return hash(self.user_name)


class Review:

    def __init__(self, book: Book, review_text: str, rating: int, user: User):
        if isinstance(book, Book):
            self.__book = book
        else:
            self.__book = None

        if isinstance(review_text, str):
            self.__review_text = review_text.strip()
        else:
            self.__review_text = "N/A"

        if isinstance(rating, int) and rating >= 1 and rating <= 5:
            self.__rating = rating
        else:
            raise ValueError

        self.__timestamp = datetime.now()
        self.__user = user

    @property
    def book(self) -> Book:
        return self.__book

    @property
    def review_text(self) -> str:
        return self.__review_text

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    @property
    def user(self):
        return self.__user

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return other.book == self.book and other.review_text == self.review_text \
               and other.rating == self.rating and other.timestamp == self.timestamp

    def __repr__(self):
        return f'<Review of book {self.book}, rating = {self.rating}, timestamp = {self.timestamp}>'


class BooksInventory: 

    def __init__(self):
        self.__books = {}
        self.__prices = {}
        self.__discount = {}
        self.__stock_count = {}

    def add_book(self, book: Book, price: int, nr_books_in_stock: int):
        self.__books[book.book_id] = book
        self.__prices[book.book_id] = price
        self.__discount[book.book_id] = 0
        self.__stock_count[book.book_id] = nr_books_in_stock

    def remove_book(self, book_id: int):
        self.__books.pop(book_id)
        self.__prices.pop(book_id)
        self.__stock_count.pop(book_id)

    def find_book(self, book_id: int):
        if book_id in self.__books.keys():
            return self.__books[book_id]
        return None

    def find_price(self, book_id: int):
        if book_id in self.__books.keys():
            return self.__prices[book_id]
        return None

    def find_stock_count(self, book_id: int):
        if book_id in self.__books.keys():
            return self.__stock_count[book_id]
        return None

    def adjust_stock_count(self, book_id: int, amount_to_deduct: int):
        if book_id in self.__books.keys():
            self.__stock_count[book_id] = self.__stock_count[book_id] - amount_to_deduct
        else:
            return None

    def search_book_by_title(self, book_title: str):
        for book_id in self.__books.keys():
            if self.__books[book_id].title == book_title:
                return self.__books[book_id]
        return None

    def discount_book(self, book_id: int, discount: int):
        if book_id in self.__discount.keys():
            self.__discount[book_id] = discount

    def get_book_discount(self, book_id: int):
        discount = 0

        if book_id in self.__discount.keys():
            discount = self.__discount[book_id]

        return discount


class ShoppingCart:

    def __init__(self):
        self.__books = {}

    def __iter__(self):
        for book_id in self.__books:
            yield book_id


    @property
    def books(self):
        return self.__books

    def add_book(self, book: Book):
        if book.book_id not in self.__books.keys():
            self.books[book.book_id] = 1
        else:
            self.__books[book.book_id] += 1

    def remove_book(self, book: Book):
        if self.books[book.book_id] > 1:
            self.books[book.book_id] -= 1
        else:
            self.books.pop(book.book_id)

    def quantity_of_book(self, book_id):
        if book_id not in self.__books.keys():
            return 0
        else:
            return self.__books[book_id]

    def clear_cart(self):
        self.__books = {}


def make_review(review_text: str, rating: int, book_to_review: Book, user: User):
    review = Review(book_to_review, review_text, rating, user)
    user.add_review(review)
    book_to_review.add_review(review)

    return review


def get_total_price(dict_of_book_ids, inventory: BooksInventory):
    total_price_of_order = 0
    for book_id in dict_of_book_ids:
        discount = inventory.get_book_discount(book_id)
        price_of_book = inventory.find_price(book_id)
        if discount == 0:
            total_price_of_order += dict_of_book_ids[book_id] * price_of_book
        else:
            total_price_of_order += dict_of_book_ids[book_id] * price_of_book * discount / 100
    return total_price_of_order
