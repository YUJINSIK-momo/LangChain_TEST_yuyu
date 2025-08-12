#!/usr/bin/env python3
"""
한국어 지원 PDF 파일 생성 (수정된 버전)
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
import os

def create_korean_pdf_fixed():
    """한국어 지원 PDF 파일 생성 (수정된 버전)"""
    try:
        # PDF 파일명
        filename = "korean_sports_document_fixed.pdf"
        
        # A4 크기로 캔버스 생성
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        
        # 기본 폰트 설정
        c.setFont("Helvetica", 16)
        
        # 제목
        c.drawString(50, height - 50, "Sports Information Document")
        c.line(50, height - 60, width - 50, height - 60)
        
        # 내용 시작 위치
        y_position = height - 100
        
        # 스포츠 정보 내용 (영어로 작성)
        content = [
            ("Baseball Information:", 14, True),
            ("", 12, False),
            ("• KBO is Korea's professional baseball league.", 12, False),
            ("• 10 teams participate from March to October.", 12, False),
            ("• Major teams: Samsung Lions, Doosan Bears, LG Twins, SSG Landers", 12, False),
            ("• 2024 season champion: SSG Landers", 12, False),
            ("• Key players: Lee Jung-hoo, Kim Ha-seong, Ohtani, Trout", 12, False),
            ("", 12, False),
            ("Football Information:", 14, True),
            ("", 12, False),
            ("• K-League is Korea's professional football league.", 12, False),
            ("• 12 teams participate from February to December.", 12, False),
            ("• Major teams: Ulsan Hyundai, Jeonbuk Hyundai, Pohang Steelers, FC Seoul", 12, False),
            ("• 2024 season champion: Ulsan Hyundai", 12, False),
            ("• Key players: Son Heung-min, Kim Min-jae, Lee Kang-in, Hwang Hee-chan", 12, False),
            ("", 12, False),
            ("Basketball Information:", 14, True),
            ("", 12, False),
            ("• KBL is Korea's professional basketball league.", 12, False),
            ("• 10 teams participate from October to April.", 12, False),
            ("• Major teams: Anyang KGC, Seoul SK, Busan KT, Wonju DB", 12, False),
            ("• 2023-24 season champion: Anyang KGC", 12, False),
            ("• Key players: Heo Hoon, Kim Sun-bin, Ra Gun-ah, Rodriguez", 12, False),
            ("", 12, False),
            ("Latest Sports News:", 14, True),
            ("", 12, False),
            ("• Son Heung-min is recognized as Asia's best player at Tottenham.", 12, False),
            ("• Kim Ha-seong is preparing for MLB debut with San Diego Padres.", 12, False),
            ("• Lee Jung-hoo confirmed MLB entry with New York Yankees contract.", 12, False),
            ("• Korean national football team performing well in 2026 World Cup qualifiers.", 12, False),
            ("", 12, False),
            ("Statistics:", 14, True),
            ("", 12, False),
            ("• KBO 2024 average attendance: 15,234", 12, False),
            ("• K-League 2024 average attendance: 8,567", 12, False),
            ("• KBL 2023-24 average attendance: 3,456", 12, False),
            ("", 12, False),
            ("This document is for sports chatbot testing.", 10, False),
            ("The chatbot can reference this information to answer questions.", 10, False)
        ]
        
        # 내용 작성
        for text, font_size, is_bold in content:
            if is_bold:
                c.setFont("Helvetica-Bold", font_size)
            else:
                c.setFont("Helvetica", font_size)
            
            # 페이지 넘침 처리
            if y_position < 50:
                c.showPage()
                y_position = height - 50
                c.setFont("Helvetica", 12)
            
            c.drawString(50, y_position, text)
            y_position -= font_size + 5
        
        # PDF 저장
        c.save()
        print(f"✅ 영어 PDF 파일 생성 완료: {filename}")
        print(f"📄 파일 크기: {os.path.getsize(filename)} bytes")
        
        return filename
        
    except Exception as e:
        print(f"❌ PDF 생성 오류: {e}")
        return None

def create_simple_text_pdf_fixed():
    """간단한 텍스트 PDF 생성 (영어 테스트용)"""
    try:
        filename = "simple_english.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        
        # 제목
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, height - 50, "Sports Information Document")
        
        # 내용
        c.setFont("Helvetica", 12)
        lines = [
            "This document contains sports information.",
            "",
            "Baseball Information:",
            "- KBO is Korea's professional baseball league.",
            "- Samsung Lions, Doosan Bears participate.",
            "",
            "Football Information:",
            "- K-League is Korea's professional football league.",
            "- Ulsan Hyundai, Jeonbuk Hyundai participate.",
            "",
            "Basketball Information:",
            "- KBL is Korea's professional basketball league.",
            "- Anyang KGC, Seoul SK participate."
        ]
        
        y = height - 100
        for line in lines:
            c.drawString(50, y, line)
            y -= 20
        
        c.save()
        print(f"✅ 간단한 영어 PDF 생성: {filename}")
        return filename
        
    except Exception as e:
        print(f"❌ 간단한 PDF 생성 오류: {e}")
        return None

def create_text_file():
    """텍스트 파일 생성 (한국어 테스트용)"""
    try:
        filename = "sports_info.txt"
        
        content = """스포츠 정보 문서

