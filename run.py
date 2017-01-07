from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from flask_restful import Api

from app import app, db
from app.auth.controllers import Index, Register, Login


manager = Manager(app)
migrate = Migrate(app, db)
api = Api(app, prefix="/api/v1")

api.add_resource(Index, "/", endpoint="home")
api.add_resource(Register, "/register", endpoint="register")
api.add_resource(Login, "/login", endpoint="login")

def make_shell_context():
    """
    Returns application and database instances
    to the shell importing them automatically
    on `python manager.py shell`.
    """
    return dict(app=app, api=api, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
