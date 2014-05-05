__author__ = 'ajrenold'

# Libs
from flask import url_for

# Our Imports
from core import db
from model_utils import slugify

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
                 'uri': url_for('author_routes.authorpage', author_slug=self.slug, _external=True),
                 'name': self.name,
                 'slug': self.slug }