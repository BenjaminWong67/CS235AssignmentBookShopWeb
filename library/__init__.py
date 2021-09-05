"""Initialize Flask app."""

from flask import Flask, render_template

import library.adapters.repository as repo
from library.adapters.memoryrepository import MemoryRepository, populate

from utils import get_project_root

#        # TODO: Access to the books should be implemented via the repository pattern and using blueprints, so this can not stay here!
#        def create_some_book():
#            some_book = Book(1, "Harry Potter and the Chamber of Secrets")
#            some_book.description = "Ever since Harry Potter had come home for the summer, the Dursleys had been so mean \
#                                     and hideous that all Harry wanted was to get back to the Hogwarts School for \
#                                     Witchcraft and Wizardry. But just as he’s packing his bags, Harry receives a \
#                                     warning from a strange impish creature who says that if Harry returns to Hogwarts, \
#                                     disaster will strike."
#            some_book.release_year = 1999
#            return some_book

def create_app(test_config=None):
    app = Flask(__name__)

    # sets up normal configuration
    app.config.from_object('config.Config')

    # setting up testing configuration
    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # creates Memory repo instance
    repo.repo_instance = MemoryRepository()
    data_path = get_project_root() / "library" / "adapters" / "data"
    # fills the repo instance with the provided data_path
    populate(data_path, repo.repo_instance)

    @app.route('/books-by-title', methods=['GET'])
    def page_of_books():
        return render_template("testing.html", books_inventory=repo.repo_instance.get_book_catalogue())

    @app.route('/book/<book_title>', methods=['GET'])
    def book_page(book_title):
        return render_template("testing.html", book=repo.repo_instance.get_book(book_title))

    return app
