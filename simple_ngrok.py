#!/usr/bin/env python3
"""
간단한 ngrok 설정 스크립트
"""

from pyngrok import ngrok
import subprocess
import time

def main():
    """ngrok 터널 생성 및 서버 시작"""
    
    # 포트 설정
    port = 8001
    
    print("🌐 ngrok 터널 생성 중...")
    
    # 기존 터널 정리
    ngrok.kill()
    
    # 새 터널 생성
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
    
    print(f"\n🚀 서버를 별도 터미널에서 시작하세요:")
    print(f"python -m uvicorn app.main:app --host 127.0.0.1 --port {port}")
    
    print("\n⏳ ngrok 터널이 실행 중입니다. Ctrl+C로 종료하세요.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 ngrok 터널 종료 중...")
        ngrok.kill()

if __name__ == "__main__":
    main()
