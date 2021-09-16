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


@books_blueprint.route('/', methods=['GET'])
def books_catalogue():

    form = utilities.SearchForm()

    return render_template("books/books.html",
                           form=form
                           )


@books_blueprint.route('/search', methods=['GET'])
def books_search():

    search_attribute = request.args.get('attribute')
    search_input = request.args.get('input')

    form = utilities.SearchForm()

    return render_template('books/books.html',
                           form=form
                           )
