#!/usr/bin/env python3
"""
서버 로그 확인 스크립트
"""

import time
import requests

def test_with_logging():
    """로그와 함께 테스트"""
    
    print("=== LLM 처리 테스트 시작 ===")
    
    # 테스트 메시지
    test_message = "축구 유니폼 디자인에 대해 알려주세요"
    
    print(f"전송 메시지: {test_message}")
    
    try:
        # 요청 전송
        response = requests.post(
            "http://localhost:8000/chat/football",
            json={"message": test_message},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"응답 상태: {response.status_code}")
            print(f"응답 내용: {result['response'][:300]}...")
            print("=== 테스트 완료 ===")
        else:
            print(f"오류 발생: {response.status_code}")
            
    except Exception as e:
        print(f"요청 실패: {e}")

if __name__ == "__main__":
    test_with_logging()
