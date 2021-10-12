"""Name: Benjamin Wong UPI:BLU378 last-Modified:1:07pm 2/8/2021"""
import pytest

from library.domain.model import Book, User, BooksInventory, Author, Publisher, Review
from library.adapters.repository import AbstractRepository, RepositoryException


def test_repository_construction(in_memory_repo):
    book = Book(1234, "random_book")
    in_memory_repo.add_book(book)
    assert in_memory_repo.get_book(1234) == book


def test_repository_can_add_book(in_memory_repo):
    book = Book(1234, "random_book")
    in_memory_repo.add_book(book)
    assert in_memory_repo.get_book(book.book_id) == book


def test_repository_does_not_add_non_book_item(in_memory_repo):
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


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Dummy', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('Dummy') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('Ben')

    assert user == User('Ben', '123456')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_add_review(in_memory_repo):
    book = Book(123456, "Test")
    user = User("testing", "12345")
    review = Review(book, "test review", 5, user)
    in_memory_repo.add_book(book)
    in_memory_repo.add_user(user)
    book.add_review(review)
    in_memory_repo.add_review(review)
    print(in_memory_repo.get_user(review.user.user_name))

    assert review in in_memory_repo.get_reviews()
    assert review in in_memory_repo.get_user(review.user.user_name).reviews
    assert review in in_memory_repo.get_book(123456).reviews


def test_repository_can_get_reviews(in_memory_repo):
    assert len(in_memory_repo.get_reviews()) == 2


# this test may be redundant after database redesign
def test_repository_can_retrieve_from_book_inventory(in_memory_repo):
    assert isinstance(in_memory_repo.get_book_inventory(), BooksInventory) == True


def test_get_books_by_ids(small_memory_repo: AbstractRepository):
    list_ids = [10, 20, 30]

    books = small_memory_repo.get_books_by_id(list_ids)

    assert len(books) == 3

def test_get_number_of_books(small_memory_repo: AbstractRepository):
    assert small_memory_repo.get_number_of_books() == 3
