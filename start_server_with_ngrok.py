#!/usr/bin/env python3
"""
ngrok을 사용해서 외부 URL을 생성하고 서버를 시작하는 스크립트
"""

import uvicorn
from pyngrok import ngrok
import os
import sys

def start_server_with_ngrok():
    """ngrok을 사용해서 서버를 시작"""
    
    # 포트 설정 (8001 대신 8002 사용)
    port = 8002
    
    # ngrok 터널 생성
    print("🌐 ngrok 터널 생성 중...")
    public_url = ngrok.connect(port)
    print(f"✅ 공개 URL: {public_url}")
    
    # 웹훅 URL들 출력
    print("\n🔗 LINE Bot 웹훅 URL 설정:")
    print(f"야구 채널: {public_url}/webhook/baseball")
    print(f"축구 채널: {public_url}/webhook/football")
    print(f"농구 채널: {public_url}/webhook/basketball")
    
    print("\n📋 LINE Developers Console에서 설정:")
    print("1. 각 스포츠 채널의 Messaging API 설정")
    print("2. Webhook URL에 위의 URL들을 입력")
    print("3. Use webhook 옵션을 활성화")
    
    # 서버 시작
    print(f"\n🚀 서버 시작 중... (포트: {port})")
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=True)

if __name__ == "__main__":
    try:
        start_server_with_ngrok()
    except KeyboardInterrupt:
        print("\n🛑 서버 종료 중...")
        ngrok.kill()
        sys.exit(0)
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        ngrok.kill()
        sys.exit(1)
