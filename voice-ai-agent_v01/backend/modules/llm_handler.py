from typing import Optional, List, Dict
import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMHandler:
    """LLM Handler using Groq (Free Llama 3.2)"""
    
    def __init__(self):
        try:
            from groq import Groq
            self.client = Groq(api_key=Config.GROQ_API_KEY)
            self.model = "llama-3.2-3b-preview"
            logger.info(f"✅ Groq initialized with {self.model}")
        except ImportError:
            raise ImportError("Install: pip install groq")
    
    def get_response(self, query: str, language: str = "en", 
                    context: List[Dict] = None) -> Optional[str]:
        """Get AI response"""
        try:
            system_prompt = self._build_system_prompt(language)
            
            messages = [{"role": "system", "content": system_prompt}]
            
            if context:
                messages.extend(context[-6:])
            
            messages.append({"role": "user", "content": query})
            
            logger.info(f"🤔 Querying Groq...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=Config.MAX_TOKENS,
                temperature=Config.TEMPERATURE
            )
            
            response_text = response.choices[0].message.content
            logger.info("✅ Got response")
            
            return response_text
            
        except Exception as e:
            logger.error(f"❌ Groq error: {e}")
            return "Sorry, I'm having trouble right now."
    
    def _build_system_prompt(self, language: str) -> str:
        """Build system prompt"""
        language_names = {
            'en': 'English', 'hi': 'Hindi', 'es': 'Spanish', 'fr': 'French'
        }
        
        lang_name = language_names.get(language, 'English')
        
        return f"""You are a helpful multilingual AI assistant.

LANGUAGE: Respond in {lang_name} ONLY.
STYLE: Keep responses SHORT (2-3 sentences). Be conversational.

Remember: This is a VOICE conversation in {lang_name}."""
    
    def test_connection(self) -> bool:
        """Test connection"""
        try:
            self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=5
            )
            logger.info("✅ Groq connected")
            return True
        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            return False