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


@shopping_blueprint.route('/shoppingcart', methods=['GET', 'POST'])
@login_required
def shoppingcart():
    user_name = session['user_name']
    remove_book_message=request.args.get("remove_book_message")
    purchase_message=request.args.get("purchase_message")

    form_search = utilities.SearchForm()
    books = services.get_shopping_cart(user_name, repo.repo_instance)
    total_price = services.get_total_price_shopping_cart(user_name, repo.repo_instance)
    return render_template('shopping/shopping_cart.html',
                            form_search=form_search,
                            books=books,
                            total_price=total_price,
                            remove_book_message=remove_book_message,
                            purchase_message=purchase_message
                            )

@shopping_blueprint.route('/purchase', methods=['GET', 'POST'])
@login_required
def purchase_books():
    user_name = session['user_name']
    services.purchase_books(user_name, repo.repo_instance)

    purchase_message = "Thank you for your purchase :)"

    return redirect(url_for('shopping_bp.shoppingcart', purchase_message=purchase_message))


@shopping_blueprint.route('/purchased_books', methods=['GET', 'POST'])
@login_required
def purchased_books():
    user_name = session['user_name']
    form_search = utilities.SearchForm()
    books = services.get_purchased_books(user_name, repo.repo_instance)
    total_price = services.get_total_price_of_purchased(user_name, repo.repo_instance)
    return render_template('shopping/purchased_books.html', form_search=form_search, books=books, total_price=total_price)


@shopping_blueprint.route('/adding_book_to_cart', methods=['GET', 'POST'])
@login_required
def add_book_to_cart():
    user_name = session['user_name']
    book_id = int(request.args.get('id'))

    book_out_of_stock = None
    book_no_more_stock = None
    book_added_message = None

    try:
        services.add_book_to_user_cart(user_name, book_id, repo.repo_instance)
        book_count = services.get_book_count_in_cart(user_name, book_id, repo.repo_instance)

        book_added_message = str(book_count) + "books are in cart"
    
    except services.OutOfStockException:
        book_out_of_stock = "sorry we are currently out of stock"
    except services.NoMoreStockException:
        book_no_more_stock = "all stock has been added to cart"

    return redirect(url_for('books_bp.books_view',
                            id=book_id, book_out_of_stock=book_out_of_stock,
                            book_no_more_stock=book_no_more_stock,
                            book_added_message=book_added_message)
                            )

@shopping_blueprint.route('/removing_book_from_cart', methods=['GET', 'POST'])
@login_required
def remove_book_from_cart():
    user_name = session['user_name']
    book_id = int(request.args.get('id'))

    remove_book_message = "one book was removed from cart"

    services.remove_book_from_user_cart(user_name, book_id, repo.repo_instance)

    return redirect(url_for('shopping_bp.shoppingcart', remove_book_message=remove_book_message))
