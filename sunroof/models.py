# -*- coding: utf-8 -*-
"""
    sunroof.models
    ~~~~~~~~~

    SQLAlchemy models for Congress tables
"""

from sqlalchemy import Table, Column, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.schema import MetaData

metadata = MetaData()

bills = Table('bills', metadata,
              Column('bill_id', String),
              Column('sponsor_id', String),
              Column('official_title', String),
              Column('document', JSONB))

legislators = Table('legislators', metadata,
                    Column('bioguide_id', String),
                    Column('first_name', String),
                    Column('last_name', String),
                    Column('document', JSONB))
