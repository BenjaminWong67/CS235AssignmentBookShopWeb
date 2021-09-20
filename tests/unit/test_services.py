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

def test_cannot_add_user_with_existing_name(empty_memory_repo):
    user_name = 'dummy'
    password = '123456'
    auth_services.add_user(user_name, password, empty_memory_repo)

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, empty_memory_repo)

def test_authentication_with_valid_credentials(empty_memory_repo):
    new_user_name = 'Chicken Little'
    new_password = 'nuggets'

    auth_services.add_user(new_user_name, new_password, empty_memory_repo)

    try:
        auth_services.authenticate_user(new_user_name, new_password, empty_memory_repo)
    except AuthenticationException:
        assert False

def test_authentication_with_invalid_credentials(empty_memory_repo):
    new_user_name = 'Chicken Little'
    new_password = 'nuggets'

    auth_services.add_user(new_user_name, new_password, empty_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', empty_memory_repo)

def test_can_add_review(empty_memory_repo):
    pass
