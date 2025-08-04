# SafetyGuardian

> **Construction‑site safety, super‑charged by AI.** SafetyGuardian is a full‑stack platform that captures video, audio and IoT sensor data in real‑time, detects hazards with state‑of‑the‑art multimodal models, and alerts the people that can act on them—instantly.

---

## ✨ What’s inside

| Layer                                 | Tech                                                                                              | Purpose                                                                                          |
| ------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| **Frontend**                          | React + Vite + Tailwind CSS                                                                       | Interactive dashboard, live camera feeds, alert timeline, analytics and project management pages |
| **API Gateway**                       | **Go Fiber**                                                                                      | Auth, rate‑limiting, request fan‑out, WebSocket push                                             |
| **Micro‑services (Python + FastAPI)** | Vision, Audio, Speech‑to‑Text, QA/Summarisation, Translation, Text‑to‑Speech, Safety‑Rules Engine | Each service runs a Hugging Face model and exposes a gRPC & REST interface                       |
| **Messaging**                         | NATS JetStream                                                                                    | Low‑latency event bus connecting gateway, workers & notification service                         |
| **Data**                              | PostgreSQL + Redis                                                                                | Persist incidents & user data, cache model artefacts                                             |
| **DevOps**                            | Docker Compose • GitHub Actions • Traefik                                                         | One‑command local stack & zero‑downtime cloud deploys                                            |

---

## 🚀 Quick start

> Prerequisites: **Docker Desktop ≥ 24**, **docker‑compose v2**, **Node.js ≥ 20** (only if you plan to hack on the frontend).

```bash
# 1 — clone
$ git clone https://github.com/akumar2408/SafetyGuardian.git && cd SafetyGuardian

# 2 — spin everything up (gateway, services, DB, dashboard…)
$ docker compose --profile full up --build

# 3 — open the app
# Backend API  → http://localhost:8080
# React UI     → http://localhost:5173
```

### Local development

| Task                  | Command                                     |
| --------------------- | ------------------------------------------- |
| Hot‑reload Go gateway | `air` (inside `backend-go/`)                |
| Run a Python service  | `uvicorn services/vision/main:app --reload` |
| Frontend dev server   | `pnpm dev` (inside `frontend/`)             |
| Unit tests            | `pnpm test` & `go test ./...`               |

Create a `.env` file at the repo root (see `.env.example`) to override defaults such as database URL or Hugging Face tokens.

---

## 🗺️  Architecture

```
┌────────────┐           (WebSocket)            ┌────────────────┐
│  React UI  │  ←──── real‑time alerts ───────  │ Notification   │
└─────▲──────┘                                   │  Service (TS) │
      │REST                                      └────────────────┘
      │/ws                                               ▲
┌─────┴──────┐   gRPC/NATS        ┌────────────────┐     │Email/SMS
│  Go Gateway│  ───────────────▶ │  Safety Rules  │◀────┘
└─────▲──────┘                    │   Engine       │
      │REST                       └────────────────┘
      │                       gRPC▲  gRPC▲   gRPC▲
      │REST                        │     │       │
┌─────┴────────┐   gRPC           │     │       │
│ Vision Svc   │◀───────────────┐ │     │       │
└──────────────┘                │ │     │       │
┌──────────────┐   gRPC         │ │     │       │
│ Audio  Svc   │◀───────────────┘ │     │       │
└──────────────┘                  │     │       │
┌──────────────┐   gRPC           │     │       │
│ ASR   Svc    │◀─────────────────┘     │       │
└──────────────┘                        │       │
┌──────────────┐   gRPC                 │       │
│ QA  Svc      │◀───────────────────────┘       │
└──────────────┘                                │
┌──────────────┐   gRPC                         │
│ TTS  Svc     │◀───────────────────────────────┘
└──────────────┘
```

*Every box is a container—deploy the same stack on any orchestrator that speaks OCI.*

---

## 🔑 Authentication

| Endpoint                     | Description                    |
| ---------------------------- | ------------------------------ |
| `POST /api/auth/register`    | Create user (email + password) |
| `POST /api/auth/login`       | JWT login                      |
| `POST /api/auth/refresh`     | Rotate tokens                  |
| `POST /api/auth/2fa/request` | Send TOTP QR code              |
| `POST /api/auth/2fa/verify`  | Enable / challenge 2FA         |

All protected routes expect `Authorization: Bearer <access‑token>`.

---

## 📡 API Reference (selection)

### Vision

| Method | Route         | Body                   | Response                                                  |
| ------ | ------------- | ---------------------- | --------------------------------------------------------- |
| `POST` | `/api/detect` | multipart‑form `image` | `[ {"label":"hard‑hat","bbox":[...],"score":0.98}, ... ]` |

### Audio

\| `POST /api/classify_audio` | `{ "wav": <base64> }` → `[ { "event":"glass_break","score":0.91 } ]` |

### Multimodal QA

\| `POST /api/qa` | `{ "context": "…", "question": "…" }` → `{ "answer": "…" }` |

More endpoints: `/api/summarize`, `/api/translate`, `/api/tts`, `/api/asr`, `/api/alerts/live` (WebSocket) and `/api/alerts/history`.

---

## 🖥️  Frontend screenshots

| Dashboard                                    | Incident Details                       |
| -------------------------------------------- | -------------------------------------- |
| ![dashboard](docs/screenshots/dashboard.png) | ![detail](docs/screenshots/detail.png) |

---

## 🛠️  Built‑with

* Go 1.22 · Fiber · Zap
* Python 3.12 · FastAPI · Transformers · Torch
* React 18 · Vite · TanStack Query · Tailwind CSS · DaisyUI
* PostgreSQL · Redis · NATS · Docker Compose

---

## 📦  Deployment

* **Local** – `docker compose up` spins up everything.
* **Production (one‑liner)** – `docker stack deploy -c docker-compose.prod.yml safetyguardian` (tested on a 1‑node Swarm & AWS ECS).
* **Updates** – CI builds & pushes version‑tagged images; CD job rolls them out with zero downtime.

---

## 🧑‍💻 Contributing

1. Fork 💫 & `git clone …`
2. `pnpm i && go mod download`
3. Create your branch: `git checkout -b feat/amazing`
4. Commit with Conventional Commits
5. `pnpm test && go test ./...`
6. Open a PR 📬

All PRs run: lint ➜ tests ➜ Docker build ➜ preview deploy.

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more info.

---

## 🤝 Acknowledgements

* Hugging Face community & model authors
* NATS.io for the blazing‑fast JetStream
* All beta testers who reported issues 🙏

---

> © 2025 Aayush Kumar. Made with ☕ & 💡 in Phoenix, AZ.

