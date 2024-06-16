from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class URL(Base):
    __tablename__ = "urls"

    shortkey = Column(String(255), primary_key=True, index=True)
    url = Column(Text, nullable=False)
    title = Column(Text, nullable=True)
    counter = Column(Integer, default=0)


class Options(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, autoincrement=True)
    options_key = Column(String(255), index=True, nullable=False)
    options_value = Column(Text, nullable=False)
