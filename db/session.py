from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:postpass@db:5432/shop"

engine = create_engine(DATABASE_URL)

db_session = sessionmaker(bind=engine, autoflush=False, autocommit=False)