"""Name: Benjamin Wong UPI:BLU378 last-Modified:1:07pm 2/8/2021"""
from pathlib import Path

from library.adapters.jsondatareader import BooksJSONReader
from library.adapters.repository import AbstractRepository
from library.domain.model import Book, User, BooksInventory, Author, Publisher, Review


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__books = list()
        self.__books_index = dict()
        self.__reviews = list()
        self.__users = list()
        self.__search_dictionary = {
            "title": dict(),
            "author": dict(),
            "publisher": dict(),
            "release_year": dict()
        }

    def add_book(self, book: Book):
        """
        adds book to the repo list and index dictionary
        also indexes the book into the search dictionary

        if the book is already in the list... nothing happens
        a value error is raised when a non book item is passed
        """
        if isinstance(book, Book):
            if book.book_id not in self.__books_index.keys():
                self.__books.append(book)
                self.__books_index[book.book_id] = book

                # index title
                if book.title not in self.__search_dictionary["title"].keys():
                    self.__search_dictionary["title"][book.title] = list()
                self.__search_dictionary["title"][book.title].append(book.book_id)

                # index author
                for author in book.authors:
                    if str(author.full_name) not in self.__search_dictionary["author"].keys():
                        self.__search_dictionary["author"][str(author.full_name)] = list()
                    self.__search_dictionary["author"][str(author.full_name)].append(book.book_id)

                # index publisher
                if str(book.publisher.name) not in self.__search_dictionary["publisher"].keys():
                    self.__search_dictionary["publisher"][str(book.publisher.name)] = list()
                self.__search_dictionary["publisher"][str(book.publisher.name)].append(book.book_id)

                # index release year
                if str(book.release_year) not in self.__search_dictionary["release_year"].keys():
                    self.__search_dictionary["release_year"][str(book.release_year)] = list()
                self.__search_dictionary["release_year"][str(book.release_year)].append(book.book_id)

        else:
            raise ValueError

    def get_book(self, book_id: int) -> Book:
        book = None

        try:
            book = self.__books_index[book_id]
        except KeyError:
            pass

        return book

    def get_book_catalogue(self):
        return self.__books

    def get_search_dictionary(self):
        return self.__search_dictionary


# populates the memory repository with the provided json files
def populate(data_path: Path, repo: MemoryRepository):
    authors_data_path = str(Path(data_path) / "comic_books_excerpt.json")
    book_data_path = str(Path(data_path) / "book_authors_excerpt.json")

    books_data = BooksJSONReader(authors_data_path, book_data_path)
    books_data.read_json_files()

    for book in books_data.dataset_of_books:
        repo.add_book(book)
