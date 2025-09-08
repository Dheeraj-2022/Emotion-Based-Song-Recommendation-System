from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Emotion(Base):
    __tablename__ = "emotions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    emotion = Column(String(50), nullable=False)
    confidence = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)
    language = Column(String(50))
    singer = Column(String(100))
    recommendations = Column(Text)  # JSON string of recommendations
    
    user = relationship("User", back_populates="emotions")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    emotions = relationship("Emotion", back_populates="user")
