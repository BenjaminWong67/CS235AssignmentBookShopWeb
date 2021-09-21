from datetime import date
from library.adapters.repository import AbstractRepository

import pytest

from library.authentication.services import AuthenticationException
from library.books import services as book_services
from library.authentication import services as auth_services
from library.utilities import services as util_services
from library.home import services as home_services
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

    # Call the service layer to attempt to add comment
    with pytest.raises(book_services.NonExistentBookException):
        book_services.add_review(book_id, review_text, rating, in_memory_repo, user_name)


def test_cannot_add_reviews_by_unknown_user(in_memory_repo):
    book_id = 2250580
    review_text = "Pretty good"
    rating = 5
    user_name = "thresh"

    # Call the service layer to attempt to add comment
    with pytest.raises(book_services.UnknownUserException):
        book_services.add_review(book_id, review_text, rating, in_memory_repo, user_name)


def test_can_get_book(in_memory_repo):
    book_id = 27036538

    # Call the service layer to attempt to retrieve the Book.
    book_as_dict = book_services.get_book(book_id, in_memory_repo)

    assert book_as_dict['id'] == 27036538
    assert book_as_dict['title'] == "Crossed + One Hundred, Volume 2 (Crossed +100 #2)"
    assert book_as_dict['release_year'] == 2016
    assert book_as_dict['description'] == book_as_dict['description']
    assert book_as_dict['authors'] == [{'unique_id': 14155472, 'full_name': 'Simon Spurrier'},
                                       {'unique_id': 8224446, 'full_name': 'Fernando Heinz'},
                                       {'unique_id': 1251983, 'full_name': 'Rafael Ortiz'},
                                       {'unique_id': 5808419, 'full_name': 'DigiKore Studios'},
                                       {'unique_id': 4346284, 'full_name': 'Jaymes Reed'}]
    assert book_as_dict['ebook'] == False
    assert book_as_dict['num_pages'] == 160
    assert len(book_as_dict['reviews']) == 0


def test_cannot_get_book_with_non_existent_id(in_memory_repo):
    book_id = 12321424

    # Call the service layer to attempt to retrieve the Book.
    with pytest.raises(book_services.NonExistentBookException):
        book_services.get_book(book_id, in_memory_repo)


def test_get_reviews_for_books(in_memory_repo):
    reviews_as_dict = book_services.get_reviews_for_book(707611, in_memory_repo)
    book_to_use = book_services.get_book(707611, in_memory_repo)
    # Check that 1 review was returned for book with id 707611
    assert len(reviews_as_dict) == 1

    # Check that the review relates to the book with id 707611
    book_that_relates_to_review = [review['book'] for review in reviews_as_dict]

    assert 707611 == book_that_relates_to_review[0].book_id
    assert len(book_that_relates_to_review) == 1


def test_get_reviews_for_non_existent_book(in_memory_repo):
    with pytest.raises(NonExistentBookException):
        reviews_as_dict = book_services.get_reviews_for_book(7, in_memory_repo)


def test_get_comments_for_article_without_reviews(in_memory_repo):
    reviews_as_dict = book_services.get_reviews_for_book(27036538, in_memory_repo)
    assert len(reviews_as_dict) == 0


def test_search_with_title(in_memory_repo):
    assert util_services.search_with_title("book1", in_memory_repo) == [{
        'id': 10,
        'title': "book1",
        'release_year': None,
        'description': None,
        'publisher': None,
        'authors': list(),
        'ebook': None,
        'num_pages': None,
    }]


def test_search_with_author(in_memory_repo):
    assert util_services.search_with_author("Tim", in_memory_repo) == [{
        'id': 30,
        'title': "book3",
        'release_year': None,
        'description': None,
        'publisher': None,
        'authors': [{'unique_id': 10, 'full_name': 'Tim',}],
        'ebook': None,
        'num_pages': None,
    }]


def test_search_with_publisher(in_memory_repo):
    assert util_services.search_with_publisher("Ben", in_memory_repo) == [{
        'id': 20,
        'title': "book2",
        'release_year': 1000,
        'description': None,
        'publisher': {'name':'Ben'},
        'authors': list(),
        'ebook': None,
        'num_pages': None,
    }]


def test_search_with_release_year(in_memory_repo):
    assert util_services.search_with_release_year("1000", in_memory_repo) == [{
        'id': 20,
        'title': "book2",
        'release_year': 1000,
        'description': None,
        'publisher': {'name':'Ben'},
        'authors': [],
        'ebook': None,
        'num_pages': None,
    }]

def test_get_discounted_books(small_memory_repo: AbstractRepository):
    discounted_books = home_services.get_discounted_books(small_memory_repo)

    assert discounted_books == [{
        'id': 20,
        'title': "book2",
        'release_year': None,
        'description': None,
        'publisher': None,
        'authors': list(),
        'ebook': None,
        'num_pages': None,
    }]
