# 🧠 LangChain과 RAG 개념 완벽 가이드

## 🤔 LangChain이란?

### 📖 기본 개념
**LangChain**은 대화형 AI 모델(LLM)을 활용한 애플리케이션을 쉽게 개발할 수 있게 해주는 프레임워크입니다.

### 🎯 왜 LangChain을 사용하나요?

#### 기존 AI 모델의 한계
```
❌ 문제점:
- AI 모델은 학습된 데이터만 알고 있음
- 최신 정보나 특정 도메인 정보 부족
- "할루시네이션" (잘못된 정보 생성) 문제
- 문서 기반 질의응답 어려움
```

#### LangChain의 해결책
```
✅ 해결책:
- 외부 데이터 소스 연결
- 문서 기반 질의응답
- 메모리 기능으로 대화 맥락 유지
- 체인(Chain)으로 복잡한 작업 조합
```

### 🔧 LangChain의 핵심 구성요소

#### 1. **LLM (Large Language Model)**
```python
# Google Gemini 모델 사용
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    google_api_key="your_api_key",
    model="gemini-1.5-pro"
)
```

#### 2. **프롬프트 (Prompt)**
```python
# 시스템 프롬프트 정의
system_prompt = """
당신은 야구 전문 챗봇입니다.
- KBO, MLB 정보 제공
- 정확하고 친근한 답변
- 제공된 문서 정보 우선 사용
"""
```

#### 3. **메모리 (Memory)**
```python
# 대화 기록 저장
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
# 이전 대화 내용을 기억하여 맥락 유지
```

#### 4. **체인 (Chain)**
```python
# 여러 작업을 연결
from langchain.chains import ConversationChain

conversation = ConversationChain(
    llm=llm,
    memory=memory
)
```

## 🔍 RAG (Retrieval Augmented Generation)란?

### 📖 RAG 개념
**RAG**는 "검색 기반 생성"으로, 사용자 질문에 대해 관련 문서를 검색하고, 그 정보를 바탕으로 AI가 답변을 생성하는 방식입니다.

### 🎯 RAG의 작동 원리

```
1️⃣ 사용자 질문
   ↓
2️⃣ 관련 문서 검색 (Retrieval)
   ↓
3️⃣ 검색된 문서를 컨텍스트로 포함
   ↓
4️⃣ AI 모델이 컨텍스트를 바탕으로 답변 생성 (Generation)
```

### 🔄 RAG vs 일반 AI 모델

#### 일반 AI 모델
```
사용자: "KBO 2024년 우승팀은?"
AI: "죄송합니다. 2024년 정보는 학습되지 않았습니다."
```

#### RAG 기반 AI
```
사용자: "KBO 2024년 우승팀은?"
↓
검색: "KBO 2024년 우승팀 SSG 랜더스" 문서 발견
↓
AI: "2024년 KBO 우승팀은 SSG 랜더스입니다. (출처: 스포츠 정보 문서)"
```

### 🏗️ RAG 시스템 구성요소

#### 1. **문서 로더 (Document Loader)**
```python
# PDF 파일 로드
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("sports_document.pdf")
documents = loader.load()
```

#### 2. **텍스트 분할기 (Text Splitter)**
```python
# 긴 문서를 작은 청크로 분할
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # 1000자 단위로 분할
    chunk_overlap=200  # 200자 겹침으로 맥락 유지
)
chunks = splitter.split_documents(documents)
```

#### 3. **임베딩 (Embedding)**
```python
# 텍스트를 숫자 벡터로 변환
from langchain_google_genai import GoogleGenerativeAIEmbeddings

embeddings = GoogleGenerativeAIEmbeddings(
    google_api_key="your_api_key",
    model="models/embedding-001"
)
```

#### 4. **벡터 데이터베이스 (Vector Database)**
```python
# FAISS 벡터 스토어 생성
from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_documents(
    documents=chunks,
    embedding=embeddings
)
```

#### 5. **검색 및 생성**
```python
# 관련 문서 검색
relevant_docs = vectorstore.similarity_search(
    query="KBO 우승팀",
    k=3  # 상위 3개 문서
)

# 컨텍스트 생성
context = f"""
관련 문서 정보:
{chr(10).join([doc.page_content for doc in relevant_docs])}

질문: {user_question}
"""
```

## 🚀 실제 구현 예시

### 📋 1단계: 문서 업로드 및 처리

```python
# 1. PDF 파일 로드
loader = PyPDFLoader("sports_info.pdf")
documents = loader.load()

# 2. 텍스트 청킹
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = splitter.split_documents(documents)

# 3. 벡터 스토어 생성
vectorstore = FAISS.from_documents(
    documents=chunks,
    embedding=embeddings
)

# 4. 벡터 스토어 저장
vectorstore.save_local("data/baseball/vectorstore")
```

### 🔍 2단계: 질의응답 처리

```python
# 1. 사용자 질문
user_question = "KBO 2024년 우승팀은?"

# 2. 관련 문서 검색
relevant_docs = vectorstore.similarity_search(
    query=user_question,
    k=3
)

# 3. 컨텍스트 생성
context = f"""
다음은 관련 문서에서 찾은 정보입니다:
{chr(10).join([doc.page_content for doc in relevant_docs])}

위 정보를 참고하여 다음 질문에 답변해주세요:
질문: {user_question}
"""

# 4. AI 모델 호출
response = llm.invoke([
    SystemMessage(content="당신은 스포츠 전문 챗봇입니다."),
    HumanMessage(content=context)
])
```

## 🎯 RAG의 장점

### ✅ 정확성 향상
- 문서 기반 정확한 정보 제공
- 최신 정보 반영 가능
- 출처 명시로 신뢰성 확보

### ✅ 확장성
- 새로운 문서 추가 용이
- 다양한 문서 형식 지원
- 도메인별 특화 가능

### ✅ 투명성
- 답변의 출처 명시
- 검색된 문서 확인 가능
- 검증 가능한 정보 제공

## 🔧 실제 프로젝트에서의 활용

### 📁 문서 관리
```
data/
├── baseball/
│   ├── documents/     # 원본 문서
│   └── vectorstore/   # 벡터 데이터베이스
├── football/
│   ├── documents/
│   └── vectorstore/
└── basketball/
    ├── documents/
    └── vectorstore/
```

### 🔄 워크플로우
1. **문서 업로드** → PDF/텍스트 파일
2. **문서 처리** → 텍스트 추출 및 청킹
3. **벡터화** → 임베딩 생성 및 저장
4. **질의응답** → 검색 → 컨텍스트 생성 → AI 응답

### 🎨 사용자 경험
- **직관적**: 일반적인 대화처럼 질문
- **정확한**: 문서 기반 정확한 답변
- **투명한**: 출처 명시로 신뢰성 확보
- **확장 가능**: 새로운 문서 추가로 지식 확장

## 💡 핵심 포인트

### 🎯 LangChain
- **목적**: LLM 애플리케이션 개발 프레임워크
- **장점**: 모듈화, 확장성, 다양한 도구 통합
- **활용**: 챗봇, 문서 처리, 자동화

### 🔍 RAG
- **목적**: 문서 기반 정확한 질의응답
- **장점**: 정확성, 확장성, 투명성
- **활용**: 지식 베이스, 고객 지원, 교육

### 🚀 조합 효과
- **LangChain + RAG**: 강력한 지능형 챗봇 시스템
- **실용성**: 실제 비즈니스 요구사항 충족
- **미래성**: AI 기술 발전에 따른 확장 가능
