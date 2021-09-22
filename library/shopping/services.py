from typing import Iterable

from flask import url_for

from library.adapters.repository import AbstractRepository
from library.domain.model import Book, User, BooksInventory, Author, Publisher, Review, make_review, ShoppingCart


def add_book_to_user_cart(user_name: str, book_id: int, repo: AbstractRepository):
    book_to_add = repo.get_book_inventory().find_book(book_id)
    user = repo.get_user(user_name)
    user.add_book_to_cart(book_to_add)


def remove_book_from_user_cart(user_name, book_id, repo: AbstractRepository):
    book_to_remove = repo.get_book(book_id)
    user = repo.get_user(user_name)
    user.remove_book_from_cart(book_to_remove)


def get_shopping_cart(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    book_inv = repo.get_book_inventory()
    user_shopping_cart = shopping_cart_to_list(user.shoppingcart, book_inv)
    for book in user_shopping_cart:
        book['price'] = get_book_price(book['id'], repo)
        book['stock_count'] = get_book_stock(book['id'], repo)
    return user_shopping_cart


def get_purchased_books(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    book_inv = repo.get_book_inventory()
    user_purchased_list = user.purchased_books
    user_purchased_books_as_dict = purchased_books_list_to_list_of_dicts(user_purchased_list, book_inv)
    return user_purchased_books_as_dict


def purchase_books(user_name, repo: AbstractRepository):
    user = repo.get_user(user_name)
    user.purchase_books_in_cart()


def get_book_price(book_id: int, repo: AbstractRepository):
    book_inventory = repo.get_book_inventory()
    book_price = book_inventory.find_price(book_id)
    return book_price


def get_book_stock(book_id: int, repo: AbstractRepository):
    book_inventory = repo.get_book_inventory()
    book_stock_count = book_inventory.find_stock_count(book_id)
    return book_stock_count


# ============================================
# Functions to convert model entities to dicts
# ============================================

def book_to_dict(book: Book, book_inv: BooksInventory):
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
        'price':book_inv.find_price(book.book_id),
        'stock_count':book_inv.find_stock_count(book.book_id),
        'discount':book_inv.get_book_discount(book.book_id)
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


def shopping_cart_to_list(shoppingcart, book_inv):
    shopping_cart_to_list = list()
    for book_id in shoppingcart:
        book = book_to_dict(shoppingcart.get_book(book_id), book_inv)
        shopping_cart_to_list.append(book)
    return shopping_cart_to_list

def purchased_books_list_to_list_of_dicts(purchased_books, book_inv):
    purchased_books_with_dict = list()
    for book in purchased_books:
        purchased_books_with_dict.append(book_to_dict(book, book_inv))
    return purchased_books_with_dict
