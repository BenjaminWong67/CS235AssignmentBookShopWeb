from flask import Blueprint, render_template, redirect, url_for, session, request

import library.adapters.repository as repo

# configure blueprint
home_blueprint = Blueprint(
    "home_bp", __name__, url_prefix="/")


@home_blueprint.route('/')
def home():
    return render_template("home/home.html")
