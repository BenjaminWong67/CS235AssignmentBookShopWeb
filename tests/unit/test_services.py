from datetime import date

import pytest

from library.authentication.services import AuthenticationException
from library.books import services as book_services
from library.authentication import services as auth_services
from library.books.services import NonExistentBookException


def test_can_add_user(in_memory_repo):
    new_user_name = 'dummy'
    new_password = '123456'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    user_name = 'dummy'
    password = '123456'
    auth_services.add_user(user_name, password, in_memory_repo)

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'Chicken Little'
    new_password = 'nuggets'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = 'Chicken Little'
    new_password = 'nuggets'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', in_memory_repo)


def test_can_add_review(in_memory_repo):
    book_id = 12349665
    review_text = "Testing was average"
    rating = 3
    user_name = "Ben"

    # Call the service layer to add the review.
    book_services.add_review(book_id, review_text, rating, in_memory_repo, user_name)

    # Retrieve the reviews for the article from the repository.
    reviews_as_dict = book_services.get_reviews_for_book(book_id, in_memory_repo)

    # Check that the comments include a comment with the new comment text.
    assert next(
        (review['review_text'] for review in reviews_as_dict if review['review_text'] == review_text),
        None) is not None

def test_cannot_add_review_for_non_existent_book(in_memory_repo):
    book_id = 19191919919191
    review_text = "WoooOOOOo"
    rating = 2
    user_name = "Ben"

    #Call the service layer to attempt to add comment
    with pytest.raises(book_services.NonExistentBookException):
        book_services.add_review(book_id, review_text, rating, in_memory_repo, user_name)

def test_cannot_add_comment_by_unknown_user(in_memory_repo):
    book_id = 2250580
    review_text = "Pretty good"
    rating = 5
    user_name = "thresh"

    #Call the service layer to attempt to add comment
    with pytest.raises(book_services.UnknownUserException):
        book_services.add_review(book_id, review_text, rating, in_memory_repo, user_name)


