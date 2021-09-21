from typing import Iterable

import random

from library.adapters.repository import AbstractRepository
from library.domain.model import Book, Author, Publisher


def get_discounted_books(repo: AbstractRepository):
    books = repo.get_book_catalogue()
    book_inv = repo.get_book_inventory()

    discounted_books = list()

    for book in books:
        if book_inv.get_book_discount(book.book_id) != 0:
            discounted_books.append(book_to_dict(book))
    
    return discounted_books


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
    }
    return book_dict


def publisher_to_dict(publisher: Publisher):
    publisher_dict = None

    if publisher is not None:
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