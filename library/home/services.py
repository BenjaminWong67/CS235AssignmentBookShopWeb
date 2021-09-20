from typing import Iterable

import random

from library.adapters.repository import AbstractRepository
from library.domain.model import Book, Author, Publisher


def get_random_books(quantity: int, repo: AbstractRepository):
    book_count = repo.get_number_of_books()
    
    books = list()

    if quantity >= book_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of books.
        quantity = book_count - 1
    
    random_ids = random.sample(range(1, book_count), quantity)
    random_books = repo.get_books_by_id(random_ids)

    for book in random_books:
        books.append(book_to_dict(book))

    return books


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