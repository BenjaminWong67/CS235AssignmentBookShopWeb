from datetime import date, datetime

import pytest

import library.adapters.repository as repo
from library.adapters.database_repository import SqlAlchemyRepository
from library.domain.model import User, Book, Review, Author, make_review, get_total_price, BooksInventory, ShoppingCart
from library.adapters.repository import RepositoryException

def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user

def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user(User('fmercury', '6666666'))
    user = repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')

def test_repository_can_add_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = Book(12345, 'Chicken Little')

    repo.add_book(book)


    assert repo.get_book(12345) == book