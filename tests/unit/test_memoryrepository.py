"""Name: Benjamin Wong UPI:BLU378 last-Modified:1:07pm 2/8/2021"""
from library.adapters import memoryrepository
from library.adapters.jsondatareader import BooksJSONReader
from library.adapters.memoryrepository import MemoryRepository
from library.domain.model import Book, User, BooksInventory, Author, Publisher, Review
from utils import get_project_root

class TestPublisher:

    def test_memoryrepository_construction(self):
        repo = MemoryRepository()
        book = Book(123, "Choo Choo")
        repo.add_book(book)
        print(repo.get_book("Choo Choo"))

    def test_populate_memory_repo(self):
        repo = MemoryRepository()
        author_files_name = get_project_root() / "library" / "adapters" / "data" / "comic_books_excerpt.json"
        book_files_name = get_project_root() / "library" / "adapters" / "data" / "book_authors_excerpt.json"
        memoryrepository.populate(author_files_name, book_files_name, repo)

