# Libs
from migrate.versioning import api
import os

# Our Imports
from application import app, create_app, db
from core import DevConfig
from test.db_bootstrap import bootstrapTestDB

create_app('core.DevConfig')

if not os.path.isfile("dev.db"):
    print "dev.db not found, creating..."
    with app.app_context():
        db.create_all()
        bootstrapTestDB(db)

if not os.path.exists(DevConfig.SQLALCHEMY_MIGRATE_REPO):
    api.create(DevConfig.SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(DevConfig.SQLALCHEMY_DATABASE_URI, DevConfig.SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(DevConfig.SQLALCHEMY_DATABASE_URI,
                        DevConfig.SQLALCHEMY_MIGRATE_REPO,
                        api.version(DevConfig.SQLALCHEMY_MIGRATE_REPO))
