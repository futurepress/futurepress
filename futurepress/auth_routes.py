__author__ = 'ajrenold'

# Lib Imports
from flask import ( request, session, g,
                    redirect, url_for, abort,
                    render_template, flash, jsonify,
                    make_response, Blueprint
                )

from flask.ext.stormpath import (StormpathManager,
                                User,
                                login_required,
                                login_user,
                                logout_user,
                                user,
                            )
from stormpath.error import Error as StormpathError


# Our Imports

auth_routes = Blueprint('auth_routes', __name__,
                        template_folder='templates')

stormpath_manager = StormpathManager()
@auth_routes.record_once
def on_load(state):
    stormpath_manager.init_app(state.app)

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

@auth_routes.route('/logout')
@login_required
def logout():
    """User logout/auth/session managment"""
    logout_user()
    return redirect(url_for('index'))