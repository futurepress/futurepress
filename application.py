import os
import sys
from flask import (Flask, request, session, g,
                    redirect, url_for, abort,
                    render_template, flash, jsonify,
                    make_response
                )

from flask.ext.sqlalchemy import SQLAlchemy
from migrate.versioning import api

from flask.ext.stormpath import (StormpathManager,
                                User,
                                login_required,
                                login_user,
                                logout_user,
                                user,
                            )

from stormpath.error import Error as StormpathError
from settings import basedir

from futurepress import futurepress_blueprints
from models import ( AppUser, stormpathUserHash )
from core import db, DevConfig

app = Flask(__name__)
db.init_app(app)

stormpath_manager = StormpathManager(app)
stormpath_manager.login_view = 'auth_routes.login'

def create_app(config_object):

    app.config.from_object(config_object)

    for blueprint in futurepress_blueprints:
        app.register_blueprint(blueprint)

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

if __name__ == "__main__":

    create_app('core.DevConfig')
    app.run()
