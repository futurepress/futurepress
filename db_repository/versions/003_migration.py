from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
app_users = Table('app_users', post_meta,
    Column('user_id', String, primary_key=True, nullable=False),
    Column('user_href', String, nullable=False),
    Column('is_author', Boolean, nullable=False),
    Column('test_column', String),
    Column('test_column2', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['app_users'].columns['test_column2'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['app_users'].columns['test_column2'].drop()
