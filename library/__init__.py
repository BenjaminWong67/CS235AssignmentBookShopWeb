"""Initialize Flask app."""
from pathlib import Path
from flask import Flask, render_template

from library.domain.model import Book

import library.adapters.repository as repo
from library.adapters.memory_repository import MemoryRepository, populate

# TODO: Access to the books should be implemented via the repository pattern and using blueprints, so this can not stay here!
#    def create_some_book():
#        some_book = Book(1, "Harry Potter and the Chamber of Secrets")
#        some_book.description = "Ever since Harry Potter had come home for the summer, the Dursleys had been so mean \
#                                 and hideous that all Harry wanted was to get back to the Hogwarts School for \
#                                 Witchcraft and Wizardry. But just as he’s packing his bags, Harry receives a \
#                                 warning from a strange impish creature who says that if Harry returns to Hogwarts, \
#                                 disaster will strike."
#        some_book.release_year = 1999
#        return some_book

def create_app(test_config=None):
    app = Flask(__name__)

    # sets up normal configuration
    app.config.from_object('config.Config')
    data_path = Path("library") / "adapters" / "data"

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    repo.repo_instance = MemoryRepository()

    populate(data_path, repo.repo_instance)

    with app.app_context():
        # home blueprint
        from .home import home
        app.register_blueprint(home.home_blueprint)

        # authentication blueprint
        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        # books blueprint
        from .books import books
        app.register_blueprint(books.books_blueprint)

        # utilities blueprint
        from .utilities import utilities
        app.register_blueprint(utilities.utilities_blueprint)

        # shopping blueprint
        from.shopping import shopping
        app.register_blueprint(shopping.shopping_blueprint)

    return app

