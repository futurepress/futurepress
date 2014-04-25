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

    def test_book_one(self):
        book = Book.query.get(1)
        assert book.title == "Super Sad True Love Story"

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

    def test_author_one(self):
        author = Author.query.get(1)
        assert author.name == "Gary Shteyngart"

if __name__ == '__main__':
    unittest.main()