from typing import Iterable

from flask import url_for

from library.adapters.repository import AbstractRepository
from library.domain.model import Book, User, BooksInventory, Author, Publisher, Review, make_review


def get_book(book_id: int, repo: AbstractRepository):
    book = repo.get_book(book_id)

    return book_to_dict(book)


class KeyErrorException:
    pass


def get_book_catalogue(repo: AbstractRepository, books_per_page: int, cursor: int):
    books_to_show = list()
    book_list = repo.get_book_catalogue()
    if cursor + books_per_page < len(book_list):
        for i in range(cursor, cursor + books_per_page):
            books_to_show.append(book_to_dict(book_list[i]))
    else:
        for j in range(cursor, len(book_list)):
            books_to_show.append(book_to_dict(book_list[j]))
    return books_to_show


def get_number_of_books(repo: AbstractRepository):
    return len(repo.get_book_catalogue())


class NonExistentBookException:
    pass


def add_review(book_id: int, review_text: str, rating: int, repo: AbstractRepository, user_name):
    user_reviewing = repo.get_user(user_name)
    book_to_review = repo.get_book(book_id)

    if book_to_review is None:
        raise NonExistentBookException

    review = make_review(review_text, rating, book_to_review, user_reviewing)
    repo.add_review(review)


def decide_to_display_reviews(book_id: int, repo: AbstractRepository):
    reviews_to_display = repo.get_book(book_id)
    reviews_to_display.change_display_reviews()


# ============================================
# Functions to convert model entities to dicts
# ============================================


def book_to_dict(book: Book):
    book_dict = {
        'id': book.book_id,
        'title': book.title,
        'release_year': book.release_year,
        'description': book.description,
        'publisher': publisher_to_dict(book.publisher),
        'authors': authors_to_dict(book.authors),
        'ebook': book.ebook,
        'num_pages': book.num_pages,
        'reviews': reviews_to_dict(book.reviews),
        'url': url_for('books_bp.books_view', id=book.book_id)
    }
    return book_dict


def publisher_to_dict(publisher: Publisher):
    publisher_dict = {
        'name': publisher.name,
    }
    return publisher_dict


def author_to_dict(author: Author):
    author_dict = {
        'unique_id': author.unique_id,
        'full_name': author.full_name,
    }
    return author_dict


def authors_to_dict(authors: Iterable[Author]):
    return [author_to_dict(author) for author in authors]


def review_to_dict(review: Review):
    review_dict = {
        'user_name': review.user.user_name,
        'book_id': review.book,
        'review_text': review.review_text,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]
