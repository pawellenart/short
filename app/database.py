import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_TYPE = os.getenv("DB_TYPE", "sqlite")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = os.getenv("DB_PORT", "")
DB_NAME = os.getenv("DB_NAME", "")

if DB_TYPE == "sqlite":
    SQLALCHEMY_DATABASE_URL = f"sqlite:///./{DB_NAME}.db"
elif DB_TYPE == "postgres":
    SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{
        DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
elif DB_TYPE == "mysql":
    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{
        DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
elif DB_TYPE == "mariadb":
    SQLALCHEMY_DATABASE_URL = f"mysql+mariadbconnector://{
        DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    raise ValueError(
        "Unsupported DB_TYPE. Use 'sqlite', 'postgres', 'mysql', or 'mariadb'.")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