야구 관련 정보:
• KBO 리그는 한국의 프로야구 리그입니다.
• 10개 팀이 참가하며, 3월부터 10월까지 시즌을 진행합니다.
• 주요 팀: 삼성 라이온즈, 두산 베어스, LG 트윈스, SSG 랜더스
• 2024년 시즌 우승팀: SSG 랜더스
• 주요 선수: 이정후, 김하성, 오타니, 트라웃

축구 관련 정보:
• K리그는 한국의 프로축구 리그입니다.
• 12개 팀이 참가하며, 2월부터 12월까지 시즌을 진행합니다.
• 주요 팀: 울산 현대, 전북 현대, 포항 스틸러스, FC 서울
• 2024년 시즌 우승팀: 울산 현대
• 주요 선수: 손흥민, 김민재, 이강인, 황희찬

농구 관련 정보:
• KBL은 한국의 프로농구 리그입니다.
• 10개 팀이 참가하며, 10월부터 4월까지 시즌을 진행합니다.
• 주요 팀: 안양 KGC, 서울 SK, 부산 KT, 원주 DB
• 2023-24 시즌 우승팀: 안양 KGC
• 주요 선수: 허훈, 김선빈, 라건아, 로드리게스

최신 스포츠 뉴스:
• 손흥민이 토트넘에서 활약하며 아시아 최고 선수로 인정받고 있습니다.
• 김하성이 샌디에고 파드레스에서 메이저리그 데뷔를 앞두고 있습니다.
• 이정후가 뉴욕 양키스와 계약하며 MLB 진출을 확정했습니다.
• 한국 축구대표팀이 2026 월드컵 아시아 예선에서 좋은 성적을 거두고 있습니다.

통계 정보:
• KBO 2024년 평균 관중: 15,234명
• K리그 2024년 평균 관중: 8,567명
• KBL 2023-24년 평균 관중: 3,456명

이 문서는 스포츠 챗봇 테스트를 위한 샘플 문서입니다.
PDF 문서 학습 기능을 통해 챗봇이 이 정보를 참조하여 답변할 수 있습니다.
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 한국어 텍스트 파일 생성: {filename}")
        return filename
        
    except Exception as e:
        print(f"❌ 텍스트 파일 생성 오류: {e}")
        return None

if __name__ == "__main__":
    print("🇰🇷 문서 파일 생성 (수정된 버전)\n")
    
    # 1. 영어 PDF 생성
    print("1️⃣ 영어 PDF 파일 생성")
    english_pdf = create_korean_pdf_fixed()
    
    # 2. 간단한 영어 PDF 생성
    print("\n2️⃣ 간단한 영어 PDF 생성")
    simple_pdf = create_simple_text_pdf_fixed()
    
    # 3. 한국어 텍스트 파일 생성
    print("\n3️⃣ 한국어 텍스트 파일 생성")
    text_file = create_text_file()
    
    print("\n✅ 모든 파일 생성 완료!")
    print("📝 이제 영어 PDF와 한국어 텍스트 파일을 사용하여 테스트할 수 있습니다.")
