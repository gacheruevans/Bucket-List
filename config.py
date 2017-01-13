import os

# Define the application directory
base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """ 
     Defined database using Sqlite
    """
    SECRET_KEY = '876587326432uyrhietweryoi'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'ndoo.db')


class ProductionConfig(Config):
    """
     This class cofigures the production
     environment properties
    """
    TESTING = True
    DEBUG = False


class StagingConfig(Config):
    """
     This class configures the staging
     environment properties
    """
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    """
     This class configures the development
     environment properties
    """
    DEBUG = True
    TESTING = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class TestingConfig(Config):
    """
     This class cofigures the testing
     environment properties
    """
    TESTING = True

config = {
    'production': ProductionConfig,
    'staging': StagingConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
