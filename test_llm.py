#!/usr/bin/env python3
"""
LLM 처리 테스트 스크립트
"""

import asyncio
import json
import requests

async def test_llm_processing():
    """LLM 처리 테스트"""
    
    # 테스트 메시지들
    test_messages = [
        "番号の入れる場所を、個々で変更は可能でしょうか",  # FAQ와 정확히 일치
        "축구 유니폼에 대해 알려주세요",  # 일반적인 질문
        "키퍼 유니폼도 만들 수 있나요?",  # FAQ와 유사한 질문
        "축구 경기 일정은 언제인가요?"  # 특정 키워드
    ]
    
    for message in test_messages:
        print(f"\n=== 테스트 메시지: {message} ===")
        
        try:
            response = requests.post(
                "http://localhost:8000/chat/football",
                json={"message": message},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"응답: {result['response'][:200]}...")
            else:
                print(f"오류: {response.status_code}")
                
        except Exception as e:
            print(f"요청 실패: {e}")
        
        await asyncio.sleep(1)  # 잠시 대기

if __name__ == "__main__":
    asyncio.run(test_llm_processing())
