from fastapi import FastAPI, Request, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import logging
import os
from typing import Dict, Any, List

from app.config import Config
from app.models.chat_models import SportsChatbot
from app.services.line_service import LineService
from app.services.sports_service import SportsService
from app.services.faq_service import FAQService
from app.utils.logger import setup_logger

# 로거 설정
logger = setup_logger()

app = FastAPI(
    title="스포츠 LINE 챗봇 API",
    description="야구, 축구, 농구 LINE 채널을 위한 LangChain 기반 챗봇 API",
    version="1.0.0"
)

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 환경에서는 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 스포츠별 챗봇 인스턴스
chatbots = {
    "baseball": SportsChatbot("baseball"),
    "football": SportsChatbot("football"), 
    "basketball": SportsChatbot("basketball")
}

# 스포츠별 서비스 인스턴스
sports_services = {
    "baseball": SportsService("baseball"),
    "football": SportsService("football"),
    "basketball": SportsService("basketball")
}

# 스포츠별 FAQ 서비스 인스턴스
faq_services = {
    "baseball": FAQService("baseball"),
    "football": FAQService("football"),
    "basketball": FAQService("basketball")
}

@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행"""
    logger.info("스포츠 챗봇 서비스 시작")

@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 실행"""
    logger.info("스포츠 챗봇 서비스 종료")

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "스포츠 LINE 챗봇 API",
        "version": "1.0.0",
        "sports": ["baseball", "football", "basketball"]
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}

