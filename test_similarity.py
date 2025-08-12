#!/usr/bin/env python3
"""
유사도 계산 테스트 스크립트
"""

import asyncio
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.faq_service import FAQService

async def test_similarity():
    """유사도 계산 테스트"""
    
    # FAQ 서비스 초기화
    faq_service = FAQService("football")
    
    # 테스트 쿼리들
    test_queries = [
        "番号の入れる場所を、個々で変更は可能？",
        "番号の入れる場所を、個々で変更は可能でしょうか",
        "背番号の配置場所を個別で変更できますか？",
        "番号の位置を個々で変更可能でしょうか"
    ]
    
    for query in test_queries:
        print(f"\n=== 테스트 쿼리: {query} ===")
        
        # FAQ 검색 실행
        results = await faq_service.search_faq(query, threshold=0.5)
        
        if results:
            best_match = results[0]
            print(f"FAQ 질문: {best_match['question']}")
            print(f"유사도: {best_match['similarity']:.3f}")
            print(f"답변: {best_match['answer'][:100]}...")
        else:
            print("매칭되는 FAQ 없음")

if __name__ == "__main__":
    asyncio.run(test_similarity())
