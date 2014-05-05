__author__ = 'ajrenold'

# Libs

# Our Imports
from core import db
from model_utils import slugify

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