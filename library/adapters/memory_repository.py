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
        self.__search_dictionary = dict()

    def add_book(self, book: Book):
        if isinstance(book, Book):
            self.__books.append(book)
            self.__books_index[book.book_id] = book
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

    def add_search_dictionary(self, search_dictionary: dict):
        self.__search_dictionary = search_dictionary

    def get_search_dictionary(self):
        return self.__search_dictionary


# creates a nested dictionary for searching via, Authors, Publishers, Release Year, Title
def load_search_dictionary(dataset_of_books: list, repo: MemoryRepository):
    """
    iterates the dataset of books

    checks the title, author, publisher and release year
    creates a nested dictionary using the four attributes

    if a book does not contain the attribute, then the book id is added to the key called "N/A"

    adds the search dictionary to the repository
    """
    title_search = dict()
    author_search = dict()
    publisher_search = dict()
    release_year_search = dict()

    search = {
        "title": title_search,
        "author": author_search,
        "publisher": publisher_search,
        "release_year": release_year_search
    }

    for book in dataset_of_books:
        book_id_instance = book.book_id

        # title
        title_instance = book.title if book.title is not None else "N/A"
        if title_instance not in search["title"].keys():
            search["title"][str(title_instance)] = list()
        search["title"][str(title_instance)].append(book_id_instance)

        # author -- there can be many authors
        if book.authors > 0:
            for author in book.authors:
                if author not in search["author"].keys():
                    search["author"][str(author)] = list()
                search["author"][str(author)].append(book_id_instance)

        else:
            author = "N/A"
            if author not in search["author"].keys():
                search["author"][author] = list()
            search["author"][author].append(book_id_instance)

        # publisher
        publisher_instance = book.publisher if book.publisher is not None else "N/A"
        if publisher_instance not in search["publisher"].keys():
            search["publisher"][str(publisher_instance)] = list()
        search["publisher"][str(publisher_instance)].append(book_id_instance)

        # release year
        release_year_instance = book.release_year if book.release_year is not None else "N/A"
        if release_year_instance not in search["release_year"].keys():
            search["release_year"][str(release_year_instance)] = list()
        search["release_year"][str(release_year_instance)].append(book_id_instance)

    repo.add_search_dictionary(search)


# populates the memory repository with the provided json files
def populate(data_path: Path, repo: MemoryRepository):
    authors_data_path = str(Path(data_path) / "comic_books_excerpt.json")
    book_data_path = str(Path(data_path) / "book_authors_excerpt.json")

    books_data = BooksJSONReader(authors_data_path, book_data_path)
    books_data.read_json_files()

    load_search_dictionary(books_data.dataset_of_books, repo)

    for book in books_data.dataset_of_books:
        repo.add_book(book)
