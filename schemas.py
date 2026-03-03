from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role_id: int


class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    role_id: int

    class Config:
        from_attributes = True  # ✅ Pydantic v2 — allows reading SQLAlchemy ORM objects