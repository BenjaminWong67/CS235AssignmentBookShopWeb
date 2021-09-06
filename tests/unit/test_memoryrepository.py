"""Name: Benjamin Wong UPI:BLU378 last-Modified:1:07pm 2/8/2021"""
import pytest

from library.domain.model import Book, User, BooksInventory, Author, Publisher, Review
from library.adapters.repository import RepositoryException


def test_repo_construction():

    book = Book(1234, "random_book")
    in_memory_repo.add_book(book)
    assert in_memory_repo.get_book("random_book") == book

