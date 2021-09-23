import pytest

from flask import session

def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'

@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('fmercury', 'Test#6^0', b'Your user name is already taken - please supply another'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    client.post(
        '/authentication/register',
        data={'user_name': 'fmercury', 'password': 'Test#6^0'}
    )
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data

def test_login(client):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    client.post(
            'authentication/register',
            data={'user_name': 'name', 'password': 'Test#6^0'}
    )
    response = client.post(
            'authentication/login',
            data={'user_name': 'name', 'password': 'Test#6^0'}
    )

    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['user_name'] == 'name'


def test_logout(client):
    # Login a user.
    client.post(
            'authentication/register',
            data={'user_name': 'name', 'password': 'Test#6^0'}
    )

    with client:
        # Check that logging out clears the user's session.
        client.post(
            'authentication/login',
            data={'user_name': 'name', 'password': 'Test#6^0'}
        )
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'TimBen Book Catalogue' in response.data


def test_login_required_to_review(client):
    response = client.post('catalogue/review')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_login_required_to_access_shopping_cart(client):
    response = client.post('shopping/shoppingcart')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_login_required_to_purchase(client):
    response = client.post('shopping/purchase')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_login_required_to_access_purchased_books(client):
    response = client.post('shopping/purchased_books')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_login_required_to_add_book_to_cart(client):
    response = client.post('shopping/adding_book_to_cart')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_login_required_to_remove_book_from_cart(client):
    response = client.post('shopping/removing_book_from_cart')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_catalogue_without_cursor(client):
    # Check that we can retrieve the catalogue page.
    response = client.get('/catalogue/')
    assert response.status_code == 200

    # Check that without providing a cursor query parameter the page includes the first book.
    assert b'Superman Archives, Vol. 2' in response.data
    assert b'The Thing: Idol of Millions' in response.data

def test_catalogue_with_cursor(client):
    # Check that we can retrieve the catalogue page.
    response = client.get('/catalogue/?cursor=2')
    assert response.status_code == 200

    # Check that without providing a cursor query parameter the page includes the first book.
    assert b'A.I. Revolution, Vol. 1' in response.data
    assert b'Sherlock Holmes: Year One' in response.data

def test_review_article(client):
    client.post(
            'authentication/register',
            data={'user_name': 'name', 'password': 'Test#6^0'}
    )
    client.post(
            'authentication/login',
            data={'user_name': 'name', 'password': 'Test#6^0'}
    )

    client.get('/catalogue/review?id=707611')

    response = client.post(
        '/catalogue/review?id=707611',
        data={'review': 'this book is very boring', 'book_id': 707611, 'rating': '1'}
    )
    assert response.headers['Location'] == 'http://localhost/catalogue/book?id=707611'

    response = client.get('/catalogue/book?id=707611&show_reviews_for_book=707611')
    assert b'this book is very boring' in response.data
    
