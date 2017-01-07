import os

from flask_testing import TestCase
from run import app
from config import base_dir

class globalTest(TestCase):
    """
    This is the global test case class that creates the testing app
    that is used in all test within the application
    """

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(base_dir, 'ndoo.db')
        app.config['TESTING'] = True
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        return app
