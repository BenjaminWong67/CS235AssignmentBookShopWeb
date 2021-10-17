from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Boolean

from library.domain import model

metadata = MetaData()

# domain and relationship tables will go here
publisher_table = Table(
    'publishers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False)
)

authors_table = Table(
    'authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(255), nullable=False)
)

books_table = Table(
    'books', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('publisher_id', ForeignKey('publishers.id')),
    Column('title', String(500), unique=True, nullable=False),
    Column('description', String(2000), nullable=True),
    Column('release_year', Integer, nullable=True),
    Column('ebook', Boolean, nullable=True),
    Column('num_pages', Integer, nullable=True),
    Column('prices', Integer, nullable=True), # not sure if  this should be here
    Column('discount', Integer, nullable=True), # not sure if  this should be here
    Column('stock_count', Integer, nullable=True) # not sure if  this should be here
)

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('review_text', String(1000), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False),
    Column('user', Integer, ForeignKey('users.id')),
    Column('book', Integer, ForeignKey('books.id'))
)

# relationship tables

book_authors_table = Table(
    'book_authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('author_id', Integer, ForeignKey('authors.id'))
)

coauthors_table = Table(
    'coauthors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('author_id', Integer, ForeignKey('authors.id')),
    Column('coauthor_id', Integer, ForeignKey('authors.id'))
)


purchased_books_table = Table(
    'purchased_books', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user', Integer,ForeignKey('users.id')),
    Column('book', Integer,ForeignKey('books.id')),
    Column('quantity', Integer)
)

shopping_cart_table = Table(
    'shopping_cart', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user', Integer, ForeignKey('users.id')),
    Column('book', Integer, ForeignKey('books.id')),
    Column('quantity', Integer)
)





def map_model_to_tables():

    mapper(model.Publisher, publisher_table, properties={
        '_Publisher__name' : publisher_table.c.name
    })

    mapper(model.Author, authors_table, properties={
        '_Author__unique_id' : authors_table.c.id,
        '_Author__full_name' : authors_table.c.full_name,
        '_Author__authors_this_one_has_worked_with' : relationship(model.Author,
                                secondary=coauthors_table,
                                primaryjoin=authors_table.c.id==coauthors_table.c.id,
                                secondaryjoin=authors_table.c.id==coauthors_table.c.coauthor_id,
                                backref="left_nodes",
                                collection_class=set
        )
    })

    mapper(model.Book, books_table, properties={
        '_Book__book_id' : books_table.c.id,
        '_Book__title' : books_table.c.title,
        '_Book__publisher': relationship(model.Publisher),
        '_Book__description' : books_table.c.description,
        '_Book__release_year' : books_table.c.release_year,
        '_Book__ebook' : books_table.c.ebook,
        '_Book__num_pages' : books_table.c.num_pages,
        '_Book__authors' : relationship(model.Author, secondary=book_authors_table),
        '_Book__reviews' : relationship(model.Review)
    })
    
    mapper(model.User, users_table, properties={
        '_User__user_name' : users_table.c.user_name,
        '_User__password' : users_table.c.password,
        '_User__reviews' : relationship(model.Review)
        # note when grabbing the user we need to make sure... 
        # we grab the purchased books using sql statements
    })

    mapper(model.Review, reviews_table, properties={
        '_Review__review_text' : reviews_table.c.review_text,
        '_Review__rating' : reviews_table.c.rating,
        '_Review__timestamp' : reviews_table.c.timestamp
    })
    