import json
import logging
import os
from typing import Dict, List, Any
from datetime import datetime, timedelta
from app.config import Config

logger = logging.getLogger(__name__)

class SportsService:
    """스포츠 데이터 서비스 클래스"""
    
    def __init__(self, sport_type: str):
        self.sport_type = sport_type
        self.sport_name = Config.SPORTS_CONFIG[sport_type]["name"]
        self.data_path = Config.SPORTS_CONFIG[sport_type]["data_path"]
        
        # 데이터 디렉토리 생성
        os.makedirs(self.data_path, exist_ok=True)
    
    def get_schedule_data(self) -> List[Dict[str, Any]]:
        """경기 일정 데이터 반환"""
        try:
            schedule_file = os.path.join(self.data_path, "schedule.json")
            if os.path.exists(schedule_file):
                with open(schedule_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # 샘플 데이터 반환
                return self._get_sample_schedule()
        except Exception as e:
            logger.error(f"{self.sport_name} 일정 데이터 로드 중 오류: {str(e)}")
            return []
    
    def get_ranking_data(self) -> List[Dict[str, Any]]:
        """팀 순위 데이터 반환"""
        try:
            ranking_file = os.path.join(self.data_path, "ranking.json")
            if os.path.exists(ranking_file):
                with open(ranking_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # 샘플 데이터 반환
                return self._get_sample_ranking()
        except Exception as e:
            logger.error(f"{self.sport_name} 순위 데이터 로드 중 오류: {str(e)}")
            return []
    
    def get_news_data(self) -> List[Dict[str, Any]]:
        """뉴스 데이터 반환"""
        try:
            news_file = os.path.join(self.data_path, "news.json")
            if os.path.exists(news_file):
                with open(news_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # 샘플 데이터 반환
                return self._get_sample_news()
        except Exception as e:
            logger.error(f"{self.sport_name} 뉴스 데이터 로드 중 오류: {str(e)}")
            return []
    
    def _get_sample_schedule(self) -> List[Dict[str, Any]]:
        """샘플 경기 일정 데이터"""
        if self.sport_type == "baseball":
            return [
                {
                    "date": "2024-01-15",
                    "home_team": "삼성 라이온즈",
                    "away_team": "LG 트윈스",
                    "venue": "대구구장",
                    "time": "18:30"
                },
                {
                    "date": "2024-01-16", 
                    "home_team": "두산 베어스",
                    "away_team": "키움 히어로즈",
                    "venue": "잠실구장",
                    "time": "18:30"
                }
            ]
        elif self.sport_type == "football":
            return [
                {
                    "date": "2024-01-15",
                    "home_team": "울산 현대",
                    "away_team": "전북 현대",
                    "venue": "울산문수축구경기장",
                    "time": "19:00"
                },
                {
                    "date": "2024-01-16",
                    "home_team": "포항 스틸러스", 
                    "away_team": "수원 삼성",
                    "venue": "포항스틸야드",
                    "time": "19:00"
                }
            ]
        else:  # basketball
            return [
                {
                    "date": "2024-01-15",
                    "home_team": "서울 SK",
                    "away_team": "안양 KGC",
                    "venue": "잠실체육관",
                    "time": "19:00"
                },
                {
                    "date": "2024-01-16",
                    "home_team": "부산 KT",
                    "away_team": "원주 DB",
                    "venue": "부산체육관",
                    "time": "19:00"
                }
            ]
    
    def _get_sample_ranking(self) -> List[Dict[str, Any]]:
        """샘플 팀 순위 데이터"""
        if self.sport_type == "baseball":
            return [
                {"rank": 1, "team": "SSG 랜더스", "games": 144, "wins": 88, "losses": 56},
                {"rank": 2, "team": "LG 트윈스", "games": 144, "wins": 86, "losses": 58},
                {"rank": 3, "team": "KT 위즈", "games": 144, "wins": 80, "losses": 64}
            ]
        elif self.sport_type == "football":
            return [
                {"rank": 1, "team": "울산 현대", "games": 38, "points": 76, "wins": 23, "draws": 7, "losses": 8},
                {"rank": 2, "team": "전북 현대", "games": 38, "points": 72, "wins": 21, "draws": 9, "losses": 8},
                {"rank": 3, "team": "포항 스틸러스", "games": 38, "points": 68, "wins": 19, "draws": 11, "losses": 8}
            ]
        else:  # basketball
            return [
                {"rank": 1, "team": "서울 SK", "games": 54, "wins": 35, "losses": 19},
                {"rank": 2, "team": "안양 KGC", "games": 54, "wins": 33, "losses": 21},
                {"rank": 3, "team": "부산 KT", "games": 54, "wins": 30, "losses": 24}
            ]
    
    def _get_sample_news(self) -> List[Dict[str, Any]]:
        """샘플 뉴스 데이터"""
        if self.sport_type == "baseball":
            return [
                {
                    "title": "이정후, MLB 진출 선언",
                    "summary": "KBO 리그 스타 이정후가 MLB 진출을 선언했습니다.",
                    "date": "2024-01-15"
                },
                {
                    "title": "삼성 라이온즈, 새로운 외국인 선수 영입",
                    "summary": "삼성 라이온즈가 새로운 외국인 투수를 영입했습니다.",
                    "date": "2024-01-14"
                }
            ]
        elif self.sport_type == "football":
            return [
                {
                    "title": "손흥민, 프리미어리그 득점왕 수상",
                    "summary": "손흥민이 프리미어리그 득점왕을 수상했습니다.",
                    "date": "2024-01-15"
                },
                {
                    "title": "김민재, 바이에른 뮌헨 이적",
                    "summary": "김민재가 바이에른 뮌헨으로 이적을 확정했습니다.",
                    "date": "2024-01-14"
                }
            ]
        else:  # basketball
            return [
                {
                    "title": "허재 감독, KBL 올해의 감독상 수상",
                    "summary": "허재 감독이 KBL 올해의 감독상을 수상했습니다.",
                    "date": "2024-01-15"
                },
                {
                    "title": "김선빈, NBA 진출 도전",
                    "summary": "김선빈이 NBA 진출을 위해 도전을 시작했습니다.",
                    "date": "2024-01-14"
                }
            ]
    
    def format_schedule_message(self, schedules: List[Dict[str, Any]]) -> str:
        """경기 일정을 메시지 형태로 포맷팅"""
        if not schedules:
            return f"{self.sport_name} 경기 일정이 없습니다."
        
        message = f"📅 {self.sport_name} 경기 일정\n\n"
        for schedule in schedules[:5]:  # 최근 5경기만 표시
            message += f"📆 {schedule['date']}\n"
            message += f"🏟️ {schedule['venue']}\n"
            message += f"⚽ {schedule['away_team']} vs {schedule['home_team']}\n"
            message += f"🕐 {schedule['time']}\n\n"
        
        return message
    
    def format_ranking_message(self, rankings: List[Dict[str, Any]]) -> str:
        """팀 순위를 메시지 형태로 포맷팅"""
        if not rankings:
            return f"{self.sport_name} 순위 정보가 없습니다."
        
        message = f"🏆 {self.sport_name} 팀 순위\n\n"
        for rank in rankings[:10]:  # 상위 10팀만 표시
            if self.sport_type == "football":
                message += f"{rank['rank']}위: {rank['team']} ({rank['points']}점)\n"
            else:
                message += f"{rank['rank']}위: {rank['team']} ({rank['wins']}승 {rank['losses']}패)\n"
        
        return message
    
    def format_news_message(self, news_list: List[Dict[str, Any]]) -> str:
        """뉴스를 메시지 형태로 포맷팅"""
        if not news_list:
            return f"{self.sport_name} 뉴스가 없습니다."
        
        message = f"📰 {self.sport_name} 최신 뉴스\n\n"
        for news in news_list[:3]:  # 최근 3개 뉴스만 표시
            message += f"📌 {news['title']}\n"
            message += f"📝 {news['summary']}\n"
            message += f"📅 {news['date']}\n\n"
        
        return message 