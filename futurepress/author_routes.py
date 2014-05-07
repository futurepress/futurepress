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
from models import ( Author, AppUser, Book, BookUploader, Genre, stormpathUserHash )
from settings import CLOUDFRONTURL

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

@author_routes.route('/author_settings/', methods=['GET', 'POST'])
@login_required
def settings():

    user_id = user.get_id()
    app_user = AppUser.query.get(stormpathUserHash(user_id))

    if request.method == 'GET':
        return render_template('author_settings.html', author=app_user.author)

    if not app_user.is_author:
        author = Author.author_from_dict(**request.form.to_dict())
        db.session.add(author)
        db.session.commit()
        app_user.become_author(author)

    return render_template('author_settings.html', author=app_user.author)


@author_routes.route('/dashboard/')
@login_required
def author_dashboard():
    user_id = user.get_id()
    app_user = AppUser.query.get(stormpathUserHash(user_id))

    if app_user.is_author:
        return render_template('author_dashboard.html', author=app_user.author)

@author_routes.route('/dashboard/add', methods=['GET', 'POST'])
@login_required
def add_book():
    user_id = user.get_id()
    app_user = AppUser.query.get(stormpathUserHash(user_id))

    if app_user.is_author:
        if request.method == 'GET':
            return render_template('add_book.html', author=app_user.author)

        book_file = request.files.get('epub_file', None)
        cover_file = request.files.get('cover_file', None)

        # POST is a epub file upload
        if book_file.content_type == 'application/epub+zip' or book_file.content_type == 'application/octet-stream':
            book_upload = BookUploader(book_file.filename, book_file, cover_file)
            epub_url = CLOUDFRONTURL + book_upload.epub_key
            cover_url = CLOUDFRONTURL + book_upload.cover_key

        genres = []
        for g in request.form.get('genres').split(','):
            genre_name = g.strip().title()
            if not genre_name.isspace():
                genre = Genre.query.filter_by(name=genre_name).first()
                if not genre:
                    genre = Genre(genre_name)
                    db.session.add(genre)
                genres.append(genre)

        book_data = {
                      'author': app_user.author,
                      'isbn': request.form.get('isbn'),
                      'title': request.form.get('title'),
                      'publisher': request.form.get('publisher'),
                      'genres': genres,
                      'epub_url': epub_url,
                      'cover_large': cover_url
                      }

        book = Book.book_from_dict(**book_data)
        db.session.add(book)
        db.session.commit()

        return redirect(url_for('author_routes.author_dashboard'))

    return redirect(url_for('index'))

@author_routes.route('/dashboard/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    user_id = user.get_id()
    app_user = AppUser.query.get(stormpathUserHash(user_id))
    book = Book.query.get(book_id)

    if book in app_user.author.books:
        if request.method == 'GET':
            return render_template('edit_book.html', book=book)

        genres = []
        for g in request.form.get('genres').split(','):
            genre_name = g.strip().title()
            if not genre_name.isspace():
                genre = Genre.query.filter_by(name=genre_name).first()
                if not genre:
                    genre = Genre(genre_name)
                    db.session.add(genre)
                genres.append(genre)

        book.genres = genres
        book.title = request.form.get('title'),
        book.isbn = request.form.get('isbn'),
        book.publisher = request.form.get('publisher'),
        db.session.add(book)

        db.session.commit()

        return redirect(url_for('author_routes.author_dashboard'))

    return redirect(url_for('index'))
