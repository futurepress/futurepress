
from migrate.versioning import api
import os

from core import AWSConfig
from application import app, create_app, db
from test.db_bootstrap import bootstrapTestDB

create_app('core.AWSConfig')

if not os.path.isfile("aws.db"):
    print "aws.db not found, creating..."
    with app.app_context():
        db.create_all()
        bootstrapTestDB(db)

application = app