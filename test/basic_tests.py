import os
import unittest
from flask.ext.testing import TestCase

from flask.ext.stormpath import (
                                User,
                                login_user,
                                logout_user,
                                user
                            )

from app import create_app
from core import db, TestConfig
from models import ( Book, Author, Genre, AppUser, stormpathUserHash )
from test.db_create import bootstrapTestDB

DATABASE_PATH = TestConfig.DATABASE_PATH


def testCreateApp(self):
    return create_app('core.TestConfig')

def testSetUp(self):
    if os.path.isfile(DATABASE_PATH):
        os.remove(DATABASE_PATH)
    db.create_all()
    bootstrapTestDB(db)

def testTearDown(self):
    db.session.remove()
    db.drop_all()
    os.remove(DATABASE_PATH)

class TestSetup(TestCase):

    create_app = testCreateApp

    def test_setup(self):

        self.assertTrue(self.app is not None)
        self.assertTrue(self.client is not None)
        self.assertTrue(self._ctx is not None)

class TestBookQuery(TestCase):

    create_app = testCreateApp
    setUp = testSetUp
    tearDown = testTearDown

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

    create_app = testCreateApp
    setUp = testSetUp
    tearDown = testTearDown

    def test_author_name(self):
        author = Author.query.get(1)
        assert author.name == "Gary Shteyngart"

    def test_author_app_user_relation(self):
        author = Author.query.filter_by(name="Jake Hartnell").first()
        app_user = AppUser.query.get(author.user_id)

        assert author.user_id == stormpathUserHash(app_user.user_href)
        assert author.user_id == app_user.user_id

class TestUserLogin(TestCase):

    create_app = testCreateApp
    setUp = testSetUp
    tearDown = testTearDown

    def test_user_can_login(self):
        _user = User.from_login(
                TestConfig.USER_EMAIL,
                TestConfig.USER_PASSWORD,
            )
        login_user(_user)

        user_id = user.get_id()
        app_user = AppUser.query.get(stormpathUserHash(user_id))
        assert app_user.user_href == user_id

if __name__ == '__main__':
    unittest.main()