"""
books blueprint will go here:

develop app-route for search here

-things to think about
-should a user be able to search with multiple fields e.g.
   -publisher and author at the same time
"""
from flask import Blueprint, render_template, redirect, url_for, session, request


# configure blueprint
books_blueprint = Blueprint(
    "books_bp", __name__, url_prefix="/books")
