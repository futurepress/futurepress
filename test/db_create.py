__author__ = 'ajrenold'

from copy import deepcopy

from test.data import books, authors
from models import Book, Author, AppUser, Genre, stormpathUserHash

def bootstrapTestDB(db):
    """
        Takes an created SQLAlchemy db and bootstraps the tables
        with dummy data
    """
    books_copy, authors_copy = deepcopy(books), deepcopy(authors)

    # load authors
    for author_data in authors:
        db.session.add(Author.author_from_dict(**author_data))
    db.session.commit()

    # load genres
    for book_data in books_copy:
        for genre in book_data['genres']:
            g = Genre.query.filter_by(name=genre).first()
            if not g:
                db.session.add(Genre(genre))
                db.session.flush()
    db.session.commit()

    # load books
    for book_data in books_copy:
        book_data['genres'] = [ Genre.query.filter_by(name=genre_item).first()
                                for genre_item in book_data['genres'] ]
        book_data['author'] = Author.query.filter_by(name=book_data['author']).first()
        db.session.add(Book.book_from_dict(**book_data))
    # commit the changes
    db.session.commit()

    #load users
    for author_data in authors_copy:
        author = Author.query.filter_by(name=author_data['name']).first()
        db.session.add(AppUser(stormpathUserHash(author_data['user_href']), author_data['user_href'], author))
    db.session.commit()