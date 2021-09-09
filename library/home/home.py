from flask import Blueprint, render_template, redirect, url_for, session, request

import library.adapters.repository as repo

# configure blueprint
home_blueprint = Blueprint(
    "home_bp", __name__, url_prefix="/")


@home_blueprint.route('/')
def home():
    return render_template("book_catalogue.html", list_of_books=repo.repo_instance.get_book_catalogue())


@home_blueprint.route('/book_info/<int:book_id>')
def catalogue(book_id):
    return render_template("simple_book.html", book=repo.repo_instance.get_book(book_id))
