from flask import Blueprint

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import DataRequired

import library.adapters.repository as repo
import library.utilities.services as services

utilities_blueprint = Blueprint(
    "utilities_bp", __name__,)


class SearchForm(FlaskForm):
    attribute = SelectField('attribute', choices=[("title", "Title"),
                                                  ("author", "Author"),
                                                  ("publisher", "Publisher"),
                                                  ("release_year", "Release Year")]
                            )
    input = StringField('input', [DataRequired()])
    submit = SubmitField('🔎')


def search_for_books(attribute: str, input: str, repo: repo.repo_instance):
    search_results = list()

    if attribute == 'title':
        search_results = services.search_with_title(input, repo)
    elif attribute == 'author':
        search_results = services.search_with_author(input, repo)
    elif attribute == 'publisher':
        search_results = services.search_with_publisher(input, repo)
    elif attribute == 'release_year':
        search_results = services.search_with_release_year(input, repo)

    return search_results

