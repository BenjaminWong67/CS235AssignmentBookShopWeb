"""
books blueprint will go here:

develop app-route for search here
"""
from flask import Blueprint, render_template, redirect, url_for, session, request


# configure blueprint
books_blueprint = Blueprint(
    "books_bp", __name__, url_prefix="/books")
