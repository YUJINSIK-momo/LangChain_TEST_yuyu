import aiohttp
import json
import logging
from typing import Dict, Any
from app.config import Config

logger = logging.getLogger(__name__)

class LineService:
    """LINE Bot API 서비스 클래스"""
    
    def __init__(self, sport_type: str):
        self.sport_type = sport_type
        self.sport_config = Config.SPORTS_CONFIG[sport_type]
        self.channel_access_token = self.sport_config["line_token"]
        self.channel_secret = self.sport_config["line_secret"]
        self.base_url = "https://api.line.me/v2"
    
    async def send_text_message(self, user_id: str, message: str) -> bool:
        """텍스트 메시지 전송"""
        try:
            url = f"{self.base_url}/bot/message/push"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.channel_access_token}"
            }
            
            data = {
                "to": user_id,
                "messages": [
                    {
                        "type": "text",
                        "text": message
                    }
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        logger.info(f"{self.sport_type} LINE 메시지 전송 성공: {user_id}")
                        return True
                    else:
                        logger.error(f"{self.sport_type} LINE 메시지 전송 실패: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"{self.sport_type} LINE 메시지 전송 중 오류: {str(e)}")
            return False
    
    async def send_image_message(self, user_id: str, image_url: str, preview_url: str = None) -> bool:
        """이미지 메시지 전송"""
        try:
            url = f"{self.base_url}/bot/message/push"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.channel_access_token}"
            }
            
            data = {
                "to": user_id,
                "messages": [
                    {
                        "type": "image",
                        "originalContentUrl": image_url,
                        "previewImageUrl": preview_url or image_url
                    }
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        logger.info(f"{self.sport_type} LINE 이미지 메시지 전송 성공: {user_id}")
                        return True
                    else:
                        logger.error(f"{self.sport_type} LINE 이미지 메시지 전송 실패: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"{self.sport_type} LINE 이미지 메시지 전송 중 오류: {str(e)}")
            return False
    
    async def send_multiple_messages(self, user_id: str, messages: list) -> bool:
        """여러 메시지 전송 (텍스트 + 이미지 등)"""
        try:
            url = f"{self.base_url}/bot/message/push"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.channel_access_token}"
            }
            
            data = {
                "to": user_id,
                "messages": messages
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        logger.info(f"{self.sport_type} LINE 다중 메시지 전송 성공: {user_id}")
                        return True
                    else:
                        logger.error(f"{self.sport_type} LINE 다중 메시지 전송 실패: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"{self.sport_type} LINE 다중 메시지 전송 중 오류: {str(e)}")
            return False
    
    async def send_flex_message(self, user_id: str, flex_content: Dict[str, Any]) -> bool:
        """Flex 메시지 전송 (리치 메뉴, 카드 등)"""
        try:
            url = f"{self.base_url}/bot/message/push"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.channel_access_token}"
            }
            
            data = {
                "to": user_id,
                "messages": [
                    {
                        "type": "flex",
                        "altText": "스포츠 정보",
                        "contents": flex_content
                    }
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        logger.info(f"{self.sport_type} LINE Flex 메시지 전송 성공: {user_id}")
                        return True
                    else:
                        logger.error(f"{self.sport_type} LINE Flex 메시지 전송 실패: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"{self.sport_type} LINE Flex 메시지 전송 중 오류: {str(e)}")
            return False
    
    def create_sports_menu_flex(self, sport_name: str) -> Dict[str, Any]:
        """스포츠 메뉴 Flex 메시지 생성"""
        return {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{sport_name} 정보",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#ffffff"
                    }
                ],
                "backgroundColor": "#27AE60"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "경기 일정",
                            "text": f"{sport_name} 경기 일정 알려줘"
                        },
                        "style": "primary",
                        "color": "#27AE60"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "팀 순위",
                            "text": f"{sport_name} 팀 순위 알려줘"
                        },
                        "style": "primary",
                        "color": "#27AE60"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "최신 뉴스",
                            "text": f"{sport_name} 최신 뉴스 알려줘"
                        },
                        "style": "primary",
                        "color": "#27AE60"
                    }
                ],
                "spacing": "md"
            }
        } 