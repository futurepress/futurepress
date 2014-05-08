__author__ = 'ajrenold'

from core import db
from model_utils import stormpathUserHash

user_books = db.Table('user_books',
    db.Column('book_id', db.Integer, db.ForeignKey('books.book_id')),
    db.Column('user_id', db.String(128), db.ForeignKey('app_users.user_id'))
)

class AppUser(db.Model):

    __tablename__ = 'app_users'

    # primary key
    user_id = db.Column(db.String(128), primary_key=True)

    # relationships
    author = db.relationship('Author', uselist=False, backref='app_user')
    # user_books table
    books = db.relationship('Book', secondary=user_books,
                           backref=db.backref('app_users', lazy='joined'), lazy='dynamic')

    #other columns
    user_href = db.Column(db.String(1024), nullable=False)
    is_author = db.Column(db.Boolean, nullable=False)
    ios_token = db.Column(db.String(1024))

    def __init__(self, storm_path_user_href):
        self.user_id = stormpathUserHash(storm_path_user_href)
        self.user_href = storm_path_user_href
        self.is_author = False

    def become_author(self, Author):
        self.author = Author
        self.is_author = True

        try:
            db.session.commit()
        except:
            # TODO flash error message
            db.session.rollback()

    def purchase_book(self, book):
        self.books.append(book)

        try:
            db.session.commit()
        except:
            # TODO flash error message
            db.session.rollback()

    def set_ios_token(self, ios_token):
        self.ios_token = ios_token

        try:
            db.session.commit()
        except:
            # TODO flash error message
            db.session.rollback()


    def __repr__(self):
        return '<user {}>'.format(self.user_id)

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'user_href': self.user_href,
            'is_author': self.is_author,
            'author': "" if not self.is_author else self.author.as_dict()
        }