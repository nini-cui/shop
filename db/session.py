from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:postpass@localhost:5332/shop"

engine = create_engine(DATABASE_URL)

db_session = sessionmaker(bind=engine, autoflush=False, autocommit=False)