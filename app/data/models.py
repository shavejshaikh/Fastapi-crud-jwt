from app.data.database import Base
from sqlalchemy import String, DateTime, Column, Integer


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    added_on = Column(DateTime(timezone=True))
    update_on = Column(DateTime(timezone=True), default=None)

