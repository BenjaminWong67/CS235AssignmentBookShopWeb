from datetime import date, datetime

import pytest

import library.adapters.repository as repo
from library.adapters.database_repository import SqlAlchemyRepository
from library.domain.model import User, Book, Review, Author, make_review, get_total_price, BooksInventory, ShoppingCart
from library.adapters.repository import RepositoryException

def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    user2 = User('Martin', '123456789')
    repo.add_user(user)
    repo.add_user(user2)
    my_user = repo.get_user('Dave')
    other_user = repo.get_user(('Martin'))
    print(my_user.id)
    print(other_user.id)
    assert my_user == user and user2 is other_user

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

def test_repository_can_get_book_catalogue(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book_catalogue = repo.get_book_catalogue()

    assert len(book_catalogue) == 20

def test_repo_can_get_number_of_books(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_books = repo.get_number_of_books()

    assert number_of_books == 20

def test_repo_add_book_to_user_shoppingcart(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user1 = User('Ben', '1234567')
    repo.add_user(user1)
    book = repo.get_book(707611)
    user = repo.get_user('Ben')
    repo.add_book_to_user_shoppingcart('Ben', book)
    shopping_cart = repo.get_shopping_cart('Ben')
    assert shopping_cart.quantity_of_book(707611) == 1




def test_repo_remove_book_to_user_shoppingcart(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user1 = User('Ben', '1234567')
    repo.add_user(user1)
    user = repo.get_user('Ben')
    book = repo.get_book(707611)
    repo.add_book_to_user_shoppingcart(user.user_name, book)
    repo.add_book_to_user_shoppingcart(user.user_name, book)
    repo.add_book_to_user_shoppingcart(user.user_name, book)
    repo.remove_book_from_user_shoppingcart(user.user_name, book)
    shopping_cart = repo.get_shopping_cart(user.user_name)
    assert shopping_cart.quantity_of_book(707611) == 2


def test_repo_get_shoppingcart(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user1 = User('Ben', '1234567')
    repo.add_user(user1)
    user = repo.get_user('Ben')
    book = repo.get_book(707611)
    repo.add_book_to_user_shoppingcart(user.user_name, book)
    repo.add_book_to_user_shoppingcart(user.user_name, book)
    repo.add_book_to_user_shoppingcart(user.user_name, book)

    shopping_cart = repo.get_shopping_cart('Ben')
    assert shopping_cart.quantity_of_book(707611) == 3

def test_repo_can_purchase_books(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user1 = User('Ben', '1234567')
    repo.add_user(user1)
    user = repo.get_user('Ben')
    book = repo.get_book(707611)
    repo.add_book_to_user_shoppingcart(user.user_name, book)
    repo.add_book_to_user_shoppingcart(user.user_name, book)
    repo.add_book_to_user_shoppingcart(user.user_name, book)

    repo.purchase_books_in_user_shoppingcart(user.user_name)





