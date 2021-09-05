"""Initialize Flask app."""
from pathlib import Path
from flask import Flask, render_template

# TODO: Access to the books should be implemented via the repository pattern and using blueprints, so this can not stay here!
from library.domain.model import Book

import library.adapters.repository as repo
from library.adapters.memoryrepository import MemoryRepository, populate

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


def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    data_path = Path('library') / 'adapters' / 'data'

    repo.repo_instance = MemoryRepository()

    populate(data_path, repo.repo_instance)

    @app.route('/')
    def home():
        # Use Jinja to customize a predefined html page rendering the layout for showing a single book.
        return render_template('book_catalogue.html', list_of_books=repo.repo_instance.get_book_catalogue())

    @app.route('/book_info/<int:book_id>')
    def catalogue(book_id):
        book_object = repo.repo_instance.get_book(book_id)
        print(type(book_id))
        return render_template('simple_book.html', book=book_object)

    return app