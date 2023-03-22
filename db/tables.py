from sqlalchemy import MetaData, Integer, String, Column, DateTime
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from datetime import datetime

metadata = MetaData()
Base: DeclarativeMeta = declarative_base(metadata=metadata)


class Articles(Base):
    __tablename__="Articles"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    intro = Column(String, nullable=False)
    text = Column(String, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)

