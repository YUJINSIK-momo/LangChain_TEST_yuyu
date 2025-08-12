#!/usr/bin/env python3
"""
FAQ + AI 조합 개선 테스트 스크립트
"""

import asyncio
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import process_message
from app.services.sports_service import SportsService

async def test_faq_ai_combination():
    """FAQ + AI 조합 개선 테스트"""
    
    # 스포츠 서비스 초기화
    sports_service = SportsService("football")
    
    # 테스트 쿼리들 (다양한 유사도 레벨)
    test_queries = [
        "番号の入れる場所を、個々で変更は可能？",  # 유사도 1.00 (FAQ만)
        "番号の配置について教えて",  # 유사도 낮음 (AI 우선)
        "背番号の位置変更は可能でしょうか",  # 유사도 높음 (FAQ만)
        "ユニフォームのデザインについて"  # 유사도 낮음 (AI 우선)
    ]
    
    for query in test_queries:
        print(f"\n=== 테스트 쿼리: {query} ===")
        
        # 메시지 처리 실행
        response = await process_message("football", query, sports_service)
        
        print(f"응답 타입: {type(response)}")
        if isinstance(response, dict):
            print(f"응답 길이: {len(response.get('text', ''))} 문자")
            print(f"응답 내용: {response.get('text', '')[:200]}...")
        else:
            print(f"응답 길이: {len(response)} 문자")
            print(f"응답 내용: {response[:200]}...")

if __name__ == "__main__":
    asyncio.run(test_faq_ai_combination())
