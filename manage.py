import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from foodSystem import app, db, models

manager = Manager(app)

@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


if __name__ == '__main__':
    manager.run()