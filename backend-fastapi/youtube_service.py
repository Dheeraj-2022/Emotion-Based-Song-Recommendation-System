import os
import requests
from typing import List
from dotenv import load_dotenv

load_dotenv()

class YouTubeService:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.base_url = "https://www.googleapis.com/youtube/v3"
    
    def search_music(self, emotion: str, language: str, singer: str = None) -> List[str]:
        """Search for music recommendations on YouTube"""
        # Build search query
        query_parts = [language, emotion, "songs"]
        if singer:
            query_parts.append(singer)
        
        search_query = " ".join(query_parts)
        
        # If no API key, return mock data
        if not self.api_key or self.api_key == "your_youtube_api_key_here":
            return self._get_mock_recommendations(emotion)
        
        try:
            # YouTube API search
            params = {
                "part": "snippet",
                "q": search_query,
                "type": "video",
                "videoCategoryId": "10",  # Music category
                "maxResults": 10,
                "key": self.api_key
            }
            
            response = requests.get(f"{self.base_url}/search", params=params)
            response.raise_for_status()
            
            data = response.json()
            recommendations = []
            
            for item in data.get("items", []):
                title = item["snippet"]["title"]
                video_id = item["id"]["videoId"]
                url = f"https://www.youtube.com/watch?v={video_id}"
                recommendations.append(f"{title} - {url}")
            
            return recommendations
            
        except Exception as e:
            print(f"YouTube API error: {e}")
            return self._get_mock_recommendations(emotion)
    
    def _get_mock_recommendations(self, emotion: str) -> List[str]:
        """Return mock recommendations when API is not available"""
        mock_data = {
            "happy": [
                "Happy - Pharrell Williams",
                "Can't Stop the Feeling - Justin Timberlake",
                "Good Time - Owl City & Carly Rae Jepsen"
            ],
            "sad": [
                "Someone Like You - Adele",
                "Fix You - Coldplay",
                "Mad World - Gary Jules"
            ],
            "angry": [
                "Break Stuff - Limp Bizkit",
                "Bodies - Drowning Pool",
                "Down with the Sickness - Disturbed"
            ],
            "neutral": [
                "Breathe - Pink Floyd",
                "Mad World - Tears for Fears",
                "Imagine - John Lennon"
            ]
        }
        
        return mock_data.get(emotion, mock_data["neutral"])