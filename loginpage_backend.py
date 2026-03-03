from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database_connect import get_db, engine    # ✅ DB session + engine from one place
from models import User                         # ✅ Single User model (fixed column names)
from schemas import UserCreate, UserResponse, LoginRequest
from security import verify_password, hash_password, create_token  # ✅ Uses bcrypt now

import models
models.Base.metadata.create_all(bind=engine)   # ✅ Auto-creates tables if they don't exist

# ── App Setup ────────────────────────────────────────────────
app = FastAPI(title="IT Support System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Routes ───────────────────────────────────────────────────

@app.get("/")
def hello():
    return {"message": "IT Support Help Desk API is running!"}


# REGISTER
@app.post("/users/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check duplicate email
    existing = db.query(User).filter(User.user_email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # ✅ Hash password before saving
    new_user = User(
        user_name=user.name,
        user_email=user.email,
        user_password=hash_password(user.password),   # ✅ bcrypt hash stored
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


# LOGIN
@app.post("/login/", response_model=UserResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_email == credentials.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ Verify with bcrypt — not plain text comparison
    if not verify_password(credentials.password, user.user_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    # ✅ Generate JWT token (returned in response for future use)
    token = create_token(data={"sub": user.user_email})
    print(f"[INFO] Token for {user.user_email}: {token}")   # Optional: remove in production

    return UserResponse(
        user_id=user.user_id,
        name=user.user_name,
        email=user.user_email,
        role_id=user.role_id
    )


# GET USER BY ID
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