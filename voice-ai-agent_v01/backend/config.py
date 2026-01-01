import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask Configuration
    FLASK_HOST = os.getenv("FLASK_HOST", "127.0.0.1")
    FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))

    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    
    # LLM Settings
    MAX_TOKENS = 500
    TEMPERATURE = 0.7
    
    # LLM Configuration
    LLM_PROVIDER = "ollama"
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
    
    # Supported Languages (ONLY WORKING ONES)
    SUPPORTED_LANGUAGES = {
        'en': {
            'name': 'English',
            'flag': '🇬🇧',
            'greeting': 'Hello! I can help you in English.',
            'tts_code': 'en',
            'stt_code': 'en-US'
        },
        'hi': {
            'name': 'Hindi',
            'flag': '🇮🇳',
            'greeting': 'नमस्ते! मैं हिंदी में आपकी मदद कर सकता हूं।',
            'tts_code': 'hi',
            'stt_code': 'hi-IN'
        },
        'es': {
            'name': 'Spanish',
            'flag': '🇪🇸',
            'greeting': '¡Hola! Puedo ayudarte en español.',
            'tts_code': 'es',
            'stt_code': 'es-ES'
        },
        'fr': {
            'name': 'French',
            'flag': '🇫🇷',
            'greeting': 'Bonjour! Je peux vous aider en français.',
            'tts_code': 'fr',
            'stt_code': 'fr-FR'
        }
    }
    
    # Speech Settings
    STT_ENGINE = "google"
    TTS_ENGINE = "gtts"
    LISTEN_TIMEOUT = 5
    PHRASE_TIME_LIMIT = 15
    
    # LLM Settings
    MAX_TOKENS = 500
    TEMPERATURE = 0.7
    MAX_CONVERSATION_HISTORY = 10