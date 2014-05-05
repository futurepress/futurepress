__author__ = 'ajrenold'

# Lib Imports
from flask import ( request, session, g,
                    redirect, url_for, abort,
                    render_template, flash, jsonify,
                    make_response, Blueprint
                )
from werkzeug.contrib.atom import AtomFeed, FeedEntry

# Our Imports
from models import ( Book, Genre )


book_routes = Blueprint('book_routes', __name__,
                        template_folder='templates')

@book_routes.route('/book/<int:book_id>')
def bookpage(book_id):
    if book_id:
        book = Book.query.get(book_id)
        if book:
            #return jsonify(book.as_dict())
            return render_template('bookpage.html', book=book)
    return redirect(url_for('index'))

@book_routes.route('/book/<int:book_id>.atom')
def bookatom(book_id):
    book = Book.query.get(book_id)
    entry = FeedEntry(book.title,
             author=book.author.as_dict(),
             id=url_for('book_routes.bookpage',book_id=book.book_id, _external=True),
             updated=book.last_updated,
             published=book.published,
             links=[
                 {'type': "image/jpeg",
                  'rel': "http://opds-spec.org/image",
                  'href': book.cover_large},
                 {'type': "image/jpeg",
                  'rel': "http://opds-spec.org/image/thumbnail",
                  'href': book.cover_thumb},
                 {'type': "application/epub+zip",
                  'rel': "http://opds-spec.org/acquisition",
                  'href': book.epub_url},
                 {'type': "application/atom+xml;type=entry;profile=opds-catalog",
                  'rel': "alternate",
                  'href': url_for('book_routes.bookpage', book_id=book.book_id, _external=True)},
             ]
    )
    response = make_response('<?xml version="1.0" encoding="UTF-8"?>\n'+
                             ''.join([ el for el in entry.generate() ]))
    response.headers['Content-Type'] = 'application/atom+xml'
    return response

@book_routes.route('/catalog.atom')
def catalog():
    feed = AtomFeed('FuturePress Catalog',
                    feed_url=request.url,
                    subtitle="FuturePress' full catalog")

    books = Book.query.all()
    for book in books:
        feed.add(book.title,
             author=book.author.as_dict(),
             id=url_for('book_routes.bookpage',book_id=book.book_id, _external=True),
             updated=book.last_updated,
             published=book.published,
             links=[
                 {'type': "image/jpeg",
                  'rel': "http://opds-spec.org/image",
                  'href': book.cover_large},
                 {'type': "image/jpeg",
                  'rel': "http://opds-spec.org/image/thumbnail",
                  'href': book.cover_thumb},
                 {'type': "application/epub+zip",
                  'rel': "http://opds-spec.org/acquisition",
                  'href': book.epub_url},
                 {'type': "application/atom+xml;type=entry;profile=opds-catalog",
                  'rel': "alternate",
                  'href': url_for('book_routes.bookatom', book_id=book.book_id, _external=True)},
             ]
        )

    return feed.get_response()

@book_routes.route('/genre/<genre_slug>')
def genrepage(genre_slug):
    if genre_slug:
        genre = Genre.query.filter_by(slug=genre_slug).first()
        if genre:
            #return jsonify(author.as_dict())
            return render_template('genrepage.html', genre=genre)
    return redirect(url_for('index'))