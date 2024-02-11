from app.database import Base
from sqlalchemy import Boolean, Column, Integer, String


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    token = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
