# 🎨 프롬프트 엔지니어링 완벽 가이드

## 🤔 프롬프트 엔지니어링이란?

### 📖 기본 개념
**프롬프트 엔지니어링**은 AI 모델에게 원하는 결과를 얻기 위해 입력 텍스트(프롬프트)를 최적화하는 기술입니다.

### 🎯 왜 중요한가요?

#### AI 모델의 특성
```
🧠 AI 모델은:
- 입력된 프롬프트에 따라 출력이 달라짐
- 맥락과 지시사항을 정확히 이해해야 함
- 일관성 있는 결과를 위해 명확한 가이드 필요
```

#### 프롬프트 엔지니어링의 역할
```
✅ 효과:
- 정확한 답변 유도
- 일관된 톤앤매너 유지
- 원하는 형식으로 출력
- 오류 최소화
```

## 🏗️ 프롬프트 구조

### 📋 기본 프롬프트 구성

```python
# 시스템 프롬프트 (AI의 역할 정의)
system_prompt = """
당신은 야구 전문 챗봇입니다.
- KBO, MLB, NPB 등 다양한 리그 정보 제공
- 선수 통계, 팀 순위, 경기 일정 안내
- 친근하고 전문적인 톤으로 응답
- 제공된 문서 정보를 바탕으로 정확한 답변 제공
"""

# 사용자 프롬프트 (실제 질문)
user_prompt = "KBO 2024년 우승팀은 어디인가요?"

# 컨텍스트 프롬프트 (관련 문서 정보)
context_prompt = """
다음은 관련 문서에서 찾은 정보입니다:
• KBO 리그는 한국의 프로야구 리그입니다.
• 2024년 시즌 우승팀: SSG 랜더스

위의 문서 정보를 참고하여 다음 질문에 답변해주세요:
질문: KBO 2024년 우승팀은 어디인가요?
"""
```

### 🎨 프롬프트 패턴

#### 1. **역할 정의 패턴**
```python
role_prompt = """
당신은 {도메인} 전문가입니다.
특징:
- {특징1}
- {특징2}
- {특징3}

답변 스타일:
- {스타일1}
- {스타일2}
"""
```

#### 2. **단계별 사고 패턴**
```python
thinking_prompt = """
다음 단계로 생각해보세요:

1단계: 질문 분석
- 사용자가 무엇을 묻고 있는가?
- 필요한 정보는 무엇인가?

2단계: 관련 정보 검색
- 제공된 문서에서 관련 정보 찾기
- 추가로 필요한 정보 확인

3단계: 답변 구성
- 정확한 정보 포함
- 명확하고 이해하기 쉽게 설명

4단계: 출처 명시
- 정보의 출처 표시
- 신뢰성 확보

질문: {user_question}
"""
```

#### 3. **Few-Shot 학습 패턴**
```python
few_shot_prompt = """
다음 예시를 참고하여 답변해주세요:

예시 1:
질문: "KBO 주요 팀은?"
답변: "KBO의 주요 팀들은 삼성 라이온즈, 두산 베어스, LG 트윈스, SSG 랜더스 등이 있습니다."

예시 2:
질문: "2024년 우승팀은?"
답변: "2024년 KBO 우승팀은 SSG 랜더스입니다."

이제 다음 질문에 답변해주세요:
질문: {user_question}
"""
```

## 🚀 현재 프로젝트의 프롬프트 분석

### 📊 현재 사용 중인 프롬프트

#### 1. **기본 챗봇 프롬프트** (`app/models/chat_models.py`)
```python
def _get_system_prompt(self) -> str:
    base_prompts = {
        "baseball": """당신은 야구 전문 챗봇입니다.
        - KBO, MLB, NPB 등 다양한 리그 정보 제공
        - 선수 통계, 팀 순위, 경기 일정 안내
        - 실시간 경기 결과 및 하이라이트 제공
        - 친근하고 전문적인 톤으로 응답""",
        
        "football": """당신은 축구 전문 챗봇입니다.
        - K리그, EPL, 라리가, 분데스리가 등 다양한 리그 정보 제공
        - 선수 통계, 팀 순위, 경기 일정 안내
        - 실시간 경기 결과 및 하이라이트 제공
        - 친근하고 전문적인 톤으로 응답""",
        
        "basketball": """당신은 농구 전문 챗봇입니다.
        - KBL, NBA 등 다양한 리그 정보 제공
        - 선수 통계, 팀 순위, 경기 일정 안내
        - 실시간 경기 결과 및 하이라이트 제공
        - 친근하고 전문적인 톤으로 응답"""
    }
```

