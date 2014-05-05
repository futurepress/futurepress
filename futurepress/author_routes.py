__author__ = 'ajrenold'

__author__ = 'ajrenold'

# Lib Imports
from flask import (
                    redirect, url_for, abort,
                    render_template,
                    Blueprint
                )

# Our Imports
from models import ( Author )


author_routes = Blueprint('author_routes', __name__,
                        template_folder='templates')

@author_routes.route('/author/<author_slug>')
def authorpage(author_slug):
    if author_slug:
        author = Author.query.filter_by(slug=author_slug).first()
        if author:
            #return jsonify(author.as_dict())
            return render_template('authorpage.html', author=author)
    return redirect(url_for('.index'))