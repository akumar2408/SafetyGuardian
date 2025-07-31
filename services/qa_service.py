"""
Production-ready question answering and summarization service for
SafetyGuardian.

This service preloads Hugging Face transformers pipelines for
question answering and summarization.  Clients can submit questions
with a context string to receive an answer grounded in that context.
They can also submit arbitrary text to receive a concise summary.
Configuration of the underlying models can be overridden through
environment variables (QA_MODEL and SUMMARIZATION_MODEL).
"""
import logging
import os
from typing import Any, Dict

from flask import Flask, jsonify, request
from transformers import pipeline

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Preload transformers pipelines.  Models can be customised via
# environment variables to allow experimentation without code changes.
QA_MODEL_NAME = os.getenv("QA_MODEL", "distilbert-base-uncased-distilled-squad")
SUM_MODEL_NAME = os.getenv("SUMMARIZATION_MODEL", "facebook/bart-large-cnn")

try:
    qa_pipeline = pipeline("question-answering", model=QA_MODEL_NAME)
    logger.info("Loaded QA model %s", QA_MODEL_NAME)
except Exception as exc:
    logger.exception("Failed to load QA model %s", QA_MODEL_NAME)
    raise

try:
    summarizer = pipeline("summarization", model=SUM_MODEL_NAME)
    logger.info("Loaded summarization model %s", SUM_MODEL_NAME)
except Exception as exc:
    logger.exception("Failed to load summarization model %s", SUM_MODEL_NAME)
    raise


@app.route('/qa', methods=['POST'])
def qa() -> Any:
    """Answer a question based on provided context.

    Payload must include ``question`` and ``context``.  The context
    should contain the information needed to answer the question.
    """
    data: Dict[str, Any] = request.get_json() or {}
    question = data.get('question')
    context = data.get('context')
    if not question or not context:
        msg = "Both 'question' and 'context' fields are required."
        logger.warning(msg)
        return jsonify({'error': msg}), 400
    try:
        result = qa_pipeline(question=question, context=context)
        answer = result.get('answer', '')
        return jsonify({'answer': answer})
    except Exception:
        logger.exception("QA model error")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/summarize', methods=['POST'])
def summarize() -> Any:
    """Summarize a block of text.

    Expects a ``text`` field in the request JSON.  Returns a
    summarised version of the text.  The summary length is
    automatically determined by the model; longer inputs will produce
    longer summaries.
    """
    data: Dict[str, Any] = request.get_json() or {}
    text = data.get('text')
    if not text:
        msg = "Field 'text' is required."
        logger.warning(msg)
        return jsonify({'error': msg}), 400
    try:
        # The summarizer can handle long documents by truncating and
        # splitting.  Use do_sample=False for deterministic output.
        result = summarizer(text, max_length=200, min_length=30, do_sample=False)
        summary = result[0]['summary_text'] if result else ''
        return jsonify({'summary': summary})
    except Exception:
        logger.exception("Summarization error")
        return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5003)))