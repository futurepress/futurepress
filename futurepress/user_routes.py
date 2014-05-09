__author__ = 'ajrenold'

# Lib Imports
from flask import ( request, session, g,
                    redirect, url_for, abort,
                    render_template, flash, jsonify,
                    make_response, Blueprint
                )
from werkzeug.contrib.atom import AtomFeed, FeedEntry
from flask.ext.stormpath import (
                                login_required,
                                user,
                                User
                            )
from stormpath.error import Error as StormpathError

# Our Imports
from models import ( AppUser, stormpathUserHash )


user_routes = Blueprint('user_routes', __name__,
                        template_folder='templates')

@user_routes.route('/library', methods=['GET'])
@login_required
def library():
    return render_template('user_library.html')

@user_routes.route('/library/<user_id>.atom', methods=['GET'])
def library_atom(user_id):
    app_user = AppUser.query.get(user_id)
    token = request.args.get('token', '')

    if app_user.ios_token == token:

        feed = AtomFeed('FuturePress Library',
                        feed_url=url_for('user_routes.library_atom',user_id=app_user.user_id, _external=True),
                        subtitle="Library for {}".format(app_user.user_id))

        books = app_user.books
        for book in books:
            feed.add(book.title,
                 author=book.author.as_dict(),
                 id=book.book_id,
                 updated=book.last_updated,
                 published=book.published,
                 links=[
                     {'type': "image/jpeg",
                      'rel': "http://opds-spec.org/image",
                      'href': book.cover_large},
                     {'type': "image/jpeg",
                      'rel': "http://opds-spec.org/image/thumbnail",
                      'href': book.cover_large},
                     {'type': "application/epub+zip",
                      'rel': "http://opds-spec.org/acquisition",
                      'href': book.epub_url},
                     {'type': "application/atom+xml;type=entry;profile=opds-catalog",
                      'rel': "alternate",
                      'href': url_for('book_routes.bookatom', book_id=book.book_id, _external=True)},
                 ]
            )

        return feed.get_response()

    return render_template('error.html'), 404



@user_routes.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'GET':
        return render_template('settings.html')

    ## handle a POST
    try:
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.given_name = request.form.get('first_name')
        user.surname = request.form.get('last_name')
        user.save()
    except StormpathError, err:
        return render_template('settings.html', error=err.message)

    return render_template('settings.html')

@user_routes.route('/appusers', methods=['GET'])
def appusers():

    appusers = AppUser.query.all()
    return jsonify(appusers=[a.as_dict() for a in appusers ])