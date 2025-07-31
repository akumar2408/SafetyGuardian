"""
Vision service for SafetyGuardian.

This Flask application exposes an endpoint for object detection. In a
production deployment it would load a Hugging Face transformer or a
custom model (e.g. YOLOv8, SigLIP or similar) to detect safety gear
and hazards. For this skeleton, it returns a static list of
detections.
"""
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/detect', methods=['POST'])
def detect():
    """Detect objects in an image.

    Expected JSON payload:
    {
      "image_url": "http://..."   # or base64 encoded image
    }

    Returns:
    {
      "detections": ["helmet", "vest"]
    }
    """
    data = request.get_json() or {}
    image_url = data.get('image_url')
    # TODO: download and run detection model on image_url
    detections = ['helmet', 'vest']
    return jsonify({'detections': detections})


if __name__ == '__main__':
    # Bind to all interfaces so Docker can expose the port.
    app.run(host='0.0.0.0', port=5001)
