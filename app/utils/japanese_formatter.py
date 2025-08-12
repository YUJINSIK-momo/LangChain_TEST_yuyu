#!/usr/bin/env python3
"""
LLM 기반 일본어 답변 자동 변환 유틸리티 (원본 유지)
"""

import random
import re
from typing import List, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import Config
from app.utils.logger import logger

class JapaneseFormatter:
    """LLM을 사용한 일본어 답변 자동 변환 클래스 (원본 유지)"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=Config.GOOGLE_API_KEY,
            model="gemini-1.5-pro",
            temperature=0.3  # 낮은 temperature로 일관성 확보
        )
        
        self.prompts = {
            "business_formal": """
以下のテキストを、必ず丁寧に変換してください。特に「不可」は必ず「不可でございます」に変更してください。

必須変更点：
- 「不可」→「不可でございます」（必ず変更）
- 「選択可能」→「ご選択いただけます」
- 「となります」→「となっております」

例：
元のテキスト: "不可 位置はチーム統一となります。"
変換後: "不可でございます。位置はチーム統一となっております。"

元のテキスト:
{text}

変換後（「不可」は必ず「不可でございます」に変更）:
""",
            "business_polite": """
以下のテキストを、必ず丁寧に変換してください。特に「不可」は必ず「不可です」に変更してください。

必須変更点：
- 「不可」→「不可です」（必ず変更）
- 「選択可能」→「ご選択いただけます」
- 「となります」→「となっています」

例：
元のテキスト: "不可 位置はチーム統一となります。"
変換後: "不可です。位置はチーム統一となっています。"

元のテキスト:
{text}

変換後（「不可」は必ず「不可です」に変更）:
""",
            "casual_polite": """
以下のテキストを、必ず親しみやすく変換してください。特に「不可」は必ず「できません」に変更してください。

必須変更点：
- 「不可」→「できません」（必ず変更）
- 「選択可能」→「お選びいただけます」
- 「となります」→「となっています」

例：
元のテキスト: "不可 位置はチーム統一となります。"
変換後: "できません。位置はチーム統一となっています。"

元のテキスト:
{text}

変換後（「不可」は必ず「できません」に変更）:
""",
            "football_special": """
以下のテキストを、必ず丁寧に変換してください。

特に以下の変更を必ず行ってください：
1. 「不可」→「不可でございます」
2. 「選択可能」→「ご選択いただけます」
3. 「となります」→「となっております」

元のテキスト:
{text}

変換後（上記の変更を必ず適用）:
"""
        }
    
    def _is_japanese(self, text: str) -> bool:
        """일본어 텍스트인지 확인"""
        japanese_chars = re.findall(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]', text)
        return len(japanese_chars) > len(text) * 0.3  # 30% 이상이 일본어 문자
    
    async def format_japanese_response(self, original_text: str, style: str = "random") -> str:
        """LLM을 사용하여 일본어 답변을 지정된 스타일로 변환 (원본 유지)"""
        if not self._is_japanese(original_text):
            return original_text
        
        if style == "random":
            style = random.choice(list(self.prompts.keys()))
        
        if style not in self.prompts:
            return original_text
        
        try:
            prompt = self.prompts[style].format(text=original_text)
            
            # LLM 호출
            response = await self.llm.ainvoke(prompt)
            formatted_text = response.content.strip()
            
            # 디버깅: LLM 출력 확인
            logger.info(f"LLM 원본 출력: {formatted_text}")
            
            # 변환 성공 시 로그
            logger.info(f"변환 성공: {original_text[:30]}... → {formatted_text[:30]}...")
            
            # 원본과 동일한 경우 디버깅
            if formatted_text == original_text:
                logger.warning(f"⚠️ LLM이 변환하지 않음 - 원본과 동일")
            
            return formatted_text
            
        except Exception as e:
            logger.error(f"LLM 변환 오류: {e}")
            return original_text
    
    async def get_multiple_formats(self, original_text: str, count: int = 3) -> List[str]:
        """여러 패턴으로 변환된 답변 반환"""
        if not self._is_japanese(original_text):
            return [original_text]
        
        formats = []
        available_styles = list(self.prompts.keys())
        
        for i in range(min(count, len(available_styles))):
            style = available_styles[i]
            formatted = await self.format_japanese_response(original_text, style)
            formats.append(formatted)
        
        return formats
    
    async def format_for_football(self, original_text: str) -> str:
        """축구 채널용 특별 포맷팅"""
        logger.info(f"format_for_football 호출됨: {original_text}")
        result = await self.format_japanese_response(original_text, "football_special")
        logger.info(f"format_for_football 결과: {result}")
        return result
