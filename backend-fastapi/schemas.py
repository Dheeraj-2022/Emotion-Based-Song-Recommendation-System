from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class EmotionDetectionRequest(BaseModel):
    image: str  # Base64 encoded image

class EmotionDetectionResponse(BaseModel):
    emotion: str

class EmotionCreate(BaseModel):
    user_id: int
    emotion: str
    language: Optional[str] = None
    singer: Optional[str] = None

class EmotionData(BaseModel):
    id: int
    user_id: int
    emotion: str
    timestamp: datetime
    language: Optional[str]
    singer: Optional[str]
    recommendations: Optional[str]
    
    class Config:
        from_attributes = True

class RecommendationRequest(BaseModel):
    emotion: str
    language: str
    singer: Optional[str] = None

class RecommendationResponse(BaseModel):
    recommendations: List[str]

class EmotionStats(BaseModel):
    total_detections: int
    most_common_emotion: str
    emotion_distribution: dict
    recent_emotions: List[str]