#### 2. **향상된 챗봇 프롬프트** (`app/models/enhanced_chat_models.py`)
```python
def _create_context_prompt(self, user_message: str, relevant_docs: list) -> str:
    context = f"""
    다음은 {self.sport_name} 관련 문서에서 찾은 관련 정보입니다:
    {chr(10).join([f"문서 {i+1}: {doc}" for i, doc in enumerate(relevant_docs)])}
    
    위의 문서 정보를 참고하여 다음 질문에 답변해주세요:
    질문: {user_message}
    
    답변 시 다음 사항을 지켜주세요:
    1. 제공된 문서 정보를 우선적으로 사용
    2. 문서에 없는 정보는 일반적인 지식으로 보완
    3. 문서 출처를 명시
    4. 정확하고 신뢰할 수 있는 정보 제공
    """
```

### 🎯 개선된 프롬프트 제안

#### 1. **더 구체적인 역할 정의**
```python
enhanced_system_prompt = """
당신은 {sport_name} 전문 챗봇 '스포츠 어시스턴트'입니다.

🎯 주요 역할:
• {sport_name} 관련 질문에 정확하고 친근하게 답변
• 최신 정보와 통계 제공
• 사용자의 관심사에 맞는 맞춤형 정보 제공

📊 정보 제공 범위:
• 리그 정보 (KBO, K리그, KBL 등)
• 팀 및 선수 정보
• 경기 일정 및 결과
• 통계 및 기록
• 최신 뉴스 및 소식

💬 대화 스타일:
• 친근하고 이해하기 쉬운 설명
• 전문적이면서도 접근하기 쉬운 톤
• 사용자 수준에 맞는 정보 제공
• 적절한 예시와 비유 사용

🔍 답변 원칙:
• 정확성 우선
• 출처 명시
• 객관적 정보 제공
• 사용자 관점에서 답변
"""
```

#### 2. **단계별 사고 과정 포함**
```python
thinking_prompt = """
다음 단계로 체계적으로 답변해주세요:

🔍 1단계: 질문 분석
- 사용자가 묻는 핵심 내용 파악
- 필요한 정보 유형 결정
- 관련 도메인 식별

📚 2단계: 정보 수집
- 제공된 문서에서 관련 정보 검색
- 추가 일반 지식 보완
- 최신성과 정확성 확인

🧠 3단계: 답변 구성
- 핵심 정보 우선 배치
- 논리적 구조로 정리
- 사용자 수준에 맞게 설명

✅ 4단계: 품질 검증
- 정보 정확성 확인
- 출처 명시
- 완성도 점검

질문: {user_question}
"""
```

#### 3. **감정적 연결 강화**
```python
emotional_prompt = """
당신은 {sport_name}을 사랑하는 팬이자 전문가입니다.

❤️ 스포츠에 대한 열정을 담아 답변해주세요:
• 스포츠의 재미와 감동 전달
• 팬의 관점에서 이해하기 쉽게 설명
• 흥미로운 이야기와 재미있는 사실 포함

🎯 전문성과 친근함의 균형:
• 정확한 정보 제공
• 쉽고 재미있는 설명
• 사용자와의 감정적 연결

💡 창의적 답변:
• 예상치 못한 재미있는 사실
• 흥미로운 통계나 기록
• 관련된 재미있는 이야기
"""
```

## 🚀 LangGraph 도입 계획

### 📖 LangGraph란?

**LangGraph**는 LangChain의 확장으로, 복잡한 AI 워크플로우를 그래프 형태로 구성할 수 있게 해주는 프레임워크입니다.

### 🎯 LangGraph의 장점

#### 1. **복잡한 워크플로우 관리**
```python
# 현재: 단순한 체인
user_question → RAG 검색 → AI 응답

# LangGraph: 복잡한 워크플로우
user_question → 의도 분석 → 정보 검색 → 컨텍스트 생성 → AI 응답 → 품질 검증 → 최종 응답
```

