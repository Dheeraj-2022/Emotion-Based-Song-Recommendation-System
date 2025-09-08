from sqlalchemy.orm import Session
from sqlalchemy import func
import models
import schemas
import json

def create_emotion(db: Session, emotion: schemas.EmotionCreate):
    db_emotion = models.Emotion(
        user_id=emotion.user_id,
        emotion=emotion.emotion,
        language=emotion.language,
        singer=emotion.singer
    )
    db.add(db_emotion)
    db.commit()
    db.refresh(db_emotion)
    return db_emotion

def get_user_emotions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Emotion)\
        .filter(models.Emotion.user_id == user_id)\
        .order_by(models.Emotion.timestamp.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_emotion_stats(db: Session, user_id: int):
    emotions = db.query(models.Emotion)\
        .filter(models.Emotion.user_id == user_id)\
        .all()
    
    if not emotions:
        return {
            "total_detections": 0,
            "most_common_emotion": "None",
            "emotion_distribution": {},
            "recent_emotions": []
        }
    
    # Calculate statistics
    emotion_counts = {}
    for e in emotions:
        emotion_counts[e.emotion] = emotion_counts.get(e.emotion, 0) + 1
    
    most_common = max(emotion_counts, key=emotion_counts.get)
    recent = [e.emotion for e in emotions[:5]]
    
    return {
        "total_detections": len(emotions),
        "most_common_emotion": most_common,
        "emotion_distribution": emotion_counts,
        "recent_emotions": recent
    }