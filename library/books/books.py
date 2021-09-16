from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import RadioField, TextField, SubmitField
from wtforms.validators import DataRequired

import library.adapters.repository as repo
import library.utilities.utilities as utilities
import library.books.services as services

# configure blueprint
books_blueprint = Blueprint(
    "books_bp", __name__, url_prefix="/catalogue")


@books_blueprint.route('/', methods=['GET'])
def books_catalogue():

    form = utilities.SearchForm()

    return render_template(
        "books/books.html",
        form=form,
        books=None
    )


@books_blueprint.route('/book', methods=['GET'])
def books_view():

    book_id = int(request.args.get('id'))

    book = services.get_book(book_id, repo.repo_instance)
    book['url'] = url_for('books_bp.books_view', id=book['id'])

    return render_template(
        "books/books_view.html",
        book=book,
        form=utilities.SearchForm()
    )


@books_blueprint.route('/search', methods=['GET'])
def books_search():

    return render_template(
        'books/books.html',
        form=utilities.SearchForm(),
        books=utilities.search_for_books(request.args.get('attribute'), request.args.get('input'), repo.repo_instance)
    )
