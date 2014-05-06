
from migrate.versioning import api

from core import AWSConfig
from application import app, create_app


create_app('core.AWSConfig')

if not os.path.isfile("aws.db"):
    print "aws.db not found, creating..."
    with app.app_context():
        db.create_all()
        bootstrapTestDB(db)

#api.upgrade(AWSConfig.SQLALCHEMY_DATABASE_URI, AWSConfig.SQLALCHEMY_MIGRATE_REPO)
#print 'Current database version: ' + str(api.db_version(DevConfig.SQLALCHEMY_DATABASE_URI, DevConfig.SQLALCHEMY_MIGRATE_REPO))