"""Name: Benjamin Wong UPI:BLU378 last-Modified:12:48pm 2/8/2021"""
import abc
from datetime import date

from library.domain.model import Book, User, BooksInventory, Author, Publisher, Review

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_book(self, book: Book):
        """Adds the book into the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book(self, book_id: int) -> Book:
        """Returns the book with book_id from the repository.

        If there is no book with the given book_id return None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_users(self, user: User):
        """Adds the user into the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username: str) -> User:
        """Returns the user with username from the repository.

        If there is no user with the given username return None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review:Review):
        """Adds the review into the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_review(self, username:str, book_id:int):
        """Returns the review that matches the book_id and the username

        If there is no username or book)id that matches return None
        """
        raise NotImplementedError

