import os
import unittest
from flask.ext.testing import TestCase

from app import create_app
from core import db, TestConfig
from models import ( Book, Author, Genre, AppUser, stormpathUserHash )
from test.db_create import bootstrapTestDB

EMAIL = 'jake.hartnell@test.com'
PASSWORD = 'Jake1234'
DATABASE_PATH = TestConfig.DATABASE_PATH

class TestSetup(TestCase):

    def create_app(self):
        return create_app('core.TestConfig')

    def test_setup(self):

        self.assertTrue(self.app is not None)
        self.assertTrue(self.client is not None)
        self.assertTrue(self._ctx is not None)

class TestBookQuery(TestCase):

    def create_app(self):
        return create_app('core.TestConfig')

    def setUp(self):
        if os.path.isfile(DATABASE_PATH):
            os.remove(DATABASE_PATH)
        db.create_all()
        bootstrapTestDB(db)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove(DATABASE_PATH)

    def test_book_one_title(self):
        book = Book.query.get(1)
        assert book.title == "Super Sad True Love Story"

    def test_book_one_genres(self):
        book = Book.query.get(1)

        genre_one = book.genres[0]
        assert genre_one.name == "Fiction"
        assert genre_one.slug == "fiction"

        genre_two = book.genres[1]
        assert genre_two.name == "Romance"
        assert genre_two.slug == "romance"

    def test_book_one_author(self):
        book = Book.query.get(1)

        author = book.author
        assert author.name == "Gary Shteyngart"
        assert author.user_id == "26bgM8tHF8clJCykQvIFCJ"


class TestAuthorQuery(TestCase):

    def create_app(self):
        return create_app('core.TestConfig')

    def setUp(self):
        if os.path.isfile(DATABASE_PATH):
            os.remove(DATABASE_PATH)
        db.create_all()
        bootstrapTestDB(db)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove(DATABASE_PATH)

    def test_author_name(self):
        author = Author.query.get(1)
        assert author.name == "Gary Shteyngart"

    def test_author_app_user_relation(self):
        author = Author.query.filter_by(name="Jake Hartnell").first()
        app_user = AppUser.query.get(author.user_id)

        assert author.user_id == stormpathUserHash(app_user.user_href)
        assert author.user_id == app_user.user_id


if __name__ == '__main__':
    unittest.main()