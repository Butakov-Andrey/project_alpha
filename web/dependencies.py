from postgres_db import SessionLocal


# database dependency
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
