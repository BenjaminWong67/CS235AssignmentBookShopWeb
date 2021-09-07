"""Name: Benjamin Wong UPI:BLU378 last-Modified:1:07pm 2/8/2021"""
import pytest

from library.domain.model import Book, User, BooksInventory, Author, Publisher, Review
from library.adapters.repository import RepositoryException


@pytest.fixture
def book():
    return Book(1234, "random_book")


def test_repository_construction(in_memory_repo, book):
    in_memory_repo.add_book(book)
    assert in_memory_repo.get_book(1234) == book


def test_repository_can_add_book(in_memory_repo, book):
    in_memory_repo.add_book(book)
    assert in_memory_repo.get_book(book.book_id) == book


def test_repository_does_not_add_non_book_item(in_memory_repo, book):
    with pytest.raises(ValueError):
        in_memory_repo.add_book("not a book")

    with pytest.raises(ValueError):
        in_memory_repo.add_book(1234)


def test_repository_does_not_return_book_that_does_not_exist(in_memory_repo):
    assert in_memory_repo.get_book(999) is None


def test_repository_can_retrieve_book_catalogue(empty_memory_repo):
    empty_memory_repo.add_book(Book(123, "book1"))
    empty_memory_repo.add_book(Book(456, "book2"))
    assert empty_memory_repo.get_book_catalogue() == [Book(123, "book1"), Book(456, "book2")]

