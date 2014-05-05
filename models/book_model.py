__author__ = 'ajrenold'

# Libs
from datetime import date
from urllib2 import urlopen, HTTPError, Request
from urlparse import urlparse
import re
from zipfile import ZipFile
import StringIO
from mimetypes import guess_type

import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection


# Our Imports
from core import db
from model_utils import slugify
from key import s3access, s3secret

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
    last_updated = db.Column(db.Date)
    published = db.Column(db.Date)
    epub_url = db.Column(db.String, nullable=False)
    stream_url = db.Column(db.String, nullable=False)
    atom_entry_url = db.Column(db.String, nullable=False)

    def __init__(self, title, author, publisher, genres, cover_large,
                 cover_thumb, epub_url, stream_url, atom_entry_url):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.genres = genres
        self.cover_large = cover_large
        self.cover_thumb = cover_thumb
        self.slug = slugify(title)
        self.last_updated = date.today()
        self.published = date(2010, 10, 31)
        self.epub_url = epub_url
        self.stream_url = stream_url
        self.atom_entry_url = atom_entry_url

    @staticmethod
    def book_from_dict(**kwargs):
        return Book(kwargs.get('title', ""),
                    kwargs.get('author', ""),
                    kwargs.get('publisher', ""),
                    kwargs.get('genres', ""),
                    kwargs.get('cover_large', ""),
                    kwargs.get('cover_thumb', ""),
                    kwargs.get('epub_url', ""),
                    kwargs.get('stream_url', ""),
                    kwargs.get('atom_entry_url', ""))

    def __repr__(self):
        return '<title {}>'.format(self.title)

    def as_dict(self):
        return { 'title': self.title,
                 'author': self.author.as_dict(),
                 'publisher': self.publisher,
                 'genres': [ g.as_dict() for g in self.genres ],
                 'slug': self.slug }



S3Bucket = 'epubjs.books'

## also see gutenberg book mirror, where 135 =
## http://snowy.arsc.alaska.edu/gutenberg/cache/generated/135/pg135-images.epub
class BookUploader():
    """ Book class
    init with book_file hand an uploaded file
    """
    def __init__(self, filename, book_file):

        if book_file:
            self.zip_file = self.getZipFile(book_file)
            self.file_dir = self.getFileDir(filename)
            self.uploadS3(self.zip_file, self.file_dir) ## Only uploads unzipped epub

    def getZipFile(self, book_file):
        return ZipFile(StringIO.StringIO(book_file.read()))

    def getFileDir(self, filename):
        return filename[:filename.find('.epub')] + '/'

    def uploadS3(self, zip_file, file_dir):
        for f in zip_file.filelist:

            file_mime = guess_type(f.filename)[0]

            conn = S3Connection(s3access, s3secret)
            bucket = conn.get_bucket(S3Bucket)

            k = Key(bucket)
            k.key = file_dir + f.filename

            if file_mime:
                k.set_metadata('Content-Type', file_mime)
            k.set_contents_from_string(zip_file.read(f))

class ValidationError(Exception):
    pass