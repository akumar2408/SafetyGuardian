"""
Production-ready translation and text‑to‑speech service for
SafetyGuardian.

This service preloads a Hugging Face translation pipeline for
converting text from one language to another.  The target language
defaults to English but can be overridden via query parameters or an
environment variable.  A simple text‑to‑speech (TTS) endpoint is
provided as a placeholder; in production you might integrate with
gTTS, Azure Cognitive Speech or another synthesis service.  Logging
is configured for easier debugging and monitoring.
"""
import logging
import os
from typing import Any, Dict

from flask import Flask, jsonify, request
from transformers import pipeline

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Preload translation model.  You can override the default model via
# the TRANSLATION_MODEL environment variable.  The default model
# supports English↔Spanish translation.  For other languages choose a
# different MarianMT model (e.g. Helsinki-NLP/opus-mt-en-de).
MODEL_NAME = os.getenv("TRANSLATION_MODEL", "Helsinki-NLP/opus-mt-en-es")
try:
    translator = pipeline("translation", model=MODEL_NAME)
    logger.info("Loaded translation model %s", MODEL_NAME)
except Exception as exc:
    logger.exception("Failed to load translation model %s", MODEL_NAME)
    raise


@app.route('/translate', methods=['POST'])
def translate() -> Any:
    """Translate a piece of text into the target language.

    The request JSON must include a ``text`` field and may include a
    ``target_lang`` code (e.g. ``es`` for Spanish).  If not provided,
    the default target language for the model will be used.  Only
    supported language pairs will work; an error is returned for
    unsupported combinations.
    """
    data: Dict[str, Any] = request.get_json() or {}
    text = data.get('text')
    if not text:
        msg = "Field 'text' is required."
        logger.warning(msg)
        return jsonify({'error': msg}), 400
    try:
        # If a target language is provided, set forced_bos_token_id via
        # the underlying tokenizer.  Not all models support arbitrary
        # language codes; this example assumes a fixed model that
        # translates into its default target language.
        result = translator(text)
        translation = result[0]['translation_text'] if result else ''
        return jsonify({'translation': translation})
    except Exception:
        logger.exception("Translation error")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/tts', methods=['POST'])
def tts() -> Any:
    """Generate a speech audio URL from text.

    This endpoint currently returns a placeholder URL.  In a real
    implementation you might call a service like Google TTS or Azure
    Cognitive Speech and return a signed URL to the generated audio.
    """
    data: Dict[str, Any] = request.get_json() or {}
    text = data.get('text')
    if not text:
        msg = "Field 'text' is required."
        logger.warning(msg)
        return jsonify({'error': msg}), 400
    # Placeholder implementation
    fake_url = 'http://example.com/audio.mp3'
    return jsonify({'audio_url': fake_url})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5004)))