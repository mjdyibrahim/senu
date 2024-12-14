from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError
from sqlalchemy.engine.url import make_url
from app.models import Base  # This imports all models

# Update this line with the correct database URL
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/senu"

def create_database():
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    conn.execute(text("commit"))
    try:
        conn.execute(text("CREATE DATABASE senu IF NOT EXIST"))
        print("Database 'senu' created successfully.")
    except ProgrammingError:
        print("Database 'senu' already exists.")
    except SQLAlchemyError as e:
        print(f"An error occurred while creating the database: {e}")
    finally:
        conn.close()

def create_tables():
    try:
        senu_url = make_url(DATABASE_URL).set(database='senu')
        engine = create_engine(str(senu_url))
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully.")
    except SQLAlchemyError as e:
        print(f"An error occurred while creating the tables: {e}")

if __name__ == "__main__":
    create_database()
    create_tables()