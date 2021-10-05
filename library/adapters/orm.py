from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey, Boolean
)
from sqlalchemy.orm import mapper, relationship, synonym

from library.domain import model

metadata = MetaData()

# domain tables will go here
publishers_table = Table(
    'publishers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('publisher_name', String(255), unique=True, nullable=False)
)

authors_table = Table(
    'authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('author_name', String(255), nullable=False)
)

books_table = Table(
    'books', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('description', String(1024), nullable=True),
    Column('publisher_id', ForeignKey('publishers.id'), nullable=True),
    Column('release_year', Integer, nullable=True),
    Column('ebook', Boolean, nullable=True),
    Column('num_pages', Integer, nullable=True)
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', ForeignKey('books.id'), nullable=False),
    Column('review_text', String(1024), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False),
    Column('user_id', ForeignKey('users.id'))
)

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, autoincrement=True),
    Column('password', String(255), nullable=False),
    Column('pages_read', Integer, nullable=False),
    Column('shopping_cart', ForeignKey('shopping_carts.id'))
)

book_inventory_table = Table(
    'book_inventories', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True)
)

shopping_carts_table = Table(
    'shopping_carts', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True)
)


def map_model_to_tables():
    mapper(model.Publisher, publishers_table, properties={
        '_Publisher__name': publishers_table.c.publisher_name
    })
    mapper(model.Author, authors_table, properties={
        '_Author__unique_id': authors_table.c.id,
        '_Author__full_name': authors_table.c.author_name,
        #'_Author__authors_this_one_has_worked_with': relationship(String, backref=)
    })
    mapper(model.Book, books_table, properties={
        '_Book__book_id': books_table.c.id,
        '_Book__title': books_table.c.title
    })
    # mapping will go here