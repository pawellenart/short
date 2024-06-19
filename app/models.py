from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class URL(Base):
    __tablename__ = "urls"

    shortkey = Column(String(255), primary_key=True, index=True)
    url = Column(Text, nullable=False)
    title = Column(Text, nullable=True)
    counter = Column(Integer, default=0)
    date_created = Column(DateTime, server_default=func.now())


class Options(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, autoincrement=True)
    options_key = Column(String(255), index=True, nullable=False)
    options_value = Column(Text, nullable=False)


class ApiKey(Base):
    __tablename__ = "api_keys"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    api_key = Column(String(128), unique=True, index=True, nullable=False)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
