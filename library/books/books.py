from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import RadioField, TextField, SubmitField, IntegerField, HiddenField
from wtforms.validators import DataRequired

import library.adapters.repository as repo
import library.utilities.utilities as utilities
import library.books.services as services

# configure blueprint
from library.authentication.authentication import login_required

books_blueprint = Blueprint(
    "books_bp", __name__, url_prefix="/catalogue")


@books_blueprint.route('/', methods=['GET'])
def books_catalogue():
    books_per_page = 5
    # read query parameters
    cursor = request.args.get('cursor')

    if cursor is None:
        # no cursor query parameter, so initialise cursor to start at begginign
        cursor = 0
    else:
        # Convert cursor from string to int
        cursor = int(cursor)
    books = services.get_book_catalogue(repo.repo_instance, books_per_page, cursor)
    form_search = utilities.SearchForm()
    return render_template(
        "books/books.html",
        form_search=form_search,
        books=books
    )


@books_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def book_review():
    user_name = session['user_name']
    form_search = utilities.SearchForm()
    form_review = ReviewForm()

    if form_review.validate_on_submit():
        book_id = int(form_review.book_id.data)
        services.add_review(book_id, form_review.review.data, form_review.rating.data, repo.repo_instance)
        return redirect(url_for('books_bp.books_view', id=book_id))

    if request.method == "GET":
        book_id = int(request.args.get('id'))
        form_review.book_id.data = book_id
    book = services.get_book(book_id, repo.repo_instance)
    return render_template('books/book_review.html', id=book_id, form_search=form_search, form_review=form_review, book=book)


@books_blueprint.route('/book', methods=['GET'])
def books_view():
    book_id = int(request.args.get('id'))
    show_reviews_for_book = request.args.get('show_reviews_for_book')
    if show_reviews_for_book is None:
        show_reviews_for_book = -1
    else:
        show_reviews_for_book = int(show_reviews_for_book)
    book = services.get_book(book_id, repo.repo_instance)
    book['url'] = url_for('books_bp.books_view', id=book['id'])
    return render_template(
        "books/books_view.html",
        book=book,
        form_search=utilities.SearchForm(),
        show_reviews_for_book=show_reviews_for_book
    )


@books_blueprint.route('/search', methods=['GET'])
def books_search():
    return render_template(
        'books/books.html',
        form_search=utilities.SearchForm(),
        books=utilities.search_for_books(request.args.get('attribute'), request.args.get('input'), repo.repo_instance)
    )


class ReviewForm(FlaskForm):
    review = TextField('write your review here:', [DataRequired()])
    rating = IntegerField('Your rating out of 5:', [DataRequired()])
    book_id = HiddenField('Book id')
    submit = SubmitField("Submit")
