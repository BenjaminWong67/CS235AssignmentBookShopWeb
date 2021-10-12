"""Name: Benjamin Wong UPI:BLU378 last-Modified:12:48pm 2/8/2021"""
import abc

from library.domain.model import Book, User, BooksInventory, Author, Publisher, Review

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_book(self, book: Book):
        """Adds the book into the repository.

        also adds the book to the search dictionary
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book(self, book_id: int) -> Book:
        """Returns the book with book_id from the repository.

        If there is no book with the given book_id return None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_catalogue(self):
        """Returns the book catalogue

        If there is none return None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a review to the repository.
        If the review doesn't have bidirectional links with an Book and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        """
        Delete comment when implement user
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Review not correctly attached to a User')
        """
        if review.book is None or review not in review.book.reviews:
            raise RepositoryException('Review not correctly attached to an Book')

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the reviews stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self):
        """Returns the user
        if there is no user return none
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user):
        """Adds user to user database """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_number_of_books(self):
        """returns number of books in the repo"""
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_books_by_id(self, id_list: int):
        """returns list of books with the given list of ids"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_inventory(self):
        """returns the book inventory"""
        raise NotImplementedError
    
    @abc.abstractmethod
    def add_book_to_inventory(self, book, price, nr_books_in_stock):
        """adds book to book inventory"""
        raise NotImplementedError
    
    @abc.abstractmethod
    def remove_book_from_inventory(self, book_id):
        """removes book from the book inventory"""
        raise NotImplementedError
    
    @abc.abstractmethod
    def find_book(self, book_id):
        """finds book in book inv"""
        raise NotImplementedError
    
    @abc.abstractmethod
    def find_price(self, book_id):
        """finds price in book inv"""
        raise NotImplementedError

    @abc.abstractmethod
    def find_stock_count(self, book_id):
        """finds stock count in book inv"""
        raise NotImplementedError
    
    @abc.abstractmethod
    def adjust_stock_count(self, book_id, amount_to_deduct):
        """adjusts stock count in book inv"""
        raise NotImplementedError
    
    @abc.abstractmethod
    def search_book_by_title(self, book_title):
        """searches book inv by book title"""
        raise NotImplementedError
    
    @abc.abstractmethod
    def discount_book(self, book_id, discount):
        """discounts the book in the book inv"""
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_book_discount(self, book_id):
        """gets the discount from the book inv"""
        raise NotImplementedError
    
