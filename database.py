# Import necessary modules from SQLAlchemy for database management
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Define the base class for SQLAlchemy ORM models
Base = declarative_base()

# Define the Contact model which will represent the contacts table in the database
class Contact(Base):
    __tablename__ = 'contacts'  # Name of the table in the database

    # Define columns in the contacts table with appropriate data types and constraints

    # Primary key, unique identifier for each contact entry
    id = Column(Integer, primary_key=True)
    
    # Phone number field, can be null if not provided
    phoneNumber = Column(String, nullable=True)
    
    # Email field, can be null if not provided
    email = Column(String, nullable=True)
    
    # Foreign key linking to another contact's ID (if this contact is linked to a primary contact)
    linkedId = Column(Integer, nullable=True)
    
    # Indicates whether this contact is a primary or secondary entry
    linkPrecedence = Column(String, nullable=False)  # Must be "primary" or "secondary"
    
    # Date and time when the contact was created
    createdAt = Column(DateTime, default=datetime.utcnow)
    
    # Date and time when the contact was last updated; updated automatically on each update
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Date and time when the contact was deleted; null if the contact is active
    deletedAt = Column(DateTime, nullable=True)

# Define the database URL (using SQLite in this case for simplicity)
DATABASE_URL = "sqlite:///./test.db"

# Create the SQLAlchemy engine, responsible for managing database connections
engine = create_engine(DATABASE_URL)

# Create a configured "SessionLocal" class that will be used to create database sessions
# `autocommit=False` prevents automatic commits to allow explicit control over transactions
# `autoflush=False` ensures data is only flushed to the database when explicitly committed
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency that provides a database session to each request
# Ensures that each session is properly closed after use
def get_db():
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Yield the session to be used in the request
    finally:
        db.close()  # Close the session after the request is finished
