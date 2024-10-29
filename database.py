from sqlmodel import create_engine, SQLModel
import os

# Set the path for the database file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current file
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'db', 'database.db')}"  # Path to your SQLite database

# Create the database engine
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    """Create the database and tables on startup."""
    SQLModel.metadata.create_all(engine)
