#!flask/bin/python
from migrate.versioning import api
from core import DevConfig
api.upgrade(DevConfig.SQLALCHEMY_DATABASE_URI, DevConfig.SQLALCHEMY_MIGRATE_REPO)
print 'Current database version: ' + str(api.db_version(DevConfig.SQLALCHEMY_DATABASE_URI, DevConfig.SQLALCHEMY_MIGRATE_REPO))