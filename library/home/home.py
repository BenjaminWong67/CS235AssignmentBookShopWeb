from flask import Blueprint, render_template, redirect, url_for, session, request

import library.adapters.repository as repo

import library.utilities.utilities as utilities
import library.home.services as services

# configure blueprint
from library.domain.model import Book

home_blueprint = Blueprint(
    "home_bp", __name__)


@home_blueprint.route('/', methods=['GET'])
def home():

    form_search = utilities.SearchForm()

    featured_books = utilities.get_featured_books(3, repo.repo_instance)


    discounted_books = services.get_discounted_books(repo.repo_instance)

    return render_template(
        "home/home.html",
        form_search=form_search,
        featured_books=featured_books,
        discounted_books=discounted_books
    )
