from book_routes import book_routes
from author_routes import author_routes
from auth_routes import auth_routes
from user_routes import user_routes

futurepress_blueprints = [ book_routes, author_routes,
                           auth_routes, user_routes ]