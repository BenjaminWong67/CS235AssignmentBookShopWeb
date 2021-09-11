from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import RadioField, TextField, SubmitField
from wtforms.validators import DataRequired

import library.adapters.repository as repo
import library.utilities.utilities as utilities
import library.books.services as services

# configure blueprint
books_blueprint = Blueprint(
    "books_bp", __name__, url_prefix="/books")


@books_blueprint.route('/search', methods=['GET', 'POST'])
def books_search():

    form = SearchForm()

    if request.method == 'GET':
        return render_template('books/books.html', form=form)
    else:
        search_attribute = form.attribute.data
        search_input = form.input.data

        id_list = services.search_repository_by_attribute(search_attribute, search_input, repo.repo_instance)

        list_of_books = services.get_books_from_list_of_ids(id_list, repo.repo_instance)

        return render_template('books/search.html', list_of_books=list_of_books)


class SearchForm(FlaskForm):
    attribute = RadioField('Search by...',
                           choices=[("title", "Title"),
                                    ("author", "Author"),
                                    ("publisher", "Publisher"),
                                    ("release_year", "Release Year")]
                           )
    input = TextField('input', [DataRequired()])
    submit = SubmitField("Search")
