from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from api import models
from api import create_app
from api.models import db

app = create_app('production')

migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()