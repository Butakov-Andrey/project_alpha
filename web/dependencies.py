from postgres_db import SessionLocal


# database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
