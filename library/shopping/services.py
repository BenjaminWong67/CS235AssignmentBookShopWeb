from typing import Iterable

from flask import url_for

from library.adapters.repository import AbstractRepository
from library.domain.model import Book, User, BooksInventory, Author, Publisher, Review, make_review, ShoppingCart, \
    get_total_price


class NonExistentBookException(Exception):
    pass


class UnknownUserException(Exception):
    pass

class OutOfStockException(Exception):
    pass

class NoMoreStockException(Exception):
    pass


def add_book_to_user_cart(user_name: str, book_id: int, repo: AbstractRepository):
    # book_to_add = repo.get_book_inventory().find_book(book_id)
    book_to_add = repo.find_book(book_id)
    
    if book_to_add is None:
        raise NonExistentBookException
    
    # check if user exists
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    
    # stock_count = repo.get_book_inventory().find_stock_count(book_id)
    stock_count = repo.find_stock_count(book_id)
    if stock_count == 0:
        raise OutOfStockException
    elif stock_count == repo.get_shopping_cart(user_name).quantity_of_book(book_id):
        raise NoMoreStockException
    else:
        repo.add_book_to_user_shoppingcart(user_name, book_to_add)
        # user.add_book_to_cart(book_to_add)


def remove_book_from_user_cart(user_name, book_id, repo: AbstractRepository):
    book_to_remove = repo.get_book(book_id)

    # check if user exists
    user = repo.get_user(user_name)
    if book_to_remove is None:
        raise NonExistentBookException

    if user is None:
        raise UnknownUserException

    repo.remove_book_from_user_shoppingcart(user_name, book_to_remove)
    # user.remove_book_from_cart(book_to_remove)


def get_shopping_cart(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    # book_inv = repo.get_book_inventory()

    if user is None:
        raise UnknownUserException

    user_shopping_cart = shopping_cart_to_dict(user_name, repo)

    return user_shopping_cart


def get_purchased_books(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    # book_inv = repo.get_book_inventory()

    if user is None:
        raise UnknownUserException

    user_purchased_books_as_dict = purchased_books_dict_to_list(user_name, repo)

    return user_purchased_books_as_dict


def purchase_books(user_name, repo: AbstractRepository):
    user = repo.get_user(user_name)
    
    # check if user exists
    if user is None:
        raise UnknownUserException

    adjust_stock_count(user_name, repo)
    repo.purchase_books_in_user_shoppingcart(user_name)
    # user.purchase_books_in_cart()


def get_book_price(book_id: int, repo: AbstractRepository):
    # book_inventory = repo.get_book_inventory()
    book_price = repo.find_price(book_id)
    return book_price


def get_book_stock(book_id: int, repo: AbstractRepository):
    # book_inventory = repo.get_book_inventory()
    book_stock_count = repo.find_stock_count(book_id)
    return book_stock_count


def adjust_stock_count(user_name, repo: AbstractRepository):
    # book_inventory = repo.get_book_inventory()
    books_to_purchase = shopping_cart_to_dict(user_name, repo)
    for book in books_to_purchase:
        repo.adjust_stock_count(book['id'], book['quantity'])


def get_total_price_shopping_cart(user_name: str, repo: AbstractRepository):
    # books_inventory = repo.get_book_inventory()
    user = repo.get_user(user_name)

    if user is None:
        raise UnknownUserException

    return get_total_price(repo.get_shopping_cart(user_name).books, repo)


def get_total_price_of_purchased(user_name: str, repo: AbstractRepository):
    # books_inventory = repo.get_book_inventory()
    user = repo.get_user(user_name)

    if user is None:
        raise UnknownUserException

    return get_total_price(repo.get_purchased_books(user_name), repo)


def get_book_count_in_cart(user_name: str, book_id: int, repo: AbstractRepository):
    shopping_cart = repo.get_user(user_name).shoppingcart
    return shopping_cart.quantity_of_book(book_id)


# ============================================
# Functions to convert model entities to dicts
# ============================================

def book_to_dict(book: Book, repo: AbstractRepository):
    book_dict = {
        'id': book.book_id,
        'title': book.title,
        'release_year': book.release_year,
        'description': book.description,
        'publisher': publisher_to_dict(book.publisher),
        'authors': authors_to_dict(book.authors),
        'ebook': book.ebook,
        'num_pages': book.num_pages,
        'reviews': reviews_to_dict(book.reviews),
        'price': repo.find_price(book.book_id),
        'stock_count': repo.find_stock_count(book.book_id),
        'discount': repo.get_book_discount(book.book_id)
    }
    return book_dict


def publisher_to_dict(publisher: Publisher):
    publisher_dict = {
        'name': publisher.name,
    }
    return publisher_dict


def author_to_dict(author: Author):
    author_dict = {
        'unique_id': author.unique_id,
        'full_name': author.full_name,
    }
    return author_dict


def authors_to_dict(authors: Iterable[Author]):
    return [author_to_dict(author) for author in authors]


def review_to_dict(review: Review):
    review_dict = {
        'user_name': review.user.user_name,
        'book': review.book,
        'review_text': review.review_text,
        'timestamp': review.timestamp,
        'rating': review.rating
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]


def shopping_cart_to_dict(user_name, repo: AbstractRepository):
    shopping_cart_to_list = list()
    books_in_shopping_cart = repo.get_shopping_cart(user_name)
    for book_id in books_in_shopping_cart.books:
        book = book_to_dict(repo.get_book(int(book_id)), repo)
        book['quantity'] = books_in_shopping_cart.books[book_id]
        book['price'] = repo.find_price(book_id)
        shopping_cart_to_list.append(book)
    
    return shopping_cart_to_list


def purchased_books_dict_to_list(user_name, repo: AbstractRepository):
    purchased_books_with_dict = list()
    purchased_books_dict = repo.get_purchased_books(user_name)
    for book_id in purchased_books_dict:
        book = book_to_dict(repo.get_book(int(book_id)), repo)
        book['quantity'] = purchased_books_dict[book_id]
        book['price'] = repo.find_price(book_id)
        purchased_books_with_dict.append(book)

    return purchased_books_with_dict
