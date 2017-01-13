from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from flask_restful import Api

from app import app, db
from app.auth.controllers import Register, Login
from app.bucketlist.controllers import (Bucketlists,
                                        OneBucketlist,
                                        BucketlistItem,
                                        OneBucketListItem)

manager = Manager(app)
migrate = Migrate(app, db)
api = Api(app, prefix="/api/v1")

api.add_resource(Login, "/auth/login", endpoint="login")

api.add_resource(Register, "/auth/register", endpoint="register")

api.add_resource(Bucketlists, "/bucketlists", endpoint="bucketlist")

api.add_resource(OneBucketlist, "/bucketlists/<bucketlists_id>",
                 endpoint="onebucketlist")

api.add_resource(BucketlistItem, "/bucketlists/<bucketlists_id>/items",
                 endpoint="items")

api.add_resource(OneBucketListItem,
                 "/bucketlists/<bucketlists_id>/items/<item_id>",
                 endpoint="oneitem")


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
