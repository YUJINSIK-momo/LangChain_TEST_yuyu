import logging
import sys
from app.config import Config

def setup_logger():
    """로거 설정"""
    # 로그 레벨 설정
    log_level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)
    
    # 로거 설정
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('sports_chatbot.log', encoding='utf-8')
        ]
    )
    
    # 특정 로거들의 레벨 설정
    logging.getLogger('uvicorn').setLevel(logging.INFO)
    logging.getLogger('aiohttp').setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)

def get_logger(name: str) -> logging.Logger:
    """특정 이름의 로거 반환"""
    return logging.getLogger(name)

# 기본 logger 인스턴스 생성
logger = setup_logger() 