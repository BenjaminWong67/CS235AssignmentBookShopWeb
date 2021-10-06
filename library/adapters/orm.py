from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import backref, mapper, relationship, synonym
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Boolean

from library.domain import model

metadata = MetaData()

# domainn and relationship tables will go here
publisher_table = Table(
    'publishers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), unique=True, nullable=False)
)

authors_table = Table(
    'authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(255), unique=True, nullable=False)
)

books_table = Table(
    'books', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('publisher_id', ForeignKey('publishers.id')),
    Column('title', String(500), unique=True, nullable=False),
    Column('description', String(2000)),
    Column('release_year', Integer),
    Column('ebook', Boolean),
    Column('price', Integer), # not sure if  this should be here
    Column('discount', Integer), # not sure if  this should be here
    Column('stock_count', Integer) # not sure if  this should be here
)

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('review_text', String(1000), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False),
    Column('user', ForeignKey('users.id'))
)


def map_model_to_tables():
    mapper(model.Publisher, publisher_table, properties={
        '_Publisher__name' : publisher_table.c.name
    })

    mapper(model.Author, authors_table, properties={
        '_Author__author_id' : authors_table.c.id,
        '_Author__full_name' : authors_table.c.full_name,
        '_Author__authors_this_one_has_worked_with' : relationship(model.Author)
    })

    mapper(model.Book, books_table, properties={
        '_Book__book_id' : books_table.c.id,
        '_Book__publisher' : books_table.c.publisher_id,
        '_Book__title' : books_table.c.title,
        '_Book__description' : books_table.c.description,
        '_Book__release_year' : books_table.c.release_year,
        '_Book__ebook' : books_table.c.ebook,
        '_Book__num_pages' : books_table.c.num_pages,
        '_Book__authors' : relationship(model.Author, back_populates='_Book__authors'),
        '_Book__reviews' : relationship(model.Review, back_populates='_Review__book')
    })

    mapper(model.User, users_table, properties={
        '_User__user_name' : users_table.c.user_name,
        '_User_password' : users_table.c.password,
        '_User__read_books' : relationship(model.Book),
        '_User__reviews' : relationship(model.Review, backref='_Review__user'),
        '_User__pages_read' : users_table.c.pages_read,
        '_User__purchased_books' : relationship(model.Book)
    })

    mapper(model.Review, reviews_table, properties={
        '_Review__book' : reviews_table.c.book,
        '_Review__review_text' : reviews_table.c.review_text,
        '_Review__rating' : reviews_table.c.rating,
        '_Review__timestamp' : reviews_table.c.timestamp,
    })

    mapper(model.BooksInventory, books_table, properties={
        # not sure what to put here yet
    })