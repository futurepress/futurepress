__author__ = 'ajrenold'

# db_create.py

from test.data import books
from models import db, Flaskr, Book

def createTestDB(db):

    # create the database and the db table
    db.create_all()

    # load testing data
    for book_data in books:
        db.session.add(Book.book_from_kwargs(**book_data))
    # commit the changes
    db.session.commit()