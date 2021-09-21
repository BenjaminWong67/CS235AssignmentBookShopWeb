from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, RadioField, TextField, SubmitField, IntegerField, HiddenField
from wtforms.validators import DataRequired
from library.authentication.authentication import login_required

import library.adapters.repository as repo
import library.utilities.utilities as utilities
import library.shopping.services as services

# configure blueprint
shopping_blueprint = Blueprint(
    "shopping_bp", __name__, url_prefix="/shopping")


@shopping_blueprint.route('/shoppingcart', methods=['GET'])
@login_required
def shoppingcart():
    pass


@shopping_blueprint.route('/purchased_books', methods=['GET'])
@login_required
def purchased_books():
    pass


@shopping_blueprint.route('/adding_book_to_cart', methods=['GET'])
def add_book_to_cart():
    pass
