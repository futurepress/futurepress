from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
app_users = Table('app_users', pre_meta,
    Column('user_id', VARCHAR, primary_key=True, nullable=False),
    Column('user_href', VARCHAR, nullable=False),
    Column('is_author', BOOLEAN, nullable=False),
    Column('test_column', VARCHAR),
    Column('test_column2', VARCHAR),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['app_users'].columns['test_column'].drop()
    pre_meta.tables['app_users'].columns['test_column2'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['app_users'].columns['test_column'].create()
    pre_meta.tables['app_users'].columns['test_column2'].create()
