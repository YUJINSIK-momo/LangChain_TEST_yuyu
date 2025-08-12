#!/usr/bin/env python3
"""
일본어 LLM 처리 테스트 스크립트
"""

import asyncio
import json
import requests

async def test_japanese_llm():
    """일본어 LLM 처리 테스트"""
    
    # 일본어 테스트 메시지들
    test_messages = [
        "サッカーウェアのカスタム制作について教えてください",
        "ユニフォームの価格はいくらですか？",
        "キーパーウェアも作れますか？",
        "チームウェアの制作期間はどのくらいですか？",
        "素材の種類を教えてください"
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
                print(f"응답: {result['response'][:300]}...")
            else:
                print(f"오류: {response.status_code}")
                
        except Exception as e:
            print(f"요청 실패: {e}")
        
        await asyncio.sleep(2)  # 잠시 대기

if __name__ == "__main__":
    asyncio.run(test_japanese_llm())
