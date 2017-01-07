# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from datetime import datetime


# Base model for other database tables to inherit
class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(
        timezone=True), default=datetime.utcnow())
    date_modified = db.Column(db.DateTime(timezone=True), nullable=True)

# User model


class Users(Base):

    __tablename__ = 'auth_user'

    # User Name
    username = db.Column(db.String(128), nullable=False)

    # Identification Data: email & password
    email = db.Column(db.String(128), nullable=False,
                      unique=True)
    password = db.Column(db.String(192), nullable=False)

    def __repr__(self):
        return '<User %r>' % (self.username)
