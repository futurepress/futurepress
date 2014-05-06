
from migrate.versioning import api
import os

from core import AWSConfig
from application import app, create_app, db
from test.db_bootstrap import bootstrapTestDB

create_app('core.AWSConfig')

with app.app_context():
    db.create_all()

application = app