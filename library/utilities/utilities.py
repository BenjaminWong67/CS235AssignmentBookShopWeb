from flask import Blueprint

from flask_wtf import FlaskForm
from wtforms import TextField, SelectField, SubmitField, StringField
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
