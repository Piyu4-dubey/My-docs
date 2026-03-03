from database_connect import Base          # ✅ Fixed: was "from mysql import Base" (wrong module)
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "users"

    user_id   = Column(Integer, primary_key=True, index=True)   # ✅ Renamed to match backend & DB schema
    user_name = Column(String(100), nullable=False)
    user_email= Column(String(100), unique=True, index=True, nullable=False)
    user_password = Column(String(255), nullable=False)          # stores bcrypt hash
    dept_id   = Column(Integer, nullable=True)
    role_id   = Column(Integer, nullable=False)