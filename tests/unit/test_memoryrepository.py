"""Name: Benjamin Wong UPI:BLU378 last-Modified:1:07pm 2/8/2021"""
from library.adapters import memoryrepository
from library.adapters.jsondatareader import BooksJSONReader
from library.adapters.memoryrepository import MemoryRepository
from library.domain.model import Book, User, BooksInventory, Author, Publisher, Review
from utils import get_project_root

import pytest


class TestPublisher:

    def test_memoryrepository_construction(self):
        repo = MemoryRepository()
        book = Book(123, "Choo Choo")
        repo.add_book(book)
        print(repo.get_book("Choo Choo"))

    def test_populate_memory_repo(self):
        data_path = get_project_root() / "library" / "adapters" / "data"
        repo = MemoryRepository()
        memoryrepository.populate(data_path, repo)
        for book in repo.get_book_catalogue():
            print(book)

