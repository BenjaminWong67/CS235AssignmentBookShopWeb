from flask import Blueprint, url_for

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import DataRequired

import library.adapters.repository as repo
import library.utilities.services as services

utilities_blueprint = Blueprint(
    "utilities_bp", __name__, )


class SearchForm(FlaskForm):
    attribute = SelectField('attribute', choices=[("title", "Title"),
                                                  ("author", "Author"),
                                                  ("publisher", "Publisher"),
                                                  ("release_year", "Release Year")]
                            )
    input = StringField('input', [DataRequired()])
    submit = SubmitField('🔎')


class NoMoreBookException:
    pass


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


def get_searched_results_segment(search_results, cursor: int, books_per_page: int):
    section_of_searched_results = list()
    if cursor + books_per_page < len(search_results):
        for i in range(cursor, cursor + books_per_page):
            section_of_searched_results.append(search_results[i])
    else:
        for j in range(cursor, len(search_results)):
            section_of_searched_results.append(search_results[j])
    return section_of_searched_results

 

