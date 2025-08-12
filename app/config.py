import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    """애플리케이션 설정 클래스"""
    
    # Google Gemini 설정
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # LINE Bot 설정
    LINE_CHANNEL_ACCESS_TOKEN_BASEBALL = os.getenv("LINE_CHANNEL_ACCESS_TOKEN_BASEBALL")
    LINE_CHANNEL_ACCESS_TOKEN_FOOTBALL = os.getenv("LINE_CHANNEL_ACCESS_TOKEN_FOOTBALL")
    LINE_CHANNEL_ACCESS_TOKEN_BASKETBALL = os.getenv("LINE_CHANNEL_ACCESS_TOKEN_BASKETBALL")
    
    LINE_CHANNEL_SECRET_BASEBALL = os.getenv("LINE_CHANNEL_SECRET_BASEBALL")
    LINE_CHANNEL_SECRET_FOOTBALL = os.getenv("LINE_CHANNEL_SECRET_FOOTBALL")
    LINE_CHANNEL_SECRET_BASKETBALL = os.getenv("LINE_CHANNEL_SECRET_BASKETBALL")
    
    # 데이터베이스 설정
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sports_chatbot.db")
    
    # 로그 설정
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # 스포츠별 설정
    SPORTS_CONFIG = {
        "baseball": {
            "name": "야구",
            "line_token": LINE_CHANNEL_ACCESS_TOKEN_BASEBALL,
            "line_secret": LINE_CHANNEL_SECRET_BASEBALL,
            "data_path": "data/baseball"
        },
        "football": {
            "name": "축구", 
            "line_token": LINE_CHANNEL_ACCESS_TOKEN_FOOTBALL,
            "line_secret": LINE_CHANNEL_SECRET_FOOTBALL,
            "data_path": "data/football"
        },
        "basketball": {
            "name": "농구",
            "line_token": LINE_CHANNEL_ACCESS_TOKEN_BASKETBALL,
            "line_secret": LINE_CHANNEL_SECRET_BASKETBALL,
            "data_path": "data/basketball"
        }
    } 