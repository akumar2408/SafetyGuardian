"""
Production-ready vision service for SafetyGuardian.

This Flask application exposes an endpoint for object detection using
Hugging Face transformers.  At startup it preloads an object detection
pipeline so that each request can be served quickly.  Requests can
provide either a remote URL to an image or a base64-encoded payload.
Errors are logged and a clear error message is returned to the client.
"""
import base64
import logging
import os
from io import BytesIO
from typing import Any, Dict, List

import requests
from PIL import Image
from flask import Flask, jsonify, request
from transformers import pipeline

# Configure basic logging.  In production you might route this to
# structured log aggregation like ELK or Datadog.
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load the detection model once at import time.  The model name can
# be overridden via the VISION_MODEL environment variable.  The
# default model is facebook/detr-resnet-50 which balances accuracy
# and performance.  Loading at import means subsequent requests will
# reuse the same model instance.
MODEL_NAME = os.getenv("VISION_MODEL", "facebook/detr-resnet-50")
try:
    detector = pipeline("object-detection", model=MODEL_NAME)
    logger.info("Loaded vision model %s", MODEL_NAME)
except Exception as exc:
    logger.exception("Failed to load vision model %s", MODEL_NAME)
    raise


def _load_image(data: Dict[str, Any]) -> Image.Image:
    """Load an image from a base64-encoded string or remote URL.

    Args:
        data: Request JSON payload.

    Returns:
        PIL Image object.

    Raises:
        ValueError: If no image is provided or the image cannot be loaded.
    """
    # Base64 input takes priority
    b64 = data.get("image_base64")
    if b64:
        try:
            decoded = base64.b64decode(b64)
            return Image.open(BytesIO(decoded)).convert("RGB")
        except Exception as e:
            raise ValueError(f"Invalid base64 image: {e}")

    url = data.get("image_url")
    if not url:
        raise ValueError("An 'image_url' or 'image_base64' field is required.")
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return Image.open(BytesIO(resp.content)).convert("RGB")
    except Exception as e:
        raise ValueError(f"Failed to fetch image from URL: {e}")


@app.route("/detect", methods=["POST"])
def detect() -> Any:
    """Detect objects in an image.

    The expected payload is a JSON object with one of the following
    fields:

    * ``image_url`` – a publicly accessible URL to an image.
    * ``image_base64`` – a base64‐encoded representation of the image.

    Returns a JSON object containing a list of detections.  Each
    detection includes a label and a confidence score between 0 and 1.
    """
    data = request.get_json() or {}
    try:
        img = _load_image(data)
        results = detector(img)
        detections: List[Dict[str, Any]] = [
            {"label": r["label"], "score": float(r["score"])} for r in results
        ]
        return jsonify({"detections": detections})
    except ValueError as ve:
        logger.warning("Bad request: %s", ve)
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.exception("Unexpected error during detection")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    # When running directly (not under gunicorn), default to port 5001.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))