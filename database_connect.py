from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ✅ SQLAlchemy connection (used by FastAPI/SQLAlchemy ORM)
DATABASE_URL = "mysql+pymysql://root:root@localhost/it_support"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency — inject DB session into routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()