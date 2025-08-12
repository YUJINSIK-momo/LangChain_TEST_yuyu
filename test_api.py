#!/usr/bin/env python3
"""
API 테스트 스크립트
"""

import requests
import json

def test_api():
    """API 엔드포인트 테스트"""
    base_url = "http://127.0.0.1:8001"
    
    print("🏈 스포츠 챗봇 API 테스트\n")
    
    # 1. 루트 엔드포인트 테스트
    print("1. 루트 엔드포인트 테스트")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   상태: {response.status_code}")
        print(f"   응답: {response.json()}")
        print()
    except Exception as e:
        print(f"   오류: {e}")
        print()
    
    # 2. 헬스체크 테스트
    print("2. 헬스체크 테스트")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   상태: {response.status_code}")
        print(f"   응답: {response.json()}")
        print()
    except Exception as e:
        print(f"   오류: {e}")
        print()
    
    # 3. 채팅 API 테스트 (POST)
    sports = ["baseball", "football", "basketball"]
    
    for sport in sports:
        print(f"3. {sport} 채팅 API 테스트")
        try:
            data = {
                "message": "안녕하세요"
            }
            response = requests.post(f"{base_url}/chat/{sport}", json=data)
            print(f"   상태: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   스포츠: {result.get('sport_type')}")
                print(f"   사용자 메시지: {result.get('user_message')}")
                print(f"   챗봇 응답: {result.get('response')[:100]}...")
            else:
                print(f"   오류: {response.text}")
            print()
        except Exception as e:
            print(f"   오류: {e}")
            print()

if __name__ == "__main__":
    test_api() 