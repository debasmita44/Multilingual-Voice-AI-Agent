from gtts import gTTS
import logging
import tempfile
import os
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextToSpeech:
    """Enhanced Text-to-Speech with natural voices"""
    
    def __init__(self):
        logger.info("✅ Enhanced TTS initialized (EN, HI, ES, FR)")
    
    def generate_audio(self, text: str, language: str = "en") -> Optional[str]:
        """Generate natural-sounding audio"""
        if not text or not text.strip():
            logger.warning("⚠️ No text to speak")
            return None
        
        try:
            # Enhanced language mapping with regional accents
            lang_settings = {
                'en': {
                    'lang': 'en',
                    'tld': 'com',         # US accent
                    'slow': False
                },
                'hi': {
                    'lang': 'hi',
                    'tld': 'co.in',       # Indian accent
                    'slow': False
                },
                'es': {
                    'lang': 'es',
                    'tld': 'es',          # Spain accent
                    'slow': False
                },
                'fr': {
                    'lang': 'fr',
                    'tld': 'fr',          # France accent
                    'slow': False
                }
            }
            
            settings = lang_settings.get(language, lang_settings['en'])
            
            logger.info(f"🔊 Generating natural speech in {settings['lang']}...")
            
            # Create TTS with regional accent
            tts = gTTS(
                text=text,
                lang=settings['lang'],
                slow=settings['slow'],
                tld=settings['tld']
            )
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tts.save(temp_file.name)
            temp_file.close()
            
            logger.info(f"✅ Natural audio generated: {temp_file.name}")
            return temp_file.name
            
        except Exception as e:
            logger.error(f"❌ TTS error: {e}")
            return None