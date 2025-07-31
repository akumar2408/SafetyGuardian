"""
Production-ready audio service for SafetyGuardian.

This Flask application provides endpoints for classifying audio events
and converting speech to text.  It preloads Hugging Face pipelines
for audio classification and automatic speech recognition (ASR) at
startup so that requests can be handled efficiently.  Clients can
upload audio via a remote URL or base64 string.  Errors are handled
gracefully and logged.
"""
import base64
import logging
import os
from io import BytesIO
from typing import Any, Dict, List

import numpy as np
import requests
import soundfile as sf
from flask import Flask, jsonify, request
from transformers import pipeline


logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Preload models.  Environment variables can override the default
# models used for classification and ASR.  Loading at module import
# time ensures that subsequent requests do not pay the startup cost.
AUDIO_CLASS_MODEL = os.getenv("AUDIO_CLASS_MODEL", "superb/hubert-large-superb-ks")
ASR_MODEL = os.getenv("ASR_MODEL", "openai/whisper-small")

try:
    classifier = pipeline("audio-classification", model=AUDIO_CLASS_MODEL)
    logger.info("Loaded audio classification model %s", AUDIO_CLASS_MODEL)
except Exception as exc:
    logger.exception("Failed to load audio classification model %s", AUDIO_CLASS_MODEL)
    raise

try:
    asr_pipeline = pipeline("automatic-speech-recognition", model=ASR_MODEL)
    logger.info("Loaded ASR model %s", ASR_MODEL)
except Exception as exc:
    logger.exception("Failed to load ASR model %s", ASR_MODEL)
    raise


def _load_audio(data: Dict[str, Any]) -> np.ndarray:
    """Load audio data from a base64 string or remote URL.

    Returns a 1D numpy array of samples at the sample rate expected by
    the model (16 kHz for Whisper).  If the audio is stereo it is
    converted to mono.
    """
    if 'audio_base64' in data:
        try:
            decoded = base64.b64decode(data['audio_base64'])
            buf = BytesIO(decoded)
            samples, sr = sf.read(buf)
        except Exception as e:
            raise ValueError(f"Invalid base64 audio: {e}")
    else:
        url = data.get('audio_url')
        if not url:
            raise ValueError("An 'audio_url' or 'audio_base64' field is required.")
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            samples, sr = sf.read(BytesIO(resp.content))
        except Exception as e:
            raise ValueError(f"Failed to fetch audio from URL: {e}")
    # Convert to mono
    if samples.ndim > 1:
        samples = np.mean(samples, axis=1)
    return samples.astype(np.float32)


@app.route('/classify_audio', methods=['POST'])
def classify_audio() -> Any:
    """Classify an uploaded audio sample into event types.

    The payload must include either ``audio_url`` (pointing to a remote
    audio file) or ``audio_base64`` (a base64 encoded WAV/FLAC/OGG
    file).  Returns the top predicted event along with its score.
    """
    data = request.get_json() or {}
    try:
        samples = _load_audio(data)
        results = classifier(samples, sampling_rate=16000)
        # Return the top 3 labels with scores for richness
        top_events: List[Dict[str, Any]] = [
            {"label": r['label'], "score": float(r['score'])}
            for r in results[:3]
        ]
        return jsonify({"events": top_events})
    except ValueError as ve:
        logger.warning("Bad request: %s", ve)
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.exception("Audio classification error")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/asr', methods=['POST'])
def asr() -> Any:
    """Convert speech to text using a preloaded ASR model.

    Payload must include ``audio_url`` or ``audio_base64``.  Returns
    the transcript as a string.
    """
    data = request.get_json() or {}
    try:
        samples = _load_audio(data)
        result = asr_pipeline(samples, sampling_rate=16000)
        transcript = result.get("text", "")
        return jsonify({"transcript": transcript})
    except ValueError as ve:
        logger.warning("Bad request: %s", ve)
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.exception("ASR error")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5002)))