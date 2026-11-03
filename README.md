# CSE ASPIRANT – NEXTGEN MUSIC BOT 🚀

A state-of-the-art Telegram Music Bot and Academic Ecosystem built from scratch for Computer Science & UPSC Aspirants.

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Golang](https://img.shields.io/badge/Golang-1.22-00ADD8.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-NextGen-009688.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)
![Redis](https://img.shields.io/badge/Redis-7-DC382D.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5.4-3178C6.svg)
![Docker](https://img.shields.io/badge/Docker-VPS_Ready-2496ED.svg)

---

## 🌟 Key Capabilities

### 1. 🎵 High-Performance Music Engine
- **Powered by Golang**: Worker pool and ring buffers for ultra-low latency audio transcoding and streaming.
- **Full Player Suite**: Play, Pause, Resume, Skip, Previous, Stop, Queue, Shuffle, Repeat (OFF/ONE/ALL), Volume (0-200), and Playlists.
- **Multi-Group Isolation**: Manages independent playback states across any number of Telegram groups concurrently.
- **Auto-Reconnect & Recovery**: Automatic audio stream recovery from network jitter.

### 2. 📚 CSE Aspirant Academy (Bilingual: Hindi & English)
- **UPSC Civil Services Preparation**: Prelims, CSAT, Mains GS 1 to 4 syllabus blueprints and strategies.
- **Core Computer Science**: Operating Systems, DBMS, Computer Networks, and DSA.
- **NCERT Foundation**: History, Geography, Polity, Economics summaries (Classes 6–12).
- **Current Affairs & PYQs**: High-yield daily digests and previous year exam questions with model answers.
- **Interactive Quizzes & Study Planner**: Daily mock tests and customizable Pomodoro timetables.

### 3. 💻 Programming Academy
- In-depth tracks for: **Python, Golang, C, C++, Java, and JavaScript**.
- Every lesson includes bilingual explanations, working code snippets, output, hands-on exercises, and quizzes.

### 4. 🤖 NextGen AI System
- Intelligent chatbot, academic Q&A solver, automated code generator, code debugger, step-by-step mathematics solver, and notes summarizer.

### 5. ⚡ NextGen REST API
- Powered by FastAPI with OpenAPI Swagger documentation at `/docs`.
- API Key creation, tier enforcement, and real-time usage analytics.
- Prometheus metrics at `/metrics` and diagnostics at `/health`.

### 6. 💎 Premium & Multi-Method Payments
- Tier structure: **FREE**, **PREMIUM** (₹199), and **PRO** (₹499).
- Supports **UPI, NEFT, and Cards**.
- 12-digit UTR submission with duplicate transaction detection (replay protection).
- Owner approval workflow with automatic subscription activation and API key delivery to user DM.
- Social verification for Telegram group, Instagram, and YouTube.

### 7. 🛡 Robust Security & Moderation
- Anti-spam message velocity tracking and duplicate detection.
- Sliding window anti-flood protection.
- Toxic content, NSFW, and copyright filters.
- Malicious URL and suspicious file scanners (`.exe`, `.sh`, `.apk` rejection).
- Administrative audit logs and broadcast protections.

### 8. 🧭 Advanced Help UI & Multi-Prefix Support
- Supports prefixes: `/command`, `!command`, and `.command`.
- One-click **HELP** button categorizing commands into:
  - 🎵 MUSIC
  - 📚 EDUCATION
  - 💻 PROGRAMMING
  - 🤖 AI ASSISTANT
  - 💎 PREMIUM
  - 🔐 SECURITY
  - 📢 PROMOTION
  - 👑 OWNER PANEL

---

## 📂 Project Structure

```text
CSE-Aspirant/
├── main.py                     # Central startup & integration orchestrator
├── requirements.txt            # Python dependencies
├── core/                       # Configurations, logging, event bus, context
├── bot/                        # Telegram bot client, routers, handlers & callbacks
├── music/                      # Python music management & audio bridge
├── golang/                     # High-performance Go streaming engine & worker pool
├── api/                        # NextGen FastAPI server, schemas & route controllers
├── ui/                         # Modern TypeScript + HTML + CSS web dashboard
├── database/                   # PostgreSQL schema, connection pool & repository
├── ai/                         # Hybrid AI engine, math/code solvers & summarizer
├── education/                  # CSE Aspirant Academy (UPSC, CS, NCERT, Quizzes)
├── programming/                # Programming Academy (Python, Go, C, C++, Java, JS)
├── premium/                    # Tier policies, quota manager & social verification
├── payments/                   # UPI/NEFT gateway, UTR validation & activation
├── promotion/                  # Channel promotion requests & review workflows
├── security/                   # Anti-spam, anti-flood, URL & file scanners
├── moderation/                 # Admin moderation tools (kick, ban, warn)
├── welcome/                    # Welcome greeter & verification captcha
├── broadcast/                  # Rate-limited mass broadcast engine
├── error_handling/             # Dedicated Python/Go exceptions, retries & circuit breakers
├── monitoring/                 # Hardware telemetry, metrics & Prometheus exporter
├── tests/                      # Full test suite (100% verified)
├── deployment/                 # Dockerfile, docker-compose.yml, systemd & VPS scripts
└── docs/                       # Architecture, API guide, Bot commands & Deployment docs
```

---

## 🚀 Quick Start & Deployment

### Run via Docker Compose
```bash
cd deployment
cp .env.example .env
# Edit .env with your credentials
docker compose up -d --build
```

### Accessing Dashboards
- **Web Dashboard**: `http://localhost:3000`
- **FastAPI OpenAPI Docs**: `http://localhost:8000/docs`
- **Go Engine Health**: `http://localhost:8080/health`

---

## 📖 Documentation
- [Architecture & Diagrams](docs/ARCHITECTURE.md)
- [NextGen API Guide](docs/API_GUIDE.md)
- [Bot Commands Reference](docs/BOT_COMMANDS.md)
- [Educational Academy Manual](docs/EDUCATION_MANUAL.md)
- [Linux VPS Deployment Guide](docs/DEPLOYMENT.md)
- [Verification & Test Report](docs/TEST_REPORT.md)

---
*CSE ASPIRANT – Designed for High Performance, Education, and Scalability.*