@app.post("/webhook/{sport_type}")
async def line_webhook(sport_type: str, request: Request):
    """LINE Bot 웹훅 엔드포인트"""
    try:
        # 스포츠 타입 검증
        if sport_type not in ["baseball", "football", "basketball"]:
            raise HTTPException(status_code=400, detail="Invalid sport type")
        
        # LINE 서비스 초기화
        line_service = LineService(sport_type)
        sports_service = sports_services[sport_type]
        
        # 요청 본문 파싱
        body = await request.body()
        signature = request.headers.get("X-Line-Signature", "")
        
        # LINE 이벤트 파싱
        events = json.loads(body.decode('utf-8'))
        
        for event in events.get("events", []):
            try:
                # 이벤트 타입 확인
                if event.get("type") == "message" and event.get("message", {}).get("type") == "text":
                    # source 필드 안전하게 접근
                    source = event.get("source", {})
                    user_id = source.get("userId")
                    user_message = event.get("message", {}).get("text", "")
                    
                    if not user_id or not user_message:
                        logger.warning(f"유효하지 않은 이벤트 데이터: {event}")
                        continue
                    
                    logger.info(f"{sport_type} 채널에서 메시지 수신: {user_message}")
                    
                    # 메시지 처리
                    response_data = await process_message(
                        sport_type, user_message, sports_service
                    )
                    
                    # 응답이 딕셔너리인 경우 (향상된 챗봇)
                    if isinstance(response_data, dict):
                        # 텍스트 메시지 전송
                        await line_service.send_text_message(user_id, response_data["text"])
                        
                        # 이미지가 있으면 이미지도 전송
                        if response_data.get("image_urls"):
                            for image_url in response_data["image_urls"]:
                                await line_service.send_image_message(user_id, image_url)
                    else:
                        # 일반 텍스트 응답
                        await line_service.send_text_message(user_id, response_data)
                        
            except Exception as event_error:
                logger.error(f"이벤트 처리 중 오류: {str(event_error)}")
                continue
        
        return JSONResponse(content={"status": "success"})
        
    except Exception as e:
        logger.error(f"웹훅 처리 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def process_message(sport_type: str, user_message: str, sports_service: SportsService):
    """사용자 메시지 처리"""
    try:
        # 특정 키워드 처리
        if "일정" in user_message or "경기" in user_message:
            schedules = sports_service.get_schedule_data()
            return sports_service.format_schedule_message(schedules)
        
        elif "순위" in user_message or "랭킹" in user_message:
            rankings = sports_service.get_ranking_data()
            return sports_service.format_ranking_message(rankings)
        
        elif "뉴스" in user_message or "소식" in user_message:
            news = sports_service.get_news_data()
            return sports_service.format_news_message(news)
        
        elif "메뉴" in user_message or "도움말" in user_message:
            return get_help_message(sport_type)
        
        else:
            # FAQ 검색 우선 수행
            faq_service = faq_services[sport_type]
            faq_results = await faq_service.search_faq(user_message, threshold=0.5)
            
            if faq_results:
                # FAQ에서 답변 찾음
                best_match = faq_results[0]
                
                logger.info(f"FAQ 매칭 결과: 유사도 {best_match['similarity']:.2f}")
                
                # 유사도가 매우 높은 경우 FAQ 답변만 반환
                if best_match['similarity'] >= 0.95:
                    logger.info(f"유사도가 매우 높음 ({best_match['similarity']:.2f}), FAQ 답변만 반환")
                    # FAQ에 이미지가 있는 경우
                    if best_match.get('image_urls'):
                        return {
                            "text": best_match['answer'],
                            "image_urls": best_match['image_urls']
                        }
                    else:
                        return best_match['answer']
                elif best_match['similarity'] >= 0.7:
                    # 유사도가 높은 경우 FAQ 답변만 반환 (AI 추가 설명 없이)
                    logger.info(f"유사도가 높음 ({best_match['similarity']:.2f}), FAQ 답변만 반환")
                    if best_match.get('image_urls'):
                        return {
                            "text": best_match['answer'],
                            "image_urls": best_match['image_urls']
                        }
                    else:
                        return best_match['answer']
                else:
                    # 유사도가 낮은 경우 AI 답변 우선
                    logger.info(f"유사도가 낮음 ({best_match['similarity']:.2f}), AI 답변 우선")
                    chatbot = chatbots[sport_type]
                    ai_response = await chatbot.get_response(user_message)
                    
                    if isinstance(ai_response, dict):
                        combined_text = f"AI 답변: {ai_response['text']}\n\n관련 FAQ: {best_match['answer']}"
                        return {
                            "text": combined_text,
                            "image_urls": ai_response.get("image_urls", [])
                        }
                    else:
                        combined_text = f"AI 답변: {ai_response}\n\n관련 FAQ: {best_match['answer']}"
                        return combined_text
            
            # FAQ에서 답변을 찾지 못한 경우 AI 모델 사용
            logger.info(f"{sport_type} FAQ에서 답변을 찾지 못해 AI 모델 사용")
            chatbot = chatbots[sport_type]
            logger.info(f"LLM 처리 시작: {user_message}")
            ai_response = await chatbot.get_response(user_message)
            logger.info(f"LLM 처리 완료: {ai_response[:100] if isinstance(ai_response, str) else '응답 생성됨'}...")
            return ai_response
    
    except Exception as e:
        logger.error(f"메시지 처리 중 오류: {str(e)}")
        return "죄송합니다. 메시지를 처리하는 중 오류가 발생했습니다."

def get_help_message(sport_type: str) -> str:
    """도움말 메시지 반환"""
    sport_name = Config.SPORTS_CONFIG[sport_type]["name"]
    
    return f"""🏈 {sport_name} 챗봇 도움말

📋 사용 가능한 명령어:
• "일정" 또는 "경기" - 경기 일정 확인
• "순위" 또는 "랭킹" - 팀 순위 확인  
• "뉴스" 또는 "소식" - 최신 뉴스 확인
• "메뉴" 또는 "도움말" - 이 도움말 표시

💬 자유로운 대화도 가능합니다!
{sport_name}에 대해 궁금한 것이 있으면 언제든 물어보세요.

📚 PDF 문서 학습 기능도 지원합니다!"""

@app.post("/chat/{sport_type}")
async def chat_endpoint(sport_type: str, request: Dict[str, Any]):
    """채팅 API 엔드포인트 (테스트용)"""
    try:
        if sport_type not in ["baseball", "football", "basketball"]:
            raise HTTPException(status_code=400, detail="Invalid sport type")
        
        user_message = request.get("message", "")
        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        sports_service = sports_services[sport_type]
        response_message = await process_message(sport_type, user_message, sports_service)
        
        return {
            "sport_type": sport_type,
            "user_message": user_message,
            "response": response_message
        }
    
    except Exception as e:
        logger.error(f"채팅 API 처리 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# FAQ 관리 API 엔드포인트들
@app.get("/faq/{sport_type}")
async def get_faq_list(sport_type: str, category: str = None):
    """FAQ 목록 조회"""
    try:
        if sport_type not in ["baseball", "football", "basketball"]:
            raise HTTPException(status_code=400, detail="Invalid sport type")
        
        faq_service = faq_services[sport_type]
        
        if category:
            faq_list = faq_service.get_faq_by_category(category)
        else:
            faq_list = faq_service.export_faq_to_json()
        
        return {
            "sport_type": sport_type,
            "category": category,
            "count": len(faq_list),
            "faq_list": faq_list
        }
    
    except Exception as e:
        logger.error(f"FAQ 목록 조회 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/faq/{sport_type}/categories")
async def get_faq_categories(sport_type: str):
    """FAQ 카테고리 목록 조회"""
    try:
        if sport_type not in ["baseball", "football", "basketball"]:
            raise HTTPException(status_code=400, detail="Invalid sport type")
        
        faq_service = faq_services[sport_type]
        categories = faq_service.get_all_categories()
        
        return {
            "sport_type": sport_type,
            "categories": categories,
            "count": len(categories)
        }
    
    except Exception as e:
        logger.error(f"FAQ 카테고리 조회 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/faq/{sport_type}")
async def add_faq(sport_type: str, request: Dict[str, Any]):
    """FAQ 항목 추가"""
    try:
        if sport_type not in ["baseball", "football", "basketball"]:
            raise HTTPException(status_code=400, detail="Invalid sport type")
        
        # 필수 필드 검증
        required_fields = ["category", "question", "answer"]
        for field in required_fields:
            if field not in request or not request[field]:
                raise HTTPException(status_code=400, detail=f"{field} is required")
        
        faq_service = faq_services[sport_type]
        
        success = faq_service.add_faq(
            category=request["category"],
            question=request["question"],
            answer=request["answer"],
            tags=request.get("tags", []),
            threshold=request.get("threshold", 0.7),
            questions=request.get("questions", [])
        )
        
        if success:
            return {
                "status": "success",
                "message": "FAQ 항목이 성공적으로 추가되었습니다.",
                "sport_type": sport_type
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to add FAQ item")
    
    except Exception as e:
        logger.error(f"FAQ 항목 추가 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/faq/{sport_type}/{faq_id}")
async def update_faq(sport_type: str, faq_id: int, request: Dict[str, Any]):
    """FAQ 항목 수정"""
    try:
        if sport_type not in ["baseball", "football", "basketball"]:
            raise HTTPException(status_code=400, detail="Invalid sport type")
        
        faq_service = faq_services[sport_type]
        
        success = faq_service.update_faq(
            faq_id=faq_id,
            category=request.get("category"),
            question=request.get("question"),
            answer=request.get("answer"),
            tags=request.get("tags"),
            threshold=request.get("threshold")
        )
        
        if success:
            return {
                "status": "success",
                "message": "FAQ 항목이 성공적으로 수정되었습니다.",
                "sport_type": sport_type,
                "faq_id": faq_id
            }
        else:
            raise HTTPException(status_code=404, detail="FAQ item not found")
    
    except Exception as e:
        logger.error(f"FAQ 항목 수정 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/faq/{sport_type}/{faq_id}")
async def delete_faq(sport_type: str, faq_id: int):
    """FAQ 항목 삭제"""
    try:
        if sport_type not in ["baseball", "football", "basketball"]:
            raise HTTPException(status_code=400, detail="Invalid sport type")
        
        faq_service = faq_services[sport_type]
        
        success = faq_service.delete_faq(faq_id)
        
        if success:
            return {
                "status": "success",
                "message": "FAQ 항목이 성공적으로 삭제되었습니다.",
                "sport_type": sport_type,
                "faq_id": faq_id
            }
        else:
            raise HTTPException(status_code=404, detail="FAQ item not found")
    
    except Exception as e:
        logger.error(f"FAQ 항목 삭제 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/faq/{sport_type}/search")
async def search_faq(sport_type: str, request: Dict[str, Any]):
    """FAQ 검색"""
    try:
        if sport_type not in ["baseball", "football", "basketball"]:
            raise HTTPException(status_code=400, detail="Invalid sport type")
        
        query = request.get("query", "")
        threshold = request.get("threshold", 0.7)
        
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        faq_service = faq_services[sport_type]
        results = faq_service.search_faq(query, threshold)
        
        return {
            "sport_type": sport_type,
            "query": query,
            "threshold": threshold,
            "count": len(results),
            "results": results
        }
    
    except Exception as e:
        logger.error(f"FAQ 검색 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/faq/{sport_type}/import")
async def import_faq(sport_type: str, request: Dict[str, Any]):
    """FAQ JSON 데이터 가져오기"""
    try:
        if sport_type not in ["baseball", "football", "basketball"]:
            raise HTTPException(status_code=400, detail="Invalid sport type")
        
        faq_data = request.get("faq_data", [])
        
        if not isinstance(faq_data, list):
            raise HTTPException(status_code=400, detail="faq_data must be a list")
        
        faq_service = faq_services[sport_type]
        success = faq_service.import_faq_from_json(faq_data)
        
        if success:
            return {
                "status": "success",
                "message": f"{len(faq_data)}개의 FAQ 항목이 성공적으로 가져와졌습니다.",
                "sport_type": sport_type,
                "imported_count": len(faq_data)
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to import FAQ data")
    
    except Exception as e:
        logger.error(f"FAQ 가져오기 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/faq/{sport_type}/export")
async def export_faq(sport_type: str):
    """FAQ JSON 데이터 내보내기"""
    try:
        if sport_type not in ["baseball", "football", "basketball"]:
            raise HTTPException(status_code=400, detail="Invalid sport type")
        
        faq_service = faq_services[sport_type]
        faq_data = faq_service.export_faq_to_json()
        
        return {
            "sport_type": sport_type,
            "count": len(faq_data),
            "faq_data": faq_data
        }
    
    except Exception as e:
        logger.error(f"FAQ 내보내기 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 