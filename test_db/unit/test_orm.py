import pytest
import datetime

from sqlalchemy.exc import IntegrityError

from library.adapters import orm
from library.domain.model import Author, User, Publisher, Book, make_review

def insert_book(empty_session):
    empty_session.execute('INSERT INTO books (id, title) VALUES (12345, "chicken")')
    row = empty_session.execute('SELECT id from books').fetchone()
    return row[0]


def make_book():
    return Book(12345, 'chicken')


def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]


def make_author():
    return Author(12345678, 'chicken little')


def insert_reviewed_book(empty_session):
    book_id = insert_book(empty_session)
    user_id = insert_user(empty_session)

    timestamp_1 = datetime.datetime.now()
    empty_session.execute(
        'INSERT INTO reviews  (review_text, rating, timestamp, user_id, book_id) '
        'VALUES ("chicken", 1, :timestamp_1, 1234, 12345)',
        {'timestamp_1' : timestamp_1}
    )

    row = empty_session.execute('SELECT id from books').fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def make_user():
    user = User("Andrew", "111abcEFG")
    return user


def test_loading_of_users(empty_session):
    users = list()
    users.append(("Andrew", "1234"))
    users.append(("Cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User("Andrew", "1234"),
        User("Cindy", "999")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = User('chicken', 'little1234!')
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("chicken", "little1234!")]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("Andrew", "1234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("Andrew", "111")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_book(empty_session):
    book_id = insert_book(empty_session)
    expected_book = make_book()
    fetched_book = empty_session.query(Book).one()

    assert expected_book == fetched_book
    assert book_id == fetched_book.book_id


def test_loading_of_reviewed_book(empty_session):
    insert_reviewed_book(empty_session)

    rows = empty_session.query(Book).all()
    book = rows[0]

    for review in book.reviews:
        assert review.book is book


def test_saving_of_review(empty_session):
    book_id = insert_book(empty_session)
    user_key = insert_user(empty_session)

    rows = empty_session.query(Book).all()
    book = rows[0]
    user = empty_session.query(User).filter(User._User__user_name == "Andrew").one()

    review = make_review('chicken', 1, book, user)

    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, book_id, review_text FROM reviews'))

    assert rows == [(user_key, book_id, 'chicken')]


def test_saving_of_book(empty_session):
    book = make_book()
    empty_session.add(book)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT id, title FROM books'))
    assert rows == [(12345, 'chicken')]


def test_saving_book_with_author(empty_session):
    book = make_book()
    author = make_author()

    book.add_author(author)

    empty_session.add(book)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT id FROM books'))
    book_key = rows[0][0]

    rows = list(empty_session.execute('SELECT id, full_name FROM authors'))
    author_key = rows[0][0]
    assert rows[0][1] == 'chicken little'

    rows = list(empty_session.execute('SELECT book_id, author_id FROM book_authors'))
    book_foreign_key = rows[0][0]
    author_foreign_key = rows[0][1]

    assert book_key == book_foreign_key
    assert author_key == author_foreign_key


def test_save_reviewed_book(empty_session):
    book = make_book()
    user = make_user()

    review = make_review('chicken', 1, book, user)

    empty_session.add(book)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT id FROM books'))
    book_key = rows[0][0]

    rows = list(empty_session.execute('SELECT id FROM users'))
    user_key = rows[0][0]

    rows = list(empty_session.execute('SELECT user_id, book_id, review_text FROM reviews'))
    assert rows == [(user_key, book_key, 'chicken')]


def test_loading_and_saving_publisher(empty_session):
    pub = Publisher("12345")
    with empty_session as scm:
        scm.add(pub)
        scm.commit()
    
    assert empty_session.query(Publisher).all() == [Publisher("12345")]


def test_loading_and_saving_author(empty_session):
    author = Author(1234, "chicken little")
    with empty_session as scm:
        scm.add(author)
        scm.commit()
    
    assert empty_session.query(Author).all() == [Author(1234, "chicken little")]
