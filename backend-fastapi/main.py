from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import uvicorn

from database import engine, SessionLocal
import models
import schemas
import crud
import auth
from emotion_detector import EmotionDetector
from youtube_service import YouTubeService

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Emotion Music API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
emotion_detector = EmotionDetector()
youtube_service = YouTubeService()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Emotion Music Recommender API"}

@app.post("/api/emotions/detect", response_model=schemas.EmotionDetectionResponse)
async def detect_emotion(request: schemas.EmotionDetectionRequest):
    """Detect emotion from base64 encoded image"""
    try:
        emotion = emotion_detector.detect(request.image)
        return {"emotion": emotion}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/emotions/save", response_model=schemas.EmotionData)
def save_emotion(
    emotion_data: schemas.EmotionCreate,
    db: Session = Depends(get_db)
):
    """Save emotion detection to history"""
    return crud.create_emotion(db=db, emotion=emotion_data)

@app.get("/api/emotions/history/{user_id}", response_model=List[schemas.EmotionData])
def get_emotion_history(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get emotion history for a user"""
    emotions = crud.get_user_emotions(db, user_id=user_id, skip=skip, limit=limit)
    return emotions

@app.post("/api/emotions/recommend", response_model=schemas.RecommendationResponse)
async def get_recommendations(request: schemas.RecommendationRequest):
    """Get music recommendations based on emotion"""
    try:
        recommendations = youtube_service.search_music(
            emotion=request.emotion,
            language=request.language,
            singer=request.singer
        )
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/emotions/stats/{user_id}", response_model=schemas.EmotionStats)
def get_emotion_stats(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get emotion statistics for a user"""
    return crud.get_emotion_stats(db, user_id=user_id)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)