from sqlalchemy import MetaData, Table, Integer, String, TIMESTAMP, ForeignKey, Column, DateTime, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

metadata = MetaData()
Base: DeclarativeMeta = declarative_base(metadata=metadata)


class Articles(Base):
    __tablename__="Articles"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    intro = Column(String, nullable=False)
    text = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)

