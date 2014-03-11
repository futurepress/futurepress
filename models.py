__author__ = 'ajrenold'

import re
from unidecode import unidecode
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

class AppUser(db.Model):

    __tablename__ = 'app_users'

    # primary key
    user_id = db.Column(db.String, primary_key=True)

    #other columns
    user_href = db.Column(db.String, nullable=False)
    is_author = db.Column(db.Boolean, nullable=False)

    # relationships
    author = db.relationship('Author', uselist=False, backref='app_user')

    def __init__(self, user_id, user_href, author=None):
        self.user_id = user_id
        self.user_href = user_href
        self.author = author
        self.is_author = True if author is not None else False

class Book(db.Model):

    __tablename__ = 'books'

    # primary key
    book_id = db.Column(db.Integer, primary_key=True)

    # foreign key
    author_id = db.Column(db.Integer, db.ForeignKey('author.author_id'))

    # other columns
    title = db.Column(db.String, nullable=False)
    publisher = db.Column(db.String, nullable=False)
    cover_large = db.Column(db.String, nullable=False)
    cover_thumb = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False)
    #genres = ["Fiction","Romance"]

    def __init__(self, title, author, publisher, cover_large, cover_thumb):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.cover_large = cover_large
        self.cover_thumb = cover_thumb
        self.slug = slugify(title)

    @staticmethod
    def book_from_dict(**kwargs):
        return Book(kwargs.get('title', ""),
                    kwargs.get('author', ""),
                    kwargs.get('publisher', ""),
                    kwargs.get('cover_large', ""),
                    kwargs.get('cover_thumb', ""))

    def __repr__(self):
        return '<title {}>'.format(self.title)

    def as_dict(self):
        return { 'title': self.title,
                 'author': self.author.as_dict(),
                 'slug': self.slug }

class Author(db.Model):

    __tablename__ = 'author'

    # primary key
    author_id = db.Column(db.Integer, primary_key=True)

    # relations
    books = db.relationship('Book', backref='author',
                            lazy='dynamic')
    # foreign keys
    user_id = db.Column(db.String, db.ForeignKey('app_users.user_id'))

    # other columns
    name = db.Column(db.String, nullable=False)
    bio = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)
    website = db.Column(db.String, nullable=False)
    blog = db.Column(db.String, nullable=False)
    twitter_id = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False)

    def __init__(self, name, bio, picture, website, blog, twitter_id):
        self.name = name
        self.bio = bio
        self.picture = picture
        self.website = website
        self.blog = blog
        self.twitter_id = twitter_id
        self.slug = slugify(name)

    @staticmethod
    def author_from_dict(**kwargs):
        return Author(kwargs.get('name', ""),
                      kwargs.get('bio', ""),
                      kwargs.get('picture', ""),
                      kwargs.get('website', ""),
                      kwargs.get('blog', ""),
                      kwargs.get('twitter_id', ""))

    def __repr__(self):
        return '<author {}>'.format(self.name)

    def as_dict(self):
        return { 'author_id': self.author_id,
                 'name': self.name,
                 'slug': self.slug }

def stormpathUserHash(user_href):
    """
        Gets user hash from stormpath user_href
    """
    return user_href[user_href.rfind('/')+1:]

def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        result.extend(unidecode(unicode(word)).split())
    return unicode(delim.join(result))
