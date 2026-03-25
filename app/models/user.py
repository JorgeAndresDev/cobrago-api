from sqlalchemy import Column, String
from app.database.config import Base
from app.database.mixins import BaseModelMixin

class User(Base, BaseModelMixin):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
