__author__ = 'ajrenold'

from core import db

class AppUser(db.Model):

    __tablename__ = 'app_users'

    # primary key
    user_id = db.Column(db.String, primary_key=True)

    # relationships
    author = db.relationship('Author', uselist=False, backref='app_user')

    #other columns
    user_href = db.Column(db.String, nullable=False)
    is_author = db.Column(db.Boolean, nullable=False)

    def __init__(self, user_id, user_href, author=None):
        self.user_id = user_id
        self.user_href = user_href
        self.author = author
        self.is_author = True if author is not None else False

    def __repr__(self):
        return '<user {}>'.format(self.user_id)