from library.adapters.repository import AbstractRepository
from library.domain.model import Book, User, BooksInventory, Author, Publisher, Review


def search_repository_by_attribute(attribute: str, input: str, repo: AbstractRepository):
    search_dictionary = repo.get_search_dictionary()

    search_input = None if input not in search_dictionary[attribute].keys() else input
    if search_input is None:
        return search_input
    return search_dictionary[attribute][search_input]

