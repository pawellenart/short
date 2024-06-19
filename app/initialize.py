from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database import Base, SQLALCHEMY_DATABASE_URL
from app.models import URL, Options, ApiKey  # Ensure models are imported
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def initialize():
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        # Generate the database schema
        print("Creating database schema...")
        Base.metadata.create_all(bind=engine)
        print("Database schema created successfully.")

        db.close()
    except Exception as e:
        print(f"Error during initialization: {e}")


if __name__ == "__main__":
    initialize()
