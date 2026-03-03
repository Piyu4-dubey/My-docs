from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

# ── Password Hashing ─────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compare plain text password against stored bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:                         # ✅ Fixed: was named hashed_password (confusing)
    """Hash a plain text password using bcrypt."""
    return pwd_context.hash(password)


# ── JWT Token ────────────────────────────────────────────────
SECRET_KEY = "c6374779a38ba4fb2c1ec389e5e2b492238bee9eac4564b583f546d5890c0b45"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_token(data: dict) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # ✅ Fixed: utcnow() is deprecated
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)