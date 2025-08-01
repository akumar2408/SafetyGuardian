# SafetyGuardian

SafetyGuardian is a proof‑of‑concept platform for monitoring
construction‑site safety using multimodal AI models. It demonstrates how
to integrate several Hugging Face tasks—object detection, audio
classification, question answering, translation, summarization and
text‑to‑speech—into a microservice architecture.

The project contains:

* **backend‑go** – a Go API gateway that exposes REST endpoints and
  proxies requests to the underlying Python services.
* **services/python** – a collection of Flask microservices for vision,
  audio, QA/summarization and translation/TTS. Each service is
  designed to load a Hugging Face model; at present they return stub
  responses.
* **docker‑compose.yml** – orchestrates the gateway and microservices
  using Docker.

## Quick start

Prerequisites:

* Docker and docker‑compose installed.

To build and run all services locally:

```bash
git clone https://github.com/akumar2408/SafetyGuardian.git
cd SafetyGuardian
docker-compose up --build
```

Once running, the API gateway will be available at `http://localhost:8080`.
The gateway exposes a sample endpoint `/api/detect` that forwards to
the vision service.

## Endpoints

This skeleton defines the following REST endpoints:

* `POST /api/detect` → returns a list of detected objects from an image.
* `POST /api/classify_audio` → returns detected audio events.
* `POST /api/asr` → transcribes speech to text.
* `POST /api/qa` → answers a question given a context.
* `POST /api/summarize` → summarizes a text.
* `POST /api/translate` → translates text into a target language.
* `POST /api/tts` → synthesizes speech from text.



