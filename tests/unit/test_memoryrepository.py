"""Name: Benjamin Wong UPI:BLU378 last-Modified:1:07pm 2/8/2021"""
import pytest
<<<<<<< HEAD

from library.domain.model import Book, User, BooksInventory, Author, Publisher, Review
from library.adapters.repository import RepositoryException


def test_repo_construction(in_memory_repo):

    book = Book(1234, "random_book")
    in_memory_repo.add_book(book)
    assert in_memory_repo.get_book("random_book") == book
=======

from library import create_app
from library.domain.model import Book, Publisher, Author, BooksInventory,User, Review
from library.adapters.repository import RepositoryException
>>>>>>> develop-approute

##insert tests here
def test(in_memory_repo, client):
    book = Book(1234, "book")
    in_memory_repo.add_book(book)
    assert in_memory_repo.get_book("book") == book
