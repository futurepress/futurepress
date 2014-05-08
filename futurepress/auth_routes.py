__author__ = 'ajrenold'

# Lib Imports
from flask import ( request, session, g,
                    redirect, url_for, abort,
                    render_template, flash, jsonify,
                    make_response, Blueprint
                )
from flask.ext.login import make_secure_token
from flask.ext.stormpath import (StormpathManager,
                                User,
                                login_required,
                                login_user,
                                logout_user,
                                user
)
from stormpath.error import Error as StormpathError


# Our Imports
from models import ( AppUser, stormpathUserHash )
from core import db

auth_routes = Blueprint('auth_routes', __name__,
                        template_folder='templates')

stormpath_manager = StormpathManager()
@auth_routes.record_once
def on_load(state):
    stormpath_manager.init_app(state.app)
    stormpath_manager.login_view = 'auth_routes.login'


@auth_routes.route('/register', methods=['GET', 'POST'])
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

    try:
        _user = stormpath_manager.application.accounts.create({
            'username': request.form.get('username'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'given_name': request.form.get('first_name'),
            'surname': request.form.get('last_name')
        })
        _user.__class__ = User

        app_user = AppUser(_user.get_id())
        db.session.add(app_user)
        db.session.commit()

    except StormpathError, err:
        return render_template('register.html', error=err.message)

    login_user(_user, remember=True)
    return redirect(url_for('index'))

@auth_routes.route('/login', methods=['GET', 'POST'])
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

@auth_routes.route('/authorize_ios', methods=['POST'])
def authorize_iOS():
    """ User login/auth/session management """

    username = request.form.get('username', '1')
    password = request.form.get('password', '2')
    user = None

    try:
        user = User.from_login(username, password)
    except StormpathError, err:
        pass

    if user:
        app_user = AppUser.query.get(stormpathUserHash(user.get_id()))
        t = make_secure_token(username + password)
        if app_user.ios_token != t:
            app_user.set_ios_token(t)
        return jsonify({ 'username': user.username,
                         'user_id': app_user.user_id,
                         'authenticated': True,
                         'ios_token': t
                })
    else:
        return jsonify({ 'username': username,
                 'authenticated': False,
                 'ios_token': None
                })

@auth_routes.route('/logout')
@login_required
def logout():
    """User logout/auth/session managment"""
    logout_user()
    return redirect(url_for('index'))