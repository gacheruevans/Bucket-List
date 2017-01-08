import passlib
from app import db
from datetime import datetime
from sqlalchemy_utils import PasswordType


class Base(db.Model):
    """
    Base model for other database tables to inherit
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(
        timezone=True), default=datetime.utcnow())
    date_modified = db.Column(db.DateTime(timezone=True), nullable=True)


class Users(Base):
    """
    This class contains the database schema of the auth_user
    i.e. Table and Columns
    """

    __tablename__ = 'auth_user'

    username = db.Column(db.String(128), nullable=False, unique=True)
    # Identification Data: email & password
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(192), nullable=False)
    password = db.Column(PasswordType(onload=lambda **kwargs: dict(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],
        deprecated=['md5_crypt'],
        **kwargs
    ), ), unique=False, nullable=False)

    def verify_password(self, password):
        """
        Function to verify the password of a user
        """

        return self.password == password

    def __repr__(self):
        return '<User %r>' % (self.username)
