import pytest

from sqlalchemy.exc import IntegrityError

from library.domain.model import User, Publisher

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


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def make_user():
    user = User("Andrew", "111")
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
    pass


def test_loading_of_reviewed_book(empty_session):
    pass


def test_saving_of_review(empty_session):
    pass


def test_saving_of_book(empty_session):
    pass


def test_saving_book_with_author(empty_session):
    pass


def test_save_reviewed_book(empty_session):
    pass


def test_loading_and_saving_publisher(empty_session):
    pub = Publisher("12345")
    with empty_session as scm:
        scm.add(pub)
        scm.commit()
    
    assert empty_session.query(Publisher).all() == [Publisher("12345")]


def test_loading_and_saving_author(empty_session):
    pass
