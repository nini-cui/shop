from db import session

def get_db():
    db = session.db_session()
    try:
        yield db
    finally:
        db.close()