__author__ = 'ajrenold'

__author__ = 'ajrenold'

# Lib Imports
from flask import (
                    redirect, url_for, abort,
                    render_template, request,
                    Blueprint
                )
from flask.ext.stormpath import (
                                login_required,
                                user,
                            )
from stormpath.error import Error as StormpathError


# Our Imports
from core import db
from models import ( Author, AppUser, Book, BookUploader, stormpathUserHash )

author_routes = Blueprint('author_routes', __name__,
                        template_folder='templates')

@author_routes.route('/author/<author_slug>')
def authorpage(author_slug):
    if author_slug:
        author = Author.query.filter_by(slug=author_slug).first()
        if author:
            #return jsonify(author.as_dict())
            return render_template('authorpage.html', author=author)
    return redirect(url_for('index'))

@login_required
@author_routes.route('/dashboard')
def author_dashboard():
    user_id = user.get_id()
    app_user = AppUser.query.get(stormpathUserHash(user_id))

    if app_user.is_author:
        return render_template('author_dashboard.html', author=app_user.author)

@login_required
@author_routes.route('/dashboard/add', methods=['GET', 'POST'])
def add_book():
    user_id = user.get_id()
    app_user = AppUser.query.get(stormpathUserHash(user_id))

    if app_user.is_author:
        if request.method == 'GET':
            return render_template('add_book.html', author=app_user.author)


        book_file = request.files.get('epub_file', None)
            # POST is a epub file upload
        if book_file.content_type == 'application/epub+zip' or book_file.content_type == 'application/octet-stream':
            book_upload = BookUploader(book_file.filename, book_file)
            book_location = book_upload.file_dir[:-1]

        # fetch genres too!
        book_data = {
                      'author': app_user.author,
                      'title': request.form.get('title'),
                      'publisher': request.form.get('publisher'),
                      'epub_url': book_location
                      }

        book = Book.book_from_dict(**book_data)
        db.session.add(book)
        db.session.commit()

        print book
        return render_template('add_book.html', author=app_user.author)

    return redirect(url_for('index'))

