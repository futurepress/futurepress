__author__ = 'ajrenold'

from test.data import books, authors
from models import Book, Author, AppUser, Genre, stormpathUserHash

def bootstrapTestDB(db, refresh_db=False):
    """
        Takes an created SQLAlchemy db and bootstraps the tables
        with dummy data
    """

    # load authors
    for author_data in authors:
        db.session.add(Author.author_from_dict(**author_data))
    db.session.commit()

    # load genres
    for book_data in books:
        for genre in book_data['genres']:
            g = Genre.query.filter_by(name=genre).first()
            if not g:
                db.session.add(Genre(genre))
                db.session.flush()
    db.session.commit()

    # load books
    for book_data in books:
        book_data['genres'] = [ Genre.query.filter_by(name=genre).first() for genre in book_data['genres'] ]
        book_data['author'] = Author.query.filter_by(name=book_data['author']).first()
        db.session.add(Book.book_from_dict(**book_data))
    # commit the changes
    db.session.commit()

    #load users
    for author_data in authors:
        author = Author.query.filter_by(name=author_data['name']).first()
        db.session.add(AppUser(stormpathUserHash(author_data['user_href']), author_data['user_href'], author))
    db.session.commit()
