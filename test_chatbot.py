#!/usr/bin/env python3
"""
스포츠 챗봇 테스트 스크립트
"""

import asyncio
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.chat_models import SportsChatbot
from app.services.sports_service import SportsService

async def test_chatbot():
    """챗봇 테스트"""
    print("🏈 스포츠 챗봇 테스트 시작\n")
    
    # 스포츠별 테스트
    sports = ["baseball", "football", "basketball"]
    
    for sport in sports:
        print(f"=== {sport.upper()} 챗봇 테스트 ===")
        
        # 챗봇 초기화
        chatbot = SportsChatbot(sport)
        sports_service = SportsService(sport)
        
        # 테스트 메시지들
        test_messages = [
            "안녕하세요",
            "경기 일정 알려줘",
            "팀 순위는 어떻게 되나요?",
            "최신 뉴스 알려줘",
            "도움말"
        ]
        
        for message in test_messages:
            print(f"\n사용자: {message}")
            
            try:
                # 특정 키워드 처리 테스트
                if "일정" in message or "경기" in message:
                    schedules = sports_service.get_schedule_data()
                    response = sports_service.format_schedule_message(schedules)
                elif "순위" in message or "랭킹" in message:
                    rankings = sports_service.get_ranking_data()
                    response = sports_service.format_ranking_message(rankings)
                elif "뉴스" in message or "소식" in message:
                    news = sports_service.get_news_data()
                    response = sports_service.format_news_message(news)
                elif "도움말" in message:
                    response = f"{sport} 챗봇 도움말입니다."
                else:
                    # LangChain 챗봇 응답
                    response = await chatbot.get_response(message)
                
                print(f"챗봇: {response}")
                
            except Exception as e:
                print(f"오류: {str(e)}")
        
        print("\n" + "="*50 + "\n")

def main():
    """메인 함수"""
    try:
        asyncio.run(test_chatbot())
        print("✅ 테스트 완료!")
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    main() 