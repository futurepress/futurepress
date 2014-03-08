__author__ = 'ajrenold'

# db_create.py

from test.data import books, authors
from models import db, Flaskr, Book, Author

def createTestDB(db):

    # create the database and the db table
    db.create_all()

    # load authors
    for author_data in authors:
        db.session.add(Author.author_from_dict(**author_data))
    db.session.commit()

    # load books
    for book_data in books:
        book_data['author'] = Author.query.filter_by(name=book_data['author']).first()
        db.session.add(Book.book_from_dict(**book_data))
    # commit the changes
    db.session.commit()