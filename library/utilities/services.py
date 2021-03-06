from typing import Iterable

import random

from library.adapters.repository import AbstractRepository
from library.domain.model import Book, Author, BooksInventory, Publisher


def get_random_books(quantity: int, repo: AbstractRepository):
    book_count = repo.get_number_of_books()
    book_catalogue = repo.get_book_catalogue()
    # book_inv = repo.get_book_inventory()
    
    selected_books = list()

    if quantity >= book_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of books.
        quantity = book_count - 1
    
    random_books = random.sample(book_catalogue, quantity)

    for book in random_books:
        selected_books.append(book_to_dict(book, repo))

    return selected_books


def search_with_title(input: str, repo: AbstractRepository):
    books_catalogue = repo.get_book_catalogue()
    # book_inv = repo.get_book_inventory()

    books = list()

    for book in books_catalogue:
        if book.title == input:
            books.append(book_to_dict(book, repo))

    return books


def search_with_author(input: str, repo: AbstractRepository):
    books_catalogue = repo.get_book_catalogue()
    # book_inv = repo.get_book_inventory()

    books = list()

    for book in books_catalogue:
        authors = book.authors
        for author in authors:
            if author.full_name == input:
                books.append(book_to_dict(book, repo))
                break

    return books


def search_with_publisher(input: str, repo: AbstractRepository):
    books_catalogue = repo.get_book_catalogue()
    # books_inv = repo.get_book_inventory()

    books = list()

    for book in books_catalogue:
        if book.publisher is None:
            continue
        publisher = book.publisher
        if publisher.name == input:
            books.append(book_to_dict(book, repo))

    return books


def search_with_release_year(input: str, repo: AbstractRepository):
    books_catalogue = repo.get_book_catalogue()
    # book_inv = repo.get_book_inventory()

    books = list()

    for book in books_catalogue:
        release_year = book.release_year
        if str(release_year) == input:
            books.append(book_to_dict(book, repo))

    return books


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
        'price':repo.find_price(book.book_id),
        'stock_count':repo.find_stock_count(book.book_id),
        'discount':repo.get_book_discount(book.book_id)
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
    if len(authors) == 0:
        return list()
    return [author_to_dict(author) for author in authors]
