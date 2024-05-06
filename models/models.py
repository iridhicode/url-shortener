from sqlalchemy import Column, Integer, String
from db.database import Base


class URLs(Base):
    __tablename__ = "url-shortener-db"

    id = Column(Integer, primary_key=True, index=True)
    short_id = Column(String, unique=True, index=True)
    long_url = Column(String, index=True)
