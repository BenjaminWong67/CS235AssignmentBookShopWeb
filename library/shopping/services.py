from typing import Iterable

from flask import url_for

from library.adapters.repository import AbstractRepository
from library.domain.model import Book, User, BooksInventory, Author, Publisher, Review, make_review, ShoppingCart


class NonExistentBookException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_book_to_user_cart(user_name: str, book_id: int, repo: AbstractRepository):
    book_to_add = repo.get_book_inventory().find_book(book_id)
    user = repo.get_user(user_name)

    if book_to_add is None:
        raise NonExistentBookException

    if user is None:
        raise UnknownUserException

    if repo.get_book_inventory().find_stock_count(book_id) == 0:
        pass
    else:
        user.add_book_to_cart(book_to_add)


def remove_book_from_user_cart(user_name, book_id, repo: AbstractRepository):
    book_to_remove = repo.get_book(book_id)
    user = repo.get_user(user_name)

    if book_to_remove is None:
        raise NonExistentBookException

    if user is None:
        raise UnknownUserException
    user.remove_book_from_cart(book_to_remove)


def get_shopping_cart(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)

    if user is None:
        raise UnknownUserException

    user_shopping_cart = shopping_cart_to_dict(user.shoppingcart, repo)
    return user_shopping_cart


def get_purchased_books(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)

    if user is None:
        raise UnknownUserException

    user_purchased_books_as_dict = purchased_books_dict_to_list(user.purchased_books, repo)
    return user_purchased_books_as_dict


def purchase_books(user_name, repo: AbstractRepository):
    user = repo.get_user(user_name)

    if user is None:
        raise UnknownUserException

    adjust_stock_count(user.shoppingcart, repo)
    user.purchase_books_in_cart()


def get_book_price(book_id: int, repo: AbstractRepository):
    book_inventory = repo.get_book_inventory()
    book_price = book_inventory.find_price(book_id)
    return book_price


def get_book_stock(book_id: int, repo: AbstractRepository):
    book_inventory = repo.get_book_inventory()
    book_stock_count = book_inventory.find_stock_count(book_id)
    return book_stock_count


def adjust_stock_count(shoppingcart: ShoppingCart, repo: AbstractRepository):
    book_inventory = repo.get_book_inventory()
    books_to_purchase = shopping_cart_to_dict(shoppingcart, repo)
    for book in books_to_purchase:
        book_inventory.adjust_stock_count(book['id'], book['quantity'])


# ============================================
# Functions to convert model entities to dicts
# ============================================

def book_to_dict(book: Book):
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


def shopping_cart_to_dict(books_in_shopping_cart, repo: AbstractRepository):
    shopping_cart_to_list = list()
    for book_id in books_in_shopping_cart.books:
        book = book_to_dict(books_in_shopping_cart.get_book(book_id))
        book['quantity'] = len(books_in_shopping_cart.books[book_id])
        book['price'] = repo.get_book_inventory().find_price(book_id)
        shopping_cart_to_list.append(book)
    return shopping_cart_to_list


def purchased_books_dict_to_list(purchased_books_dict, repo: AbstractRepository):
    purchased_books_with_dict = list()
    for book_id in purchased_books_dict:
        book = book_to_dict(repo.get_book(int(book_id)))
        book['quantity'] = purchased_books_dict[book_id]
        book['price'] = repo.get_book_inventory().find_price(book_id)
        purchased_books_with_dict.append(book)
    return purchased_books_with_dict
