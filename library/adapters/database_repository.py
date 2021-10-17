from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import update, column
from sqlalchemy.sql.expression import select

from library.adapters import orm

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
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_reviews(self):
        reviews = None
        try:
            reviews = self._session_cm.session.query(Review).all()
        except NoResultFound:
            pass

        return reviews


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

    def get_number_of_books(self):
        pass

    def get_books_by_id(self, id_list: int):
        pass

    def add_book_to_inventory(self, book: Book, price: int, nr_books_in_stock: int):
        book_id = book.book_id
        with self._session_cm as scm:
            scm.session.query(orm.books_table).\
                                filter_by(id = book_id).\
                                update(dict(stock_count=nr_books_in_stock, prices=price, discount=0))
            scm.commit()

    def remove_book_from_inventory(self, book_id):
        with self._session_cm as scm:
            scm.session.query(orm.books_table).\
                                filter_by(id = book_id).\
                                update(dict(prices=None, stock_count=None, discount=None))
            scm.commit()

    def find_book(self, book_id):
        price = self.find_price(book_id)
        if price == None:
            return None
        else:
            try:
                book = self._session_cm.session.query(Book).filter(Book._Book__book_id == book_id).one()
            except NoResultFound:
                # Ignore any exception and return None.
                pass
            return book
    
    def find_price(self, book_id):
        with self._session_cm as scm:
            book_data = scm.session.query(orm.books_table).filter_by(id = book_id).one()
            return book_data['prices']

    def find_stock_count(self, book_id):
        with self._session_cm as scm:
            book_data = scm.session.query(orm.books_table).filter_by(id = book_id).one()
            return book_data['stock_count']

    def adjust_stock_count(self, book_id, amount_to_deduct):
        with self._session_cm as scm:
            stock = self.find_stock_count(book_id)
            scm.session.query(orm.books_table).\
                                filter_by(id = book_id).\
                                update(dict(stock_count = (stock-amount_to_deduct)))
            scm.commit()
    
    def search_book_by_title(self, book_title):
        with self._session_cm as scm:
            book_data = scm.session.query(orm.books_table).filter_by(title = book_title).one()
            book_id = book_data['id']
            return self.find_book(book_id)
    
    def discount_book(self, book_id, discount):
        with self._session_cm as scm:
            scm.session.query(orm.books_table).\
                                filter_by(id = book_id).\
                                update(dict(discount=discount))
            scm.commit()
    
    def get_book_discount(self, book_id):
        with self._session_cm as scm:
            book_data = scm.session.query(orm.books_table).filter_by(id = book_id).one()
            return book_data['discount']

    # below are the shopping cart methods
    def add_book_to_user_shoppingcart(self, user_name: str, book: Book):
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
