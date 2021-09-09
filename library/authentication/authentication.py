from flask import Blueprint, render_template, redirect, url_for, session, request


# Configure Blueprint.
authentication_blueprint = Blueprint(
    'authentication_bp', __name__, url_prefix='/authentication')
