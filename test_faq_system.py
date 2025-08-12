#!/usr/bin/env python3
"""
FAQ 시스템 테스트
"""

import asyncio
import json
import requests
from typing import Dict, Any
from app.services.faq_service import FAQService

# API 기본 URL
API_BASE_URL = "http://localhost:8000"

def test_faq_api():
    """FAQ API 테스트"""
    sport_type = "baseball"
    
    print("=" * 50)
    print("FAQ 시스템 테스트 시작")
    print("=" * 50)
    
    # 1. FAQ 목록 조회
    print("\n1. FAQ 목록 조회")
    try:
        response = requests.get(f"{API_BASE_URL}/faq/{sport_type}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ FAQ 목록 조회 성공: {data['count']}개 항목")
            for item in data['faq_list']:
                print(f"  - ID: {item['id']}, 카테고리: {item['category']}, 질문: {item['question'][:30]}...")
        else:
            print(f"❌ FAQ 목록 조회 실패: {response.status_code}")
    except Exception as e:
        print(f"❌ FAQ 목록 조회 오류: {e}")
    
    # 2. FAQ 항목 추가
    print("\n2. FAQ 항목 추가")
    new_faq = {
        "category": "규칙",
        "question": "야구에서 스트라이크란 무엇인가요?",
        "answer": "스트라이크는 타자가 공을 치지 못하거나, 타자가 친 공이 파울인 경우에 주어집니다. 3스트라이크가 되면 아웃됩니다.",
        "tags": ["규칙", "스트라이크", "아웃"],
        "threshold": 0.7
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/faq/{sport_type}", json=new_faq)
        if response.status_code == 200:
            print("✅ FAQ 항목 추가 성공")
        else:
            print(f"❌ FAQ 항목 추가 실패: {response.status_code}")
    except Exception as e:
        print(f"❌ FAQ 항목 추가 오류: {e}")
    
    # 3. FAQ 검색
    print("\n3. FAQ 검색")
    search_query = {
        "query": "스트라이크",
        "threshold": 0.6
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/faq/{sport_type}/search", json=search_query)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ FAQ 검색 성공: {data['count']}개 결과")
            for result in data['results']:
                print(f"  - 유사도: {result['similarity']:.2f}, 질문: {result['question']}")
        else:
            print(f"❌ FAQ 검색 실패: {response.status_code}")
    except Exception as e:
        print(f"❌ FAQ 검색 오류: {e}")
    
    # 4. 카테고리별 FAQ 조회
    print("\n4. 카테고리별 FAQ 조회")
    try:
        response = requests.get(f"{API_BASE_URL}/faq/{sport_type}?category=규칙")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 카테고리별 FAQ 조회 성공: {data['count']}개 항목")
        else:
            print(f"❌ 카테고리별 FAQ 조회 실패: {response.status_code}")
    except Exception as e:
        print(f"❌ 카테고리별 FAQ 조회 오류: {e}")
    
    # 5. FAQ 내보내기
    print("\n5. FAQ 내보내기")
    try:
        response = requests.get(f"{API_BASE_URL}/faq/{sport_type}/export")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ FAQ 내보내기 성공: {data['count']}개 항목")
            
            # JSON 파일로 저장
            with open(f"data/{sport_type}/faq_backup.json", "w", encoding="utf-8") as f:
                json.dump(data['faq_data'], f, ensure_ascii=False, indent=2)
            print(f"  - 백업 파일 저장: data/{sport_type}/faq_backup.json")
        else:
            print(f"❌ FAQ 내보내기 실패: {response.status_code}")
    except Exception as e:
        print(f"❌ FAQ 내보내기 오류: {e}")

def test_chatbot_with_faq():
    """FAQ가 통합된 챗봇 테스트"""
    print("\n" + "=" * 50)
    print("FAQ 통합 챗봇 테스트")
    print("=" * 50)
    
    sport_type = "baseball"
    test_messages = [
        "스트라이크란 무엇인가요?",
        "야구 규칙에 대해 알려주세요",
        "오늘 날씨는 어때요?",
        "일정을 알려주세요"
    ]
    
    for message in test_messages:
        print(f"\n사용자: {message}")
        try:
            response = requests.post(f"{API_BASE_URL}/chat/{sport_type}", json={"message": message})
            if response.status_code == 200:
                data = response.json()
                print(f"챗봇: {data['response']}")
            else:
                print(f"❌ 챗봇 응답 실패: {response.status_code}")
        except Exception as e:
            print(f"❌ 챗봇 테스트 오류: {e}")

async def test_faq_japanese_formatting():
    """FAQ 일본어 변환 테스트"""
    print("=" * 50)
    print("FAQ 일본어 변환 테스트")
    print("=" * 50)
    
    # FAQ 서비스 초기화
    faq_service = FAQService("football")
    
    # 테스트 쿼리
    test_queries = [
        "キーパーユニホームも作成可能ですか？",
        "ネックスタイルの種類",
        "番号の入れる場所を、個々で変更は可能でしょうか"
    ]
    
    for query in test_queries:
        print(f"\n🔍 쿼리: {query}")
        
        # FAQ 검색
        results = await faq_service.search_faq(query, threshold=0.6)
        
        if results:
            best_match = results[0]
            print(f"✅ 매칭됨 (유사도: {best_match['similarity']:.2f})")
            print(f"📝 원본 답변: {best_match['answer']}")
            
            # 일본어 변환 확인
            if faq_service.japanese_formatter._is_japanese(best_match['answer']):
                print("🇯🇵 일본어 감지됨 - 변환 적용")
            else:
                print("❌ 일본어 아님 - 변환 미적용")
        else:
            print("❌ 매칭되지 않음")
    
    print("\n" + "=" * 50)
    print("테스트 완료!")
    print("=" * 50)

def create_sample_faq_data():
    """샘플 FAQ 데이터 생성"""
    sample_data = [
        {
            "id": 1,
            "category": "규칙",
            "question": "야구에서 스트라이크란 무엇인가요?",
            "answer": "스트라이크는 타자가 공을 치지 못하거나, 타자가 친 공이 파울인 경우에 주어집니다. 3스트라이크가 되면 아웃됩니다.",
            "tags": ["규칙", "스트라이크", "아웃"],
            "threshold": 0.7
        },
        {
            "id": 2,
            "category": "규칙",
            "question": "볼이란 무엇인가요?",
            "answer": "볼은 투수가 던진 공이 스트라이크존을 벗어난 경우에 주어집니다. 4볼이 되면 타자가 1루로 진루합니다.",
            "tags": ["규칙", "볼", "진루"],
            "threshold": 0.7
        },
        {
            "id": 3,
            "category": "선수",
            "question": "최고 타율 선수는 누구인가요?",
            "answer": "현재 KBO 리그에서 최고 타율을 기록하고 있는 선수는 [선수명]입니다.",
            "tags": ["선수", "타율", "기록"],
            "threshold": 0.6
        },
        {
            "id": 4,
            "category": "경기",
            "question": "야구 경기는 몇 이닝까지 하나요?",
            "answer": "야구 경기는 일반적으로 9이닝까지 진행됩니다. 동점인 경우 연장전이 진행될 수 있습니다.",
            "tags": ["경기", "이닝", "연장전"],
            "threshold": 0.7
        }
    ]
    
    # baseball과 basketball만 생성 (football은 건드리지 않음)
    for sport in ["baseball", "basketball"]:
        print(f"{sport} 샘플 FAQ 데이터 생성 중...")
        try:
            faq_service = FAQService(sport)
            faq_service.faq_data = sample_data.copy()
            faq_service.save_faq()
            print(f"✅ {sport} 샘플 데이터 생성 성공")
        except Exception as e:
            print(f"❌ {sport} 샘플 데이터 생성 실패: {e}")

def main():
    """메인 테스트 함수"""
    print("FAQ 시스템 테스트를 시작합니다...")
    
    # 1. 샘플 데이터 생성 (football 제외)
    create_sample_faq_data()
    
    # 2. API 테스트 (baseball만)
    test_faq_api()
    
    # 3. 챗봇 통합 테스트 (baseball만)
    test_chatbot_with_faq()
    
    # 4. FAQ 일본어 변환 테스트 (football)
    asyncio.run(test_faq_japanese_formatting())
    
    print("\n" + "=" * 50)
    print("FAQ 시스템 테스트 완료")
    print("=" * 50)

if __name__ == "__main__":
    main()
