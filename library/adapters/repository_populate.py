import random

from pathlib import Path

from library.adapters.repository import AbstractRepository
from library.adapters.jsondatareader import BooksJSONReader


# populates the memory repository with the provided json files
def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    authors_data_path = str(Path(data_path) / "comic_books_excerpt.json")
    book_data_path = str(Path(data_path) / "book_authors_excerpt.json")

    books_data = BooksJSONReader(authors_data_path, book_data_path)
    books_data.read_json_files()
    # book_inventory = repo.get_book_inventory()
    if database_mode is not True:
        for book in books_data.dataset_of_books:
            price, stock_count = random_book_price_and_stock_count()
            repo.add_book_to_inventory(book, price, stock_count)
            repo.add_book(book)
    else:
        books_data.load_data(repo)


    #three_random_book_discount(repo)


def three_random_book_discount(repo: AbstractRepository):
    book_count = repo.get_number_of_books()
    book_catalogue = repo.get_book_catalogue()
    # book_inv = repo.get_book_inventory()
    quantity = 3

    if quantity >= book_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of books.
        quantity = book_count - 1
    
    random_books = random.sample(book_catalogue, quantity)

    for book in random_books:
        repo.discount_book(book.book_id, 50)


def random_book_price_and_stock_count():
    price = random.randint(0, 400)
    stock_count = random.randint(0, 20)

    return price, stock_count