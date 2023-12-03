from sqlalchemy import Column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class Tracker(Base):
    __tablename__ = 'trackers'
