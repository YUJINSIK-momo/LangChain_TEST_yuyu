#!/usr/bin/env python3
"""
JSON 기반 FAQ 서비스
"""

import json
import os
from typing import List, Dict, Any, Optional
from difflib import SequenceMatcher
from app.utils.logger import logger
from app.utils.japanese_formatter import JapaneseFormatter


class FAQService:
    """JSON 기반 FAQ 관리 및 검색 서비스"""
    
    def __init__(self, sport_type: str):
        self.sport_type = sport_type
        self.faq_file = f"data/{sport_type}/faq.json"
        self.faq_data = []
        self.japanese_formatter = JapaneseFormatter()
        self.load_faq()
    
    def load_faq(self):
        """FAQ JSON 파일 로드"""
        try:
            if os.path.exists(self.faq_file):
                with open(self.faq_file, 'r', encoding='utf-8') as f:
                    self.faq_data = json.load(f)
                logger.info(f"{self.sport_type} FAQ 로드 완료: {len(self.faq_data)}개 항목")
            else:
                self.faq_data = []
                logger.info(f"{self.sport_type} FAQ 파일이 존재하지 않아 새로 생성합니다")
        except Exception as e:
            logger.error(f"FAQ 로드 오류: {e}")
            self.faq_data = []
    
    def save_faq(self):
        """FAQ JSON 파일 저장"""
        try:
            # 디렉토리 생성
            os.makedirs(os.path.dirname(self.faq_file), exist_ok=True)
            
            with open(self.faq_file, 'w', encoding='utf-8') as f:
                json.dump(self.faq_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"{self.sport_type} FAQ 저장 완료")
            return True
        except Exception as e:
            logger.error(f"FAQ 저장 오류: {e}")
            return False
    
    def add_faq(self, category: str, question: str, answer: str, tags: List[str] = None, threshold: float = 0.7, image_urls: List[str] = None, questions: List[str] = None) -> bool:
        """FAQ 항목 추가"""
        try:
            faq_id = len(self.faq_data) + 1
            
            # 질문 리스트 처리 (기존 question도 포함)
            question_list = questions or []
            if question and question not in question_list:
                question_list.insert(0, question)  # 첫 번째 질문을 메인으로
            
            faq_item = {
                "id": faq_id,
                "category": category,
                "question": question,  # 메인 질문 (하위 호환성)
                "questions": question_list,  # 모든 질문 리스트
                "answer": answer,
                "tags": tags or [],
                "threshold": threshold,
                "image_urls": image_urls or []
            }
            
            self.faq_data.append(faq_item)
            success = self.save_faq()
            
            if success:
                logger.info(f"{self.sport_type} FAQ 항목 추가 완료: {question}")
            
            return success
        except Exception as e:
            logger.error(f"FAQ 항목 추가 오류: {e}")
            return False
    
    def update_faq(self, faq_id: int, category: str = None, question: str = None, 
                   answer: str = None, tags: List[str] = None, threshold: float = None, image_urls: List[str] = None) -> bool:
        """FAQ 항목 수정"""
        try:
            for item in self.faq_data:
                if item["id"] == faq_id:
                    if category is not None:
                        item["category"] = category
                    if question is not None:
                        item["question"] = question
                    if answer is not None:
                        item["answer"] = answer
                    if tags is not None:
                        item["tags"] = tags
                    if threshold is not None:
                        item["threshold"] = threshold
                    if image_urls is not None:
                        item["image_urls"] = image_urls
                    
                    success = self.save_faq()
                    if success:
                        logger.info(f"{self.sport_type} FAQ 항목 수정 완료: ID {faq_id}")
                    return success
            
            logger.warning(f"FAQ 항목을 찾을 수 없습니다: ID {faq_id}")
            return False
        except Exception as e:
            logger.error(f"FAQ 항목 수정 오류: {e}")
            return False
    
    def delete_faq(self, faq_id: int) -> bool:
        """FAQ 항목 삭제"""
        try:
            self.faq_data = [item for item in self.faq_data if item["id"] != faq_id]
            success = self.save_faq()
            
            if success:
                logger.info(f"{self.sport_type} FAQ 항목 삭제 완료: ID {faq_id}")
            
            return success
        except Exception as e:
            logger.error(f"FAQ 항목 삭제 오류: {e}")
            return False
    
    async def search_faq(self, query: str, threshold: float = 0.7) -> List[Dict[str, Any]]:
        """FAQ 검색 (유사도 기반)"""
        try:
            if not query.strip():
                return []
            
            results = []
            query_lower = query.lower()
            query_normalized = self._normalize_japanese_text(query_lower)
            
            for item in self.faq_data:
                # 질문과 답변에서 검색
                answer_normalized = self._normalize_japanese_text(item["answer"].lower())
                
                # 다중 질문 처리
                question_similarities = []
                
                # 메인 질문 (하위 호환성)
                if "question" in item:
                    main_question = self._normalize_japanese_text(item["question"].lower())
                    question_similarities.append(SequenceMatcher(None, query_normalized, main_question).ratio())
                
                # 추가 질문들
                if "questions" in item and item["questions"]:
                    for q in item["questions"]:
                        q_normalized = self._normalize_japanese_text(q.lower())
                        question_similarities.append(SequenceMatcher(None, query_normalized, q_normalized).ratio())
                
                # 최고 질문 유사도
                question_similarity = max(question_similarities) if question_similarities else 0
                answer_similarity = SequenceMatcher(None, query_normalized, answer_normalized).ratio()
                
                # 추가: 키워드 기반 유사도 계산
                keyword_similarity = self._calculate_keyword_similarity(query_lower, item["question"].lower())
                
                # 태그에서 검색
                tag_similarity = 0
                for tag in item["tags"]:
                    tag_sim = SequenceMatcher(None, query_lower, tag.lower()).ratio()
                    tag_similarity = max(tag_similarity, tag_sim)
                
                # 최고 유사도 계산 (키워드 유사도도 포함)
                max_similarity = max(question_similarity, answer_similarity, tag_similarity, keyword_similarity)
                
                # 임계값 확인
                item_threshold = item.get("threshold", threshold)
                logger.info(f"임계값 확인: {max_similarity:.2f} >= {item_threshold}")
                if max_similarity >= item_threshold:
                    # 일본어 답변인 경우 자동 변환
                    formatted_answer = item["answer"]
                    logger.info(f"FAQ 매칭됨: {item['question']} (유사도: {max_similarity:.2f})")
                    
                    is_japanese = self.japanese_formatter._is_japanese(item["answer"])
                    
                    if is_japanese:
                        logger.info(f"일본어 답변 감지됨: {item['answer'][:30]}...")
                        try:
                            if self.sport_type == "football":
                                formatted_answer = await self.japanese_formatter.format_for_football(item["answer"])
                                logger.info(f"축구 채널용 일본어 변환 완료")
                            else:
                                formatted_answer = await self.japanese_formatter.format_japanese_response(item["answer"])
                                logger.info(f"일반 일본어 변환 완료")
                        except Exception as e:
                            logger.error(f"일본어 변환 실패: {e}")
                            formatted_answer = item["answer"]  # 실패 시 원본 사용
                    else:
                        formatted_answer = item["answer"]
                    
                    results.append({
                        **item,
                        "answer": formatted_answer,
                        "similarity": max_similarity
                    })
            
            # 유사도 순으로 정렬
            results.sort(key=lambda x: x["similarity"], reverse=True)
            
            logger.info(f"{self.sport_type} FAQ 검색 완료: {len(results)}개 결과")
            return results
            
        except Exception as e:
            logger.error(f"FAQ 검색 오류: {e}")
            return []
    
    def get_faq_by_category(self, category: str) -> List[Dict[str, Any]]:
        """카테고리별 FAQ 조회"""
        try:
            results = [item for item in self.faq_data if item["category"] == category]
            logger.info(f"{self.sport_type} 카테고리 '{category}' FAQ 조회: {len(results)}개")
            return results
        except Exception as e:
            logger.error(f"카테고리별 FAQ 조회 오류: {e}")
            return []
    
    def get_all_categories(self) -> List[str]:
        """모든 카테고리 조회"""
        try:
            categories = list(set(item["category"] for item in self.faq_data if item["category"]))
            categories.sort()
            return categories
        except Exception as e:
            logger.error(f"카테고리 조회 오류: {e}")
            return []
    
    def get_faq_count(self) -> int:
        """FAQ 항목 수 조회"""
        return len(self.faq_data)
    
    def import_faq_from_json(self, json_data: List[Dict[str, Any]]) -> bool:
        """JSON 데이터로부터 FAQ 가져오기"""
        try:
            # 기존 데이터 백업
            backup_data = self.faq_data.copy()
            
            # 새 데이터로 교체
            self.faq_data = json_data
            
            # 저장 시도
            if self.save_faq():
                logger.info(f"{self.sport_type} FAQ 가져오기 완료: {len(json_data)}개 항목")
                return True
            else:
                # 실패 시 백업 복원
                self.faq_data = backup_data
                logger.error(f"{self.sport_type} FAQ 가져오기 실패, 백업 복원")
                return False
                
        except Exception as e:
            logger.error(f"FAQ 가져오기 오류: {e}")
            return False
    
    def export_faq_to_json(self) -> List[Dict[str, Any]]:
        """FAQ 데이터를 JSON 형태로 내보내기"""
        return self.faq_data.copy()
    
    def _normalize_japanese_text(self, text: str) -> str:
        """일본어 텍스트 정규화 (의미는 같지만 표현이 다른 경우 처리)"""
        # 일반적인 일본어 표현 정규화
        normalizations = {
            "可能？": "可能でしょうか",
            "可能ですか": "可能でしょうか",
            "可能でしょうか？": "可能でしょうか",
            "可能でしょうか？": "可能でしょうか",
            "可能でしょうか": "可能でしょうか",
            "個々で": "個々で",
            "個別で": "個々で",
            "番号": "番号",
            "背番号": "番号",
            "入れる": "入れる",
            "配置": "入れる",
            "場所": "場所",
            "位置": "場所",
            "変更": "変更",
            "変更可能": "変更可能",
            "変更できます": "変更可能",
            "変更できますか": "変更可能でしょうか"
        }
        
        normalized_text = text
        for old, new in normalizations.items():
            normalized_text = normalized_text.replace(old, new)
        
        return normalized_text
    
    def _calculate_keyword_similarity(self, query: str, question: str) -> float:
        """키워드 기반 유사도 계산"""
        # 핵심 키워드 추출
        keywords = ["番号", "場所", "変更", "可能", "個々", "入れる", "配置"]
        
        query_keywords = [kw for kw in keywords if kw in query]
        question_keywords = [kw for kw in keywords if kw in question]
        
        if not query_keywords or not question_keywords:
            return 0.0
        
        # 공통 키워드 수 계산
        common_keywords = set(query_keywords) & set(question_keywords)
        total_keywords = set(query_keywords) | set(question_keywords)
        
        if not total_keywords:
            return 0.0
        
        # Jaccard 유사도 계산
        similarity = len(common_keywords) / len(total_keywords)
        
        # 키워드 가중치 적용
        if len(common_keywords) >= 3:  # 핵심 키워드가 3개 이상 일치
            similarity = min(1.0, similarity * 1.5)
        
        return similarity
