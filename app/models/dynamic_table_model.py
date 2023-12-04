from sqlalchemy import inspect
from datetime import datetime
from flask_validator import ValidateString, ValidateInteger
from sqlalchemy.orm import validates
from sqlalchemy.dialects.postgresql import JSONB

from .. import db # from __init__.py

# ----------------------------------------------- #

# SQL Datatype Objects => https://docs.sqlalchemy.org/en/14/core/types.html
class DynamicTable(db.Model):
    __abstract__ = True
