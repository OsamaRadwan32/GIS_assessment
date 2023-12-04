from sqlalchemy import inspect
from datetime import datetime
from flask_validator import ValidateString, ValidateInteger
from sqlalchemy.orm import validates

from .. import db # from __init__.py

from .users_models import User

# ----------------------------------------------- #

# SQL Datatype Objects => https://docs.sqlalchemy.org/en/14/core/types.html
class Table(db.Model):
    __tablename__ = 'tables'

# Auto Generated Fields:
    id           = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    created      = db.Column(db.DateTime(timezone=True), default=datetime.now)                           
    updated      = db.Column(db.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

# Input by User Fields:
    name         = db.Column(db.String(100), nullable=False, unique=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    structure    = db.Column(db.JSONB, nullable=False)
    user         = db.relationship('User', backref='users', lazy=True)


# Validations => https://flask-validator.readthedocs.io/en/latest/index.html
    @classmethod
    def __declare_last__(cls):
        ValidateString(Table.name, True, True, "Table name type must be string")
        ValidateInteger(Table.user_id, True, True, "User id is not valid")

# How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

    def __repr__(self):
        return "<%r>" % self.email
