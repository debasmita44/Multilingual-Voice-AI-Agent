from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import logging
from config import Config
from modules import LanguageDetector, LLMHandler, TextToSpeech

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow all origins for development

# Initialize modules
detector = LanguageDetector()
llm = LLMHandler()
tts = TextToSpeech()

# Conversation storage
conversations = {}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check"""
    try:
        ollama_status = llm.test_connection()
        return jsonify({
            'status': 'ok',
            'ollama_connected': ollama_status,
            'supported_languages': Config.SUPPORTED_LANGUAGES
        })
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Get supported languages"""
    return jsonify({
        'languages': Config.SUPPORTED_LANGUAGES
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Process chat message"""
    try:
        data = request.json
        user_message = data.get('message')
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        logger.info(f"📩 Received: {user_message}")
        
        # Detect language
        detected_lang = detector.detect_language(user_message)
        logger.info(f"🌐 Language: {detected_lang}")
        
        # Get conversation history
        if session_id not in conversations:
            conversations[session_id] = []
        
        history = conversations[session_id]
        
        # Get AI response
        response = llm.get_response(
            query=user_message,
            language=detected_lang,
            context=history
        )
        
        if not response:
            return jsonify({'error': 'Failed to get response'}), 500
        
        logger.info(f"💬 Response: {response}")
        
        # Update history
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": response})
        
        if len(history) > 20:
            conversations[session_id] = history[-20:]
        
        return jsonify({
            'response': response,
            'language': detected_lang,
            'language_name': detector.get_language_name(detected_lang)
        })
        
    except Exception as e:
        logger.error(f"❌ Chat error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/speak', methods=['POST'])
def speak():
    """Generate speech"""
    try:
        data = request.json
        text = data.get('text')
        language = data.get('language', 'en')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        audio_path = tts.generate_audio(text, language)
        
        if not audio_path:
            return jsonify({'error': 'Failed to generate audio'}), 500
        
        response = send_file(
            audio_path,
            mimetype='audio/mpeg',
            as_attachment=False
        )
        
        @response.call_on_close
        def cleanup():
            try:
                os.unlink(audio_path)
            except:
                pass
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Speak error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    """Reset conversation"""
    try:
        data = request.json
        session_id = data.get('session_id', 'default')
        
        if session_id in conversations:
            conversations[session_id] = []
        
        return jsonify({'status': 'reset'})
        
    except Exception as e:
        logger.error(f"❌ Reset error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("🚀 Starting Multilingual Voice AI Server")
    logger.info("=" * 60)
    logger.info(f"Languages: English, Hindi, Spanish, French")
    logger.info(f"Server: http://{Config.FLASK_HOST}:{Config.FLASK_PORT}")
    logger.info("=" * 60)
    
    if not llm.test_connection():
        logger.warning("⚠️  Ollama not connected!")
        logger.warning("    Start with: ollama serve")
    else:
        logger.info("✅ Ollama connected")
    
    app.run(
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        debug=True
    )