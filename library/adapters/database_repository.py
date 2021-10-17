from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.exc import IntegrityError
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
        with self._session_cm as scm:
            scm.session.add(book)
            scm.commit()


    def get_book(self, book_id: int) -> Book:
        book = None
        try:
            book = self._session_cm.session.query(Book).filter(Book._Book__book_id == book_id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return book

    def get_book_catalogue(self):
        pass

    def add_review(self, review: Review):
        pass

    def get_reviews(self):
        pass

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()
            user_id = self._session_cm.session.execute('SELECT id FROM users WHERE user_name = :user_name',
                                                       {'user_name': user.user_name}).fetchone()
            print("hello " + str(user_id[0]))

    def get_number_of_books(self):
        pass

    def get_books_by_id(self, id_list: int):
        pass

    # below are the book inv methods
    def get_book_inventory(self):
        pass

    def add_book_to_inventory(self, book: Book, price, nr_books_in_stock):
        pass

    def remove_book_from_inventory(self, book_id):
        pass

    def find_book(self, book_id):
        pass
    
    def find_price(self, book_id):
        pass

    def find_stock_count(self, book_id):
        pass
    
    def adjust_stock_count(self, book_id, amount_to_deduct):
        pass
    
    def search_book_by_title(self, book_title):
        pass
    
    def discount_book(self, book_id, discount):
        pass
    
    def get_book_discount(self, book_id):
        pass

    # below are the shopping cart methods
    def add_book_to_user_shoppingcart(self, user_name: str, book: Book):
        user_id = self._session_cm.session.execute('SELECT id FROM users WHERE user_name = :user_name', {'user_name': user_name}).fetchone()
        user_id = user_id[0]
        """
        self._session_cm.session.execute(
            'INSERT INTO shopping_cart VALUES , user_id, '
        )
        """
        pass
    
    def remove_book_from_user_shoppingcart(self, user_name, book: Book):
        pass
    
    def purchase_books_in_user_shoppingcart(self, user_name):
        pass

    def add_publisher(self, publisher:Publisher):
        with self._session_cm as scm:
            scm.session.add(publisher)
            scm.commit()

    def add_author(self, author_object):
        with self._session_cm as scm:
            scm.session.add(author_object)
            scm.commit()
