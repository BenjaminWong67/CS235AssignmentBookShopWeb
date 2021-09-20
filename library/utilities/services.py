from typing import Iterable

import random

from library.adapters.repository import AbstractRepository
from library.domain.model import Book, Author, Publisher


def search_with_title(input: str, repo: AbstractRepository):
    books_catalogue = repo.get_book_catalogue()

    books = list()

    for book in books_catalogue:
        if book.title == input:
            books.append(book_to_dict(book))

    return books


def search_with_author(input: str, repo: AbstractRepository):
    
    books_catalogue = repo.get_book_catalogue()

    books = list()

    for book in books_catalogue:
        authors = book.authors
        for author in authors:
            if author.full_name == input:
                books.append(book_to_dict(book))
                break

    return books


def search_with_publisher(input: str, repo: AbstractRepository):
    books_catalogue = repo.get_book_catalogue()

    books = list()

    for book in books_catalogue:
        publisher = book.publisher
        if publisher.name == input:
            books.append(book_to_dict(book))

    return books


def search_with_release_year(input: str, repo: AbstractRepository):
    books_catalogue = repo.get_book_catalogue()

    books = list()

    for book in books_catalogue:
        release_year = book.release_year
        if str(release_year) == input:
            books.append(book_to_dict(book))

    return books


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
