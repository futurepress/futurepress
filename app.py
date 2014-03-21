import os
import sys
from flask import (Flask, request, session, g,
                    redirect, url_for, abort,
                    render_template, flash, jsonify
                )
from flask.ext.stormpath import (StormpathManager,
                                User,
                                login_required,
                                login_user,
                                logout_user,
                                user,
                            )

from key import ( apiKey_id, apiKey_secret )
from stormpath.error import Error as StormpathError
from settings import basedir

from models import ( Book, Author, Genre, AppUser, stormpathUserHash )
from core import db

def create_app(config_object):

    app = Flask(__name__)
    app.config.from_object(config_object)
    db.init_app(app)
    stormpath_manager = StormpathManager(app)
    stormpath_manager.login_view = '.login'

    @app.context_processor
    def inject_appuser():
        if user.is_authenticated():
            user_id = user.get_id()
            app_user = AppUser.query.get(stormpathUserHash(user_id))
            return dict(app_user=app_user)
        return dict(app_user=None)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/book/<int:book_id>')
    def bookpage(book_id):
        if book_id:
            book = Book.query.get(book_id)
            if book:
                #return jsonify(book.as_dict())
                return render_template('bookpage.html', book=book)
        return redirect(url_for('index'))

    @app.route('/author/<author_slug>')
    def authorpage(author_slug):
        if author_slug:
            author = Author.query.filter_by(slug=author_slug).first()
            if author:
                #return jsonify(author.as_dict())
                return render_template('authorpage.html', author=author)
        return redirect(url_for('index'))

    @app.route('/genre/<genre_slug>')
    def genrepage(genre_slug):
        if genre_slug:
            genre = Genre.query.filter_by(slug=genre_slug).first()
            if genre:
                #return jsonify(author.as_dict())
                return render_template('genrepage.html', genre=genre)
        return redirect(url_for('index'))

    @app.route('/copyright')
    def copyright():
        return render_template('copyright.html')

    @app.route('/makers')
    def makers():
        """ """
        if user.is_authenticated():
            return render_template('makers.html')

        return render_template('makers.html')

    @app.route('/readers')
    def readers():
        if user.is_authenticated():
            return render_template('readers.html')

        return render_template('readers.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """
        This view allows a user to register for the site.

        This will create a new User in Stormpath, and then log the user into their
        new account immediately (no email verification required).
        """
        if request.method == 'GET':
            if user.is_authenticated():
                return redirect(url_for('index'))

            return render_template('register.html')

        is_author = True if request.form.get('is_author') is not None else False

        try:
            _user = stormpath_manager.application.accounts.create({
                'username': request.form.get('username'),
                'email': request.form.get('email'),
                'password': request.form.get('password'),
                'given_name': request.form.get('first_name'),
                'surname': request.form.get('last_name'),
                'custom_data': { 'is_author': is_author }
            })
            _user.__class__ = User

        except StormpathError, err:
            return render_template('register.html', error=err.message)

        login_user(_user, remember=True)
        return redirect(url_for('index'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """ User login/auth/session management """
        if request.method == 'GET':
            if user.is_authenticated():
                return redirect(url_for('index'))

            return render_template('login.html')

        try:
            _user = User.from_login(
                request.form.get('email'),
                request.form.get('password'),
            )
        except StormpathError, err:
            return render_template('login.html', error=err.message)

        login_user(_user, remember=True)
        return redirect(url_for('index'))

    @app.route('/logout')
    @login_required
    def logout():
        """User logout/auth/session managment"""
        logout_user()
        return redirect(url_for('index'))

    return app

if __name__ == "__main__":

    app = create_app('core.DevConfig')

    args = sys.argv
    if args[1] == 'dev':
        from test.db_create import bootstrapTestDB
        if not os.path.isfile("dev.db"):
            print "dev.db not found, creating..."
            with app.app_context():
                db.create_all()
                bootstrapTestDB(db)

    else:
        print 'run app with "$ python app.py dev"'
        sys.exit()

    app.run()
