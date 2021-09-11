from library.adapters.repository import AbstractRepository
from library.domain.model import Book, User, BooksInventory, Author, Publisher, Review


def search_repository_by_attribute(attribute: str, search: str, repo: AbstractRepository):
    """
    :returns list of book ids based on attribute and search parameter
    :returns none
    """
    search_dictionary = repo.get_search_dictionary()

    search_input = None if search not in search_dictionary[attribute].keys() else search

    if search_input is None:
        return search_input

    return search_dictionary[attribute][search_input]


def get_books_from_list_of_ids(book_ids: list, repo: AbstractRepository):
    """
    takes list of book ids and gets the corresponding books from the repository
    returns list of books
    returns None if book_ids is None
    """
    if book_ids is None:
        return None

    list_of_books = list()

    for id in book_ids:
        list_of_books.append(repo.get_book(int(id)))

    return list_of_books

