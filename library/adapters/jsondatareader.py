import json
from typing import List

from library.adapters.repository import AbstractRepository
from library.domain.model import Publisher, Author, Book


class BooksJSONReader:

    def __init__(self, books_file_name: str, authors_file_name: str):
        self.__books_file_name = books_file_name
        self.__authors_file_name = authors_file_name
        self.__dataset_of_books = []


    @property
    def dataset_of_books(self) -> List[Book]:
        return self.__dataset_of_books

    def read_books_file(self) -> list:
        books_json = []
        with open(self.__books_file_name, encoding='UTF-8') as books_jsonfile:
            for line in books_jsonfile:
                book_entry = json.loads(line)
                books_json.append(book_entry)
        return books_json

    def read_authors_file(self) -> list:
        authors_json = []
        with open(self.__authors_file_name, encoding='UTF-8') as authors_jsonfile:
            for line in authors_jsonfile:
                author_entry = json.loads(line)
                authors_json.append(author_entry)
        return authors_json

    def read_json_files(self):
        authors_json = self.read_authors_file()
        books_json = self.read_books_file()

        for book_json in books_json:
            # creates book instance with id and title
            book_instance = Book(int(book_json['book_id']), book_json['title'])
            # adds publisher
            book_instance.publisher= (Publisher(book_json['publisher']))

            # adds publication year if exists
            if book_json['publication_year'] != "":
                book_instance.release_year = int(book_json['publication_year'])

            # adds bool ebook is exists
            if book_json['is_ebook'].lower() == 'false':
                book_instance.ebook = False
            else:
                if book_json['is_ebook'].lower() == 'true':
                    book_instance.ebook = True

            # adds description
            book_instance.description = book_json['description']

            # adds number of pages in book
            if book_json['num_pages'] != "":
                book_instance.num_pages = int(book_json['num_pages'])

            # extract the author ids:
            list_of_authors_ids = book_json['authors']  # extracts list of authors in book
            for author_id in list_of_authors_ids:
                numerical_id = int(author_id['author_id'])
                # We assume book authors are available in the authors file,
                # otherwise more complex handling is required.
                author_name = None
                for author_json in authors_json:
                    if int(author_json['author_id']) == numerical_id:
                        author_name = author_json['name']
                book_instance.add_author(Author(numerical_id, author_name))
            # adds book instance to the dataset of books
            self.__dataset_of_books.append(book_instance)

    def load_data(self, repo: AbstractRepository):
        authors_id_dict = dict()
        authors_name_dict = dict()
        publisher_dict = dict()
        for book in self.__dataset_of_books:
            for author in book.authors:
                if author.unique_id not in authors_id_dict:
                    authors_id_dict[author.unique_id] = list()
                    authors_name_dict[author.unique_id] = author.full_name
                authors_id_dict[author.unique_id].append(book.book_id)

            if book.publisher.name not in publisher_dict.keys():
                publisher_dict[book.publisher.name] = list()
            publisher_dict[book.publisher.name].append(book.book_id)
            book.publisher = None

            book.authors.clear()
        for book in self.__dataset_of_books:
            repo.add_book(book)
        for author_id in authors_id_dict.keys():
            author_object = Author(author_id, authors_name_dict[author_id])
            for book_id in authors_id_dict[author_id]:
                book = repo.get_book(book_id)
                book.add_author(author_object)
            repo.add_author(author_object)

        for publisher_name in publisher_dict.keys():
            publisher_object = Publisher(publisher_name)
            for book_id in publisher_dict[publisher_name]:
                book = repo.get_book(book_id)
                book.publisher = publisher_object
            repo.add_publisher(publisher_object)







