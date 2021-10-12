from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from library.domain.model import User, Book, Author, Publisher, Review, BooksInventory, ShoppingCart
from library.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)
    
    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()
    
    def add_book(self, book: Book):
        pass

    def get_book(self, book_id: int) -> Book:
        pass

    def get_book_catalogue(self):
        pass

    def add_review(self, review: Review):
        pass

    def get_reviews(self):
        pass

    def get_user(self):
        pass

    def add_user(self, user):
        pass

    def get_number_of_books(self):
        pass

    def get_books_by_id(self, id_list: int):
        pass

    def get_book_inventory(self):
        pass

    def add_book_to_inventory(self, book, price, nr_books_in_stock):
        return super().add_book_to_inventory(book, price, nr_books_in_stock)

    def remove_book_from_inventory(self, book_id):
        return super().remove_book_from_inventory(book_id)
    
    def find_book(self, book_id):
        return super().find_book(book_id)
    
    def find_price(self, book_id):
        return super().find_price(book_id)

    def find_stock_count(self, book_id):
        return super().find_stock_count(book_id)
    
    def adjust_stock_count(self, book_id, amount_to_deduct):
        return super().adjust_stock_count(book_id, amount_to_deduct)
    
    def search_book_by_title(self, book_title):
        return super().search_book_by_title(book_title)
    
    def discount_book(self, book_id, discount):
        return super().discount_book(book_id, discount)
    
    def get_book_discount(self, book_id):
        return super().get_book_discount(book_id)