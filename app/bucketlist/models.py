from app import db
from app.auth.models import Base


class Bucketlist(Base):
    """
    This class contains the database schema of the Bucketlist
    i.e. Table and Columns
    """

    __tablename__ = 'bucketlist'

    name = db.Column(db.String(128), nullable=False, unique=True)
    created_by = db.Column(db.Integer, db.ForeignKey(
        'auth_user.id'), nullable=False)
    creator = db.relationship('Users',
                              backref=db.backref('bucketlist',
                                                 lazy='dynamic'))

    def __repr__(self):
        return '<Bucketlist %r>' % (self.name)


class Item(Base):
    """
    This class contains the database schema of the Items
    i.e. Table and Columns
    """

    __tablename__ = 'items'

    name = db.Column(db.String(128), nullable=False)
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))
    bucketlist = db.relationship('Bucketlist',
                                 backref=db.backref('items', lazy='dynamic'))

    def __repr__(self):
        return '<Item %r>' % (self.name)
