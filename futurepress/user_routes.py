__author__ = 'ajrenold'

# Lib Imports
from flask import ( request, session, g,
                    redirect, url_for, abort,
                    render_template, flash, jsonify,
                    make_response, Blueprint
                )
from flask.ext.stormpath import (
                                StormpathManager,
                                login_required,
                                user,
                                User
                            )
from stormpath.error import Error as StormpathError

# Our Imports
from models import ( AppUser, stormpathUserHash )


user_routes = Blueprint('user_routes', __name__,
                        template_folder='templates')

stormpath_manager = StormpathManager()
@user_routes.record_once
def on_load(state):
    stormpath_manager.init_app(state.app)

@login_required
@user_routes.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'GET':
        return render_template('settings.html')

    is_author = True if request.form.get('is_author') is not None else False

    try:
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.given_name = request.form.get('first_name')
        user.surname = request.form.get('last_name')
        user.save()
    except StormpathError, err:
        return render_template('settings.html', error=err.message)

    user_id = user.get_id()
    app_user = AppUser.query.get(stormpathUserHash(user_id))

    if app_user.is_author:
        author_name = request.form.get('author_name')
        if author_name != app_user.author.name:
            app_user.author.update_name(author_name)

    return render_template('settings.html')
