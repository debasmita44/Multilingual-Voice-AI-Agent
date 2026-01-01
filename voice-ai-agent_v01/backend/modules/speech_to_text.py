import speech_recognition as sr
from typing import Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpeechToText:
    """Speech-to-Text for 4 languages: English, Hindi, Spanish, French"""
    
    def __init__(self, engine: str = "google"):
        self.engine = engine
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 3000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 1.0
        logger.info("✅ STT initialized (EN, HI, ES, FR)")
    
    def listen(self, timeout: int = 5, phrase_time_limit: int = 15) -> Optional[sr.AudioData]:
        """Listen to microphone"""
        try:
            with sr.Microphone() as source:
                logger.info("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1.5)
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                logger.info("✅ Audio captured")
                return audio
        except sr.WaitTimeoutError:
            logger.warning("⏱️ Timeout")
            return None
        except Exception as e:
            logger.error(f"❌ Listen error: {e}")
            return None
    
    def transcribe(self, audio: sr.AudioData, language_hint: str = None) -> Tuple[Optional[str], Optional[str]]:
        """Transcribe audio to text"""
        if audio is None:
            return None, None
        
        try:
            # Try 4 supported languages in priority order
            languages_to_try = [
                ('en-US', 'en'),
                ('hi-IN', 'hi'),
                ('es-ES', 'es'),
                ('fr-FR', 'fr')
            ]
            
            # If hint provided, try it first
            if language_hint:
                try:
                    text = self.recognizer.recognize_google(audio, language=language_hint)
                    if text:
                        logger.info(f"✅ Transcribed with hint: {text}")
                        return text, language_hint.split('-')[0]
                except:
                    pass
            
            # Try each language
            for lang_code, short_code in languages_to_try:
                try:
                    text = self.recognizer.recognize_google(audio, language=lang_code)
                    if text and len(text.strip()) > 0:
                        logger.info(f"✅ Transcribed ({lang_code}): {text}")
                        return text, short_code
                except:
                    continue
            
            # Auto-detect as last resort
            text = self.recognizer.recognize_google(audio)
            logger.info(f"✅ Transcribed (auto): {text}")
            return text, None
            
        except sr.UnknownValueError:
            logger.warning("❌ Could not understand")
            return None, None
        except Exception as e:
            logger.error(f"❌ Transcribe error: {e}")
            return None, None
    
    def listen_and_transcribe(self, language_hint: str = None, timeout: int = 5) -> Tuple[Optional[str], Optional[str]]:
        """Combined listen and transcribe"""
        audio = self.listen(timeout=timeout)
        return self.transcribe(audio, language_hint)