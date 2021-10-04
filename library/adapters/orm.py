from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym

from library.domain import model

metadata = MetaData()

# domain tables will go here
#
#
#
#
#
#########

def map_model_to_tables():
    pass
    # mapping will go here