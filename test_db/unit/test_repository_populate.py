from datetime import datetime
from sqlalchemy import select, inspect, insert
from sqlalchemy.orm import query

from library.adapters import orm
from library.adapters.orm import metadata
from library.domain import model

def test_database_populate_inspect_table_names(database_engine):
    # get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == sorted(['publishers', 'authors', 'books', 'users', 'reviews',\
                                                'book_authors', 'purchased_books', 'shopping_cart'])


def test_database_populate_select_all_publishers(empty_database_engine):
    inspector = inspect(empty_database_engine)
    name_of_publisher_table = inspector.get_table_names()[3]

    empty_database_engine.execute(insert(orm.publisher_table).values(name='chicken'))

    with empty_database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_publisher_table]])
        result = connection.execute(select_statement)

        all_publishers = []
        for row in result:
            all_publishers.append(row['name'])
        
        assert all_publishers == ['chicken']


def test_database_populate_select_all_authors(empty_database_engine):
    inspector = inspect(empty_database_engine)
    name_of_authors_table = inspector.get_table_names()[0]

    empty_database_engine.execute(insert(orm.authors_table).values(id=12345, full_name='chicken'))

    with empty_database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_authors_table]])
        result = connection.execute(select_statement)

        all_authors = []
        for row in result:
            all_authors.append(row['full_name'])
        
        assert all_authors == ['chicken']


def test_database_populate_select_all_books(empty_database_engine):
    inspector = inspect(empty_database_engine)
    name_of_books_table = inspector.get_table_names()[2]

    empty_database_engine.execute(insert(orm.books_table).values(id=12345, title='chicken'))

    with empty_database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_books_table]])
        result = connection.execute(select_statement)

        all_books = []
        for row in result:
            all_books.append(row['title'])
        
        assert all_books == ['chicken']


def test_database_populate_select_all_users(empty_database_engine):
    inspector = inspect(empty_database_engine)
    name_of_users_table = inspector.get_table_names()[7]

    empty_database_engine.execute(insert(orm.users_table).values(user_name='chicken', password='lITtlE123'))

    with empty_database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])
        
        assert all_users == ['chicken']


def test_database_populate_select_all_reviews(empty_database_engine):
    inspector = inspect(empty_database_engine)
    name_of_reviews_table = inspector.get_table_names()[5]

    empty_database_engine.execute(insert(orm.books_table).values(id=12345, title='chicken'))
    empty_database_engine.execute(insert(orm.users_table).values(id=123456 ,user_name='chicken', password='lITtlE123'))
    empty_database_engine.execute(insert(orm.reviews_table).values(review_text='chicken', rating=1, timestamp=datetime.now(), user_id=123456, book_id=12345))

    with empty_database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_reviews_table]])
        result = connection.execute(select_statement)

        all_reviews = []
        for row in result:
            all_reviews.append(row['review_text'])
        
        assert all_reviews == ['chicken']

