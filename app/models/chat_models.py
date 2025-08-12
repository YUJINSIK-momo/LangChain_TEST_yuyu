from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from app.config import Config
import logging

logger = logging.getLogger(__name__)

class SportsChatbot:
    """스포츠별 챗봇 클래스"""
    
    def __init__(self, sport_type: str):
        self.sport_type = sport_type
        self.sport_name = Config.SPORTS_CONFIG[sport_type]["name"]
        
        # Google Gemini 모델 초기화
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=Config.GOOGLE_API_KEY,
            model="gemini-1.5-pro",
            temperature=0.3  # 더 일관된 응답을 위해 낮춤
        )
        
        # 대화 메모리 초기화
        self.memory = ConversationBufferMemory()
        
        # 대화 체인 초기화
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=True
        )
        
        # 스포츠별 시스템 프롬프트 설정
        self.system_prompt = self._get_system_prompt()
    
    def _get_system_prompt(self) -> str:
        """스포츠별 시스템 프롬프트 반환"""
        prompts = {
            "baseball": """あなたは野球専門のチャットボットです。
            - KBO、MLB、NPBなど様々なリーグ情報の提供
            - 選手統計、チーム順位、試合日程の案内
            - リアルタイム試合結果とハイライトの提供
            - 親しみやすく専門的なトーンで回答""",
            
            "football": """あなたはMAX2MAXサッカーウェアカスタム専門のチャットボットです。
            
            主な役割：
            - サッカーウェアのカスタム制作に関する質問に回答
            - ユニフォームデザイン、素材、サイズ、価格について案内
            - チームウェア制作の流れと注意事項を説明
            - キーパーウェア、トレーニングウェアなど各種商品について案内
            - 背番号の配置、ネックスタイル、ロゴ配置などの詳細説明
            
            回答スタイル：
            - 丁寧で親切な敬語（です・ます調）で回答
            - 具体的で実用的な情報を提供
            - 顧客のニーズに合わせた提案を行う
            - 専門的でありながら分かりやすい説明
            - 必要に応じて箇条書きや表形式で整理して回答
            
            価格・制作に関する情報：
            - 価格は数量や仕様により変動することを明記
            - 制作期間は通常2-3週間程度
            - 最小発注数量についても案内
            - サンプル制作やデザイン修正についても説明
            
            安全な回答ガイドライン：
            - 確認された情報のみを提供
            - 不明な点は「ご確認が必要です」と回答
            - 具体的な商品仕様は「お問い合わせください」と案内
            - 架空の情報や未確認の詳細は避ける
            - 商品種類の詳細質問には「お問い合わせください」で回答
            - 価格に関する質問には「個別にお見積りいたします」で回答
            - 寸法や仕様の詳細は「ウェブサイトまたは担当者にご確認ください」で回答
            
            禁止事項：
            - 不正確な情報の提供
            - 過度に営業的な表現
            - 顧客の個人情報の要求
            - 具体的な価格の明示（概算のみ）
            - FAQの内容と矛盾する回答
            - 確認されていない商品仕様の詳細説明
            - 架空の商品種類やオプションの提示
            - 実際に提供していないサービスの説明""",
            
            "basketball": """あなたはバスケットボール専門のチャットボットです。
            - KBL、NBAなど様々なリーグ情報の提供
            - 選手統計、チーム順位、試合日程の案内
            - リアルタイム試合結果とハイライトの提供
            - 親しみやすく専門的なトーンで回答"""
        }
        
        return prompts.get(self.sport_type, "スポーツ専門チャットボットです。")
    
    async def get_response(self, user_message: str) -> str:
        """사용자 메시지에 대한 응답 생성"""
        try:
            logger.info(f"{self.sport_name} LLM 처리 시작")
            logger.info(f"시스템 프롬프트: {self.system_prompt[:100]}...")
            logger.info(f"사용자 메시지: {user_message}")
            
            # 시스템 프롬프트와 사용자 메시지 결합
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=user_message)
            ]
            
            logger.info(f"LLM 모델 호출 시작: {self.llm}")
            # 응답 생성
            response = await self.llm.ainvoke(messages)
            
            logger.info(f"{self.sport_name} 챗봇 응답 생성 완료: {response.content[:100]}...")
            return response.content
            
        except Exception as e:
            logger.error(f"{self.sport_name} 챗봇 응답 생성 중 오류: {str(e)}")
            logger.error(f"예외 상세: {type(e).__name__}: {e}")
            return f"죄송합니다. {self.sport_name} 정보를 처리하는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
    
    def reset_conversation(self):
        """대화 기록 초기화"""
        self.memory.clear()
        logger.info(f"{self.sport_name} 챗봇 대화 기록 초기화") 