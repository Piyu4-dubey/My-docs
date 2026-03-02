from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel

app = FastAPI(title="IT Support System")

# ----------------------------------
# MySQL Database Setup
# ----------------------------------
DATABASE_URL = "mysql+pymysql://root:root@localhost/it_support.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# ----------------------------------
# Database Model (Must Match MySQL Table Exactly)
# ----------------------------------

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, nullable=False)
    user_name = Column(String(45), nullable=False)
    user_email = Column(String(255), nullable=False, unique=True)
    user_password = Column(String(100), nullable=False)

# ----------------------------------
# Pydantic Models
# ----------------------------------

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role_id: int


class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    role_id: int

    class Config:
        from_attributes = True

# ----------------------------------
# Dependency
# ----------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------------------
# Routes
# ----------------------------------

@app.get("/")
def hello():
    return {"message": "Welcome user!"}


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(
        user_id=user.user_id,
        name=user.user_name,
        email=user.user_email,
        role_id=user.role_id
    )


@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.user_email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        user_name=user.name,
        user_email=user.email,
        user_password=user.password,
        role_id=user.role_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse(
        user_id=new_user.user_id,
        name=new_user.user_name,
        email=new_user.user_email,
        role_id=new_user.role_id
    )