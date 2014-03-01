import os
import sqlite3
from flask import (Flask, request, session, g,
                    redirect, url_for, abort,
                    render_template, flash, jsonify
                )
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.stormpath import (StormpathManager,
                                User,
                                login_required,
                                login_user,
                                logout_user,
                                user,
                            )

from key import ( apiKey_id, apiKey_secret )
from stormpath.error import Error as StormpathError

# grabs folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'my_precious'
USERNAME = 'admin'
PASSWORD = 'password'
STORMPATH_API_KEY_ID = apiKey_id
STORMPATH_API_KEY_SECRET = apiKey_secret
STORMPATH_APPLICATION = 'flask-stormpath-sample'

# define full path for db
DATABASE_PATH = os.path.join(basedir, DATABASE)

# the database uri
SQLALCHEMY_DATABASE_URI ='sqlite:///' + DATABASE_PATH

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)
stormpath_manager = StormpathManager(app)
stormpath_manager.login_view = '.login'

import models

# connect to database
"""def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv"""

# create the database
"""def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()"""

# open db connection
"""def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db"""

# close database connection
"""@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()"""

@app.route('/')
def index():
    """Searches the database for entries, then displays them"""
    entries = db.session.query(models.Flaskr)
    return render_template('index.html')

@app.route('/bookpage')
def bookpage():
    return render_template('bookpage.html')

@app.route('/copyright')
def copyright():
    return render_template('copyright.html')


@app.route('/makers')
def makers():
    return render_template('makers.html')


@app.route('/readers')
def readers():
    return render_template('readers.html')


@app.route('/add', methods=['POST'])
@login_required
def add_entry():
    """ Add new post to database"""
    """
    if not session.get('logged_in'):
        abort(401)
    """

    new_entry = models.Flaskr(request.form['title'], request.form['text'])
    db.session.add(new_entry)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))

@app.route('/delete/', methods=['POST'])
@login_required
def delete_entry():
    """ Delete post from database """
    result = { 'status': 0, 'message': 'Error' }
    post_id = request.form['post_id']
    try:

        db.session.query(models.Flaskr).filter_by(post_id=post_id).delete()
        db.session.commit()
        result = { 'status': 1, 'message': 'Post Deleted' }
        flash('Post {} was successfully deleted'.format(str(post_id)))
        return redirect(url_for('index'))

    except Exception as e:
        result = { 'status': 0, 'message': repr(e) }

    flash('Error deleting Post {}'.format(str(post_id)))
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    This view allows a user to register for the site.

    This will create a new User in Stormpath, and then log the user into their
    new account immediately (no email verification required).
    """
    if request.method == 'GET':
        return render_template('register.html')

    try:
        _user = stormpath_manager.application.accounts.create({
            'username': request.form.get('username'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'given_name': 'John',
            'surname': 'Doe',
        })
        _user.__class__ = User

    except StormpathError, err:
        return render_template('register.html', error=err.message)

    login_user(_user, remember=True)
    flash('Successfully created a new account')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ User login/auth/session management """
    if request.method == 'GET':
        return render_template('login.html')

    try:

        _user = User.from_login(
            request.form.get('username'),
            request.form.get('password'),
        )
    except StormpathError, err:
        return render_template('login.html', error=err.message)

    login_user(_user, remember=True)
    flash('You were logged in')
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    """User logout/auth/session managment"""
    logout_user()
    flash('You were logged out')
    return redirect(url_for('index'))

@app.route('/delete_user/')
@login_required
def delete_user():

    try:
        _user = stormpath_manager.application.accounts.get(user.get_id())
        app.logger.debug(_user)
        #_user.delete()

    except StormpathError, err:
        flash(err.message)
        return redirect(url_for('index'))

    return redirect(url_for('index'))

if __name__ == "__main__":
    #init_db()
    app.run()
