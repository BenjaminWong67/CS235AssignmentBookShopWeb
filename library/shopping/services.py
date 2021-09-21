from typing import Iterable

from flask import url_for

from library.adapters.repository import AbstractRepository
from library.domain.model import Book, User, BooksInventory, Author, Publisher, Review, make_review, ShoppingCart


def add_book_to_user_cart(user_name: str, book_id: int, repo : AbstractRepository):
    book_to_add = repo.get_book_inventory().find_book(book_id)
    user = repo.get_user(user_name)
    user.add_book_to_cart(book_to_add)
    print(len(user.shoppingcart))
