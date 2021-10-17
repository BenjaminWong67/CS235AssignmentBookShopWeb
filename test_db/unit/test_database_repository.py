from datetime import date, datetime

import pytest
import sqlite3

import library.adapters.repository as repo
from library.adapters.database_repository import SqlAlchemyRepository
from library.domain.model import User, Book, Review, Author, make_review, get_total_price, BooksInventory, ShoppingCart
from library.adapters.repository import RepositoryException
from library.adapters import orm
from sqlalchemy import select

from test_db.conftest import database_engine


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


def test_reppository_can_add_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('user1', 'abcDEF!123')
    book = Book(12345, 'Chicken Little')
    review = Review(book, 'review test', 3, user)

    repo.add_review(review)
    review2 = repo.get_reviews()

    assert review in review2


def test_repository_can_add_to_book_inventory(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = Book(12345, 'Chicken Little')
    price = 10
    stock = 10

    repo.add_book(book)
    repo.add_book_to_inventory(book, price, stock)
    book1 = repo.find_book(12345)

    assert book == book1


def test_repository_can_remove_book_from_inventory(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = Book(12345, 'Chicken Little')
    price = 10
    stock = 10
    repo.add_book(book)
    repo.add_book_to_inventory(book, price, stock)
    repo.remove_book_from_inventory(12345)
    book1 = repo.find_book(12345)

    assert book1 == None


def test_repository_can_find_price(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = Book(12345, 'Chicken Little')
    price = 10
    stock = 10
    repo.add_book(book)
    repo.add_book_to_inventory(book, price, stock)
    price1 = repo.find_price(12345)

    assert price == price1


def test_repository_can_find_stock_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = Book(123456, 'Chicken Little')
    price = 10
    stock = 10
    repo.add_book(book)
    repo.add_book_to_inventory(book, price, stock)
    stock1 = repo.find_stock_count(123456)

    assert stock == stock1


def test_repository_can_adjust_stock_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = Book(123456, 'Chicken Little')
    price = 10
    stock = 10
    repo.add_book(book)
    repo.add_book_to_inventory(book, price, stock)
    stock1 = repo.find_stock_count(123456)

    assert stock == stock1

    repo.adjust_stock_count(123456, 2)
    stock2 = repo.find_stock_count(123456)

    assert stock-2 == stock2


def test_repository_can_search_book_by_title(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = Book(123456, 'Chicken Little')
    price = 10
    stock = 10
    repo.add_book(book)
    repo.add_book_to_inventory(book, price, stock)
    book1 = repo.search_book_by_title('Chicken Little')

    assert book == book1


def test_repository_can_discount_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = Book(123456, 'Chicken Little')
    price = 10
    stock = 10
    repo.add_book(book)
    repo.add_book_to_inventory(book, price, stock)
    discount = repo.get_book_discount(123456)

    assert discount == 0

    repo.discount_book(123456, 50)
    discount = repo.get_book_discount(123456)

    assert discount == 50


def test_repository_can_get_book_discount(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = Book(123456, 'Chicken Little')
    price = 10
    stock = 10
    repo.add_book(book)
    repo.add_book_to_inventory(book, price, stock)
    discount = repo.get_book_discount(123456)

    assert discount == 0

    repo.discount_book(123456, 50)
    discount = repo.get_book_discount(123456)

    assert discount == 50
