__author__ = 'ajrenold'

import re
from unidecode import unidecode
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
        return '<user {}>'.format(self.name)

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

genre_relations = db.Table('genre_relations',
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.genre_id')),
    db.Column('book_id', db.Integer, db.ForeignKey('books.book_id'))
)

class Book(db.Model):

    __tablename__ = 'books'

    # primary key
    book_id = db.Column(db.Integer, primary_key=True)

    # foreign key
    author_id = db.Column(db.Integer, db.ForeignKey('author.author_id'))

    # relationships
    genres = db.relationship('Genre', secondary=genre_relations,
                           backref=db.backref('books', lazy='joined'), lazy='dynamic')

    # other columns
    title = db.Column(db.String, nullable=False)
    publisher = db.Column(db.String, nullable=False)
    cover_large = db.Column(db.String, nullable=False)
    cover_thumb = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False)
    #genres = ["Fiction","Romance"]

    def __init__(self, title, author, publisher, genres, cover_large, cover_thumb):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.genres = genres
        self.cover_large = cover_large
        self.cover_thumb = cover_thumb
        self.slug = slugify(title)

    @staticmethod
    def book_from_dict(**kwargs):
        return Book(kwargs.get('title', ""),
                    kwargs.get('author', ""),
                    kwargs.get('publisher', ""),
                    kwargs.get('genres', ""),
                    kwargs.get('cover_large', ""),
                    kwargs.get('cover_thumb', ""))

    def __repr__(self):
        return '<title {}>'.format(self.title)

    def as_dict(self):
        return { 'title': self.title,
                 'author': self.author.as_dict(),
                 'publisher': self.publisher,
                 'genres': [ g.as_dict() for g in self.genres ],
                 'slug': self.slug }

class Genre(db.Model):
    __tablename__ = 'genres'

    # primary key
    genre_id = db.Column(db.Integer, primary_key=True)

    # relationships
    # genre_relations

    # other columns
    name = db.Column(db.String, nullable=False, unique=True)
    slug = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, name):
        self.name = name
        self.slug = slugify(name)

    def __repr__(self):
        return '<genre {}>'.format(self.name)

    def as_dict(self):
        return { 'name': self.name,
                 'slug': self.slug }

def stormpathUserHash(user_href):
    """
        Gets user hash from stormpath user_href
    """
    return user_href[user_href.rfind('/')+1:]


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        result.extend(unidecode(unicode(word)).split())
    return unicode(delim.join(result))
