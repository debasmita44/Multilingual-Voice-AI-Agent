from langdetect import detect, detect_langs, DetectorFactory
from typing import Optional
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DetectorFactory.seed = 0

class LanguageDetector:
    """Language detector for 4 languages: English, Hindi, Spanish, French"""
    
    def __init__(self):
        self.supported_languages = {
            'en': 'English',
            'hi': 'Hindi',
            'es': 'Spanish',
            'fr': 'French'
        }
        
        self.language_hints = {
            'hi': [
                'kya', 'kaise', 'kaun', 'kahan', 'aap', 'tum', 'mai', 'mein',
                'hoon', 'hai', 'hain', 'ka', 'ke', 'ki', 'ko', 'se',
                'और', 'का', 'के', 'में', 'है', 'हैं', 'को', 'से',
                'theek', 'accha', 'ji'
            ],
            'en': [
                'the', 'is', 'are', 'was', 'were', 'have', 'has',
                'what', 'how', 'who', 'where', 'when', 'why',
                'you', 'i', 'we', 'can', 'hello', 'hi', 'yes', 'no'
            ],
            'es': [
                'el', 'la', 'los', 'las', 'es', 'son', 'qué', 'cómo',
                'quien', 'dónde', 'tú', 'yo', 'hola', 'sí', 'no'
            ],
            'fr': [
                'le', 'la', 'les', 'est', 'sont', 'comment', 'qui',
                'quoi', 'où', 'vous', 'je', 'bonjour', 'oui', 'non'
            ]
        }
        
        logger.info("✅ Language Detector initialized")
    
    def detect_language(self, text: str) -> str:
        """Detect language with fallback to English"""
        if not text or len(text.strip()) < 2:
            return 'en'
        
        text_clean = text.strip()
        
        # Check for Devanagari (Hindi)
        if re.search('[\u0900-\u097F]', text_clean):
            logger.info("🌐 Detected: Hindi (script)")
            return 'hi'
        
        # Check keywords
        hint_lang = self._detect_by_hints(text_clean.lower())
        if hint_lang:
            logger.info(f"🌐 Detected: {self.supported_languages[hint_lang]} (keywords)")
            return hint_lang
        
        # Use library
        try:
            langs = detect_langs(text_clean)
            if langs:
                detected = langs[0].lang
                if detected in self.supported_languages and langs[0].prob >= 0.7:
                    logger.info(f"🌐 Detected: {self.supported_languages[detected]} (library)")
                    return detected
        except:
            pass
        
        logger.info("🌐 Defaulting to English")
        return 'en'
    
    def _detect_by_hints(self, text: str) -> Optional[str]:
        words = text.split()
        scores = {}
        
        for lang, keywords in self.language_hints.items():
            matches = sum(1 for word in words if word in keywords)
            if matches > 0:
                scores[lang] = matches
        
        if scores:
            return max(scores, key=scores.get)
        return None
    
    def get_language_name(self, lang_code: str) -> str:
        return self.supported_languages.get(lang_code, "English")