from sqlmodel import create_engine,Session
import os

# Set the path for the database file
BASE_DIR = os.path.dirname(os.path.abspath(os.getcwd()))  # Get the directory of the current file
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR,'Meta-Agent-with-More-Agents', 'db', 'database.db')}"  # Path to your SQLite database

# Create the database engine
engine = create_engine(DATABASE_URL,echo=False)