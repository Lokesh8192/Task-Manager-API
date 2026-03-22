from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base
from app.core.enums import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, unique=True, nullable=True, index=True)
    username = Column(String, unique=True, nullable=True, index=True)
    password = Column(String, nullable=False)
    role = Column(String, default=UserRole.user.value)
    created_at = Column(DateTime, default=datetime.utcnow)

