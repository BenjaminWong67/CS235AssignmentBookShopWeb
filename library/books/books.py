from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, RadioField, TextField, SubmitField, IntegerField, HiddenField
from wtforms.validators import DataRequired
from library.authentication.authentication import login_required

import library.adapters.repository as repo
import library.utilities.utilities as utilities
import library.books.services as services


# configure blueprint


books_blueprint = Blueprint(
    "books_bp", __name__, url_prefix="/catalogue")


@books_blueprint.route('/', methods=['GET'])
def books_catalogue():

    form_search = utilities.SearchForm()
    featured_books = utilities.get_featured_books(3, repo.repo_instance)
    
    books_per_page = 2
    # read query parameters
    cursor = request.args.get('cursor')
    next_page_url = request.args.get('next_page_url')
    prev_page_url = request.args.get('prev_page_url')

    if cursor is None:
        # no cursor query parameter, so initialise cursor to start at begginning
        cursor = 0
    else:
        # Convert cursor from string to int
        cursor = int(cursor)

    books = services.get_book_catalogue(repo.repo_instance, books_per_page, cursor)

    if services.get_number_of_books(repo.repo_instance) < books_per_page:
        next_page_url = None
        prev_page_url = None
    elif cursor + books_per_page >= services.get_number_of_books(repo.repo_instance):
        next_page_url = None
        prev_page_url = url_for('books_bp.books_catalogue', cursor=cursor-books_per_page)
    elif cursor == 0:
        next_page_url = url_for('books_bp.books_catalogue', cursor=cursor+books_per_page)
        prev_page_url = None
    else:
        next_page_url = url_for('books_bp.books_catalogue', cursor=cursor+books_per_page)
        prev_page_url = url_for('books_bp.books_catalogue', cursor=cursor-books_per_page)

    return render_template(
        "books/books.html",
        form_search=form_search,
        books=books,
        next_page_url=next_page_url,
        prev_page_url=prev_page_url,
        featured_books=featured_books
    )


@books_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def book_review():
    user_name = session['user_name']
    form_search = utilities.SearchForm()
    form_review = ReviewForm()

    if form_review.validate_on_submit():
        book_id = int(form_review.book_id.data)
        services.add_review(book_id, form_review.review.data, int(form_review.rating.data), repo.repo_instance, user_name)
        return redirect(url_for('books_bp.books_view', id=book_id))

    if request.method == "GET":
        book_id = int(request.args.get('id'))
        form_review.book_id.data = book_id

    book = services.get_book(book_id, repo.repo_instance)

    return render_template(
        'books/book_review.html',
        id=book_id,
        form_search=form_search,
        form_review=form_review,
        book=book,
        featured_books=list()
    )


@books_blueprint.route('/book', methods=['GET', 'POST'])
def books_view():

    form_search = utilities.SearchForm()
    featured_books = utilities.get_featured_books(3, repo.repo_instance)

    book_added_message = request.args.get("book_added_message")
    book_out_of_stock = request.args.get("book_out_of_stock")
    book_no_more_stock = request.args.get("book_no_more_stock")

    book_id = int(request.args.get('id'))
    show_reviews_for_book = request.args.get('show_reviews_for_book')

    if show_reviews_for_book is None:
        show_reviews_for_book = -1
    else:
        show_reviews_for_book = int(show_reviews_for_book)

    book = services.get_book(book_id, repo.repo_instance)

    return render_template(
        "books/books_view.html",
        book=book,
        form_search=form_search,
        show_reviews_for_book=show_reviews_for_book,
        featured_books=featured_books,
        book_added_message=book_added_message,
        book_out_of_stock=book_out_of_stock,
        book_no_more_stock=book_no_more_stock
    )


@books_blueprint.route('/search', methods=['GET'])
def books_search():

    form_search = utilities.SearchForm()
    featured_books = utilities.get_featured_books(3, repo.repo_instance)

    next_page_url = request.args.get('next_page_url')
    prev_page_url = request.args.get('prev_page_url')
    attribute = request.args.get('attribute')
    input =  request.args.get('input')
    cursor = request.args.get('cursor')
    books_per_page = 2

    if cursor is None:
        # no cursor query parameter, so initialise cursor to start at begginning
        cursor = 0
    else:
        # Convert cursor from string to int
        cursor = int(cursor)

    list_of_searched_books = utilities.search_for_books(request.args.get('attribute'),
                                                        request.args.get('input'),
                                                        repo.repo_instance)

    part_of_searched_books = utilities.get_searched_results_segment(list_of_searched_books, cursor, books_per_page)

    if len(list_of_searched_books) < books_per_page:
        next_page_url = None
        prev_page_url = None
    elif cursor + books_per_page >= len(list_of_searched_books):
        next_page_url = None
        prev_page_url = url_for('books_bp.books_search', cursor=cursor-books_per_page, attribute=attribute, input=input)
    elif cursor == 0:
        next_page_url = url_for('books_bp.books_search', cursor=cursor+books_per_page, attribute=attribute, input=input)
        prev_page_url = None
    else:
        next_page_url = url_for('books_bp.books_search', cursor=cursor+books_per_page, attribute=attribute, input=input)
        prev_page_url = url_for('books_bp.books_search', cursor=cursor-books_per_page, attribute=attribute, input=input)

    return render_template(
        'books/books.html',
        form_search=form_search,
        books=part_of_searched_books,
        next_page_url=next_page_url,
        prev_page_url=prev_page_url,
        cursor=cursor,
        featured_books=featured_books
    )


class ReviewForm(FlaskForm):
    review = TextAreaField('Write your review here:', [DataRequired()])
    rating = SelectField('Your rating out of 5:', 
                        [DataRequired()], 
                        choices=[('1','1'),
                                ('2','2'),
                                ('3','3'),
                                ('4','4'),
                                ('5','5')]
                        )
    book_id = HiddenField('Book id')
    submit = SubmitField("Submit")
