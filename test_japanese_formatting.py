#!/usr/bin/env python3
"""
LLM 기반 일본어 자동 변환 기능 테스트 (원본 유지)
"""

import asyncio
from app.utils.japanese_formatter import JapaneseFormatter

async def test_japanese_formatting():
    """일본어 변환 테스트"""
    formatter = JapaneseFormatter()
    
    # 실제 FAQ 데이터로 테스트
    test_cases = [
        "GK(ゴールキーパー)ユニフォームも制作可能でございます。",
        "【ユニフォームネックスタイル】\nラウンドネック5種\nVネック6種\n襟付き3種\nチームでご希望のスタイルを選択可能",
        "不可\n位置はチーム統一となります。"
    ]
    
    print("=" * 50)
    print("LLM 기반 일본어 자동 변환 테스트 (실제 FAQ 데이터)")
    print("=" * 50)
    
    for i, original_text in enumerate(test_cases, 1):
        print(f"\n📝 테스트 케이스 {i}:")
        print(f"원본: {original_text}")
        
        # 일본어 감지 테스트
        is_japanese = formatter._is_japanese(original_text)
        print(f"일본어 감지: {is_japanese}")
        
        if is_japanese:
            # 변환 테스트
            try:
                formatted = await formatter.format_japanese_response(original_text, "business_formal")
                print(f"변환 후: {formatted}")
                
                if formatted == original_text:
                    print("⚠️ 변환되지 않음 (원본과 동일)")
                else:
                    print("✅ 변환 성공")
            except Exception as e:
                print(f"❌ 변환 오류: {e}")
        else:
            print("❌ 일본어로 감지되지 않음")
    
    print("\n" + "=" * 50)
    print("테스트 완료!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test_japanese_formatting())