#### 2. **조건부 분기 처리**
```python
# 사용자 의도에 따른 분기
if "일정" in question:
    → 일정 정보 제공
elif "순위" in question:
    → 순위 정보 제공
elif "뉴스" in question:
    → 뉴스 정보 제공
else:
    → 일반 대화
```

#### 3. **메모리와 상태 관리**
```python
# 대화 맥락 유지
conversation_state = {
    "user_id": "user123",
    "sport_type": "baseball",
    "previous_questions": [...],
    "user_preferences": {...}
}
```

### 🏗️ LangGraph 구현 예시

#### 1. **노드 정의**
```python
from langgraph.graph import StateGraph, END

# 상태 정의
class ConversationState:
    user_id: str
    sport_type: str
    user_question: str
    relevant_docs: List[str]
    ai_response: str
    conversation_history: List[str]

# 노드들 정의
def analyze_intent(state: ConversationState) -> ConversationState:
    """사용자 의도 분석"""
    # 의도 분석 로직
    return state

def search_documents(state: ConversationState) -> ConversationState:
    """관련 문서 검색"""
    # 문서 검색 로직
    return state

def generate_response(state: ConversationState) -> ConversationState:
    """AI 응답 생성"""
    # 응답 생성 로직
    return state

def validate_response(state: ConversationState) -> ConversationState:
    """응답 품질 검증"""
    # 품질 검증 로직
    return state
```

#### 2. **그래프 구성**
```python
# 워크플로우 그래프 생성
workflow = StateGraph(ConversationState)

# 노드 추가
workflow.add_node("analyze_intent", analyze_intent)
workflow.add_node("search_documents", search_documents)
workflow.add_node("generate_response", generate_response)
workflow.add_node("validate_response", validate_response)

# 엣지 연결
workflow.add_edge("analyze_intent", "search_documents")
workflow.add_edge("search_documents", "generate_response")
workflow.add_edge("generate_response", "validate_response")
workflow.add_edge("validate_response", END)

# 컴파일
app = workflow.compile()
```

#### 3. **조건부 분기**
```python
def route_by_intent(state: ConversationState) -> str:
    """의도에 따른 분기"""
    if "일정" in state.user_question:
        return "schedule_info"
    elif "순위" in state.user_question:
        return "ranking_info"
    elif "뉴스" in state.user_question:
        return "news_info"
    else:
        return "general_chat"

# 조건부 엣지 추가
workflow.add_conditional_edges(
    "analyze_intent",
    route_by_intent,
    {
        "schedule_info": "get_schedule",
        "ranking_info": "get_ranking", 
        "news_info": "get_news",
        "general_chat": "search_documents"
    }
)
```

## 🎯 향후 개선 계획

### 📋 1단계: 프롬프트 최적화
- [ ] 더 구체적인 역할 정의
- [ ] 단계별 사고 과정 포함
- [ ] 감정적 연결 강화
- [ ] Few-shot 학습 예시 추가

### 🚀 2단계: LangGraph 도입
- [ ] 복잡한 워크플로우 설계
- [ ] 조건부 분기 로직 구현
- [ ] 상태 관리 시스템 구축
- [ ] 품질 검증 노드 추가

### 🎨 3단계: 사용자 경험 개선
- [ ] 개인화된 응답
- [ ] 대화 맥락 유지
- [ ] 사용자 선호도 학습
- [ ] 멀티모달 지원

### 🔧 4단계: 성능 최적화
- [ ] 응답 속도 개선
- [ ] 메모리 사용량 최적화
- [ ] 에러 처리 강화
- [ ] 모니터링 시스템 구축

## 💡 핵심 포인트

### 🎯 프롬프트 엔지니어링
- **명확성**: AI가 이해하기 쉬운 명확한 지시
- **구체성**: 구체적인 예시와 제약 조건
- **일관성**: 일관된 톤앤매너 유지
- **검증**: 답변 품질 검증 메커니즘

### 🚀 LangGraph
- **복잡성**: 복잡한 워크플로우 관리
- **유연성**: 조건부 분기와 상태 관리
- **확장성**: 새로운 기능 추가 용이
- **모니터링**: 각 단계별 추적 가능

### 🎨 사용자 경험
- **개인화**: 사용자 맞춤형 응답
- **연속성**: 대화 맥락 유지
- **신뢰성**: 정확하고 검증된 정보
- **재미**: 흥미로운 대화 경험
