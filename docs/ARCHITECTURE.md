# CSE ASPIRANT – SYSTEM ARCHITECTURE

## 1. Overview

**CSE ASPIRANT** is a next-generation distributed Telegram bot and educational academy engineered for high concurrency, ultra-low-latency audio streaming, and bilingual learning (Hindi & English).

```mermaid
flowchart TD
    User([Telegram User / Group]) -->|Commands / Callbacks| TG[Telegram API Gateway]
    TG -->|Long Polling / Webhook| BotEngine[Python AsyncIO Bot Client]
    
    subgraph Core Services
        BotEngine --> Router[Multi-Prefix Command Router]
        Router --> Moderation[Security & Anti-Spam / Anti-Flood]
        Router --> MusicMgr[Multi-Group Music Manager]
        Router --> EduMgr[CSE Aspirant Academy]
        Router --> ProgMgr[Programming Academy]
        Router --> AIMgr[AI Inference Engine]
        Router --> PayMgr[Payment & UTR Reconciliation]
    end

    subgraph Audio Subsystem
        MusicMgr -->|HTTP / JSON RPC| GoEngine[Golang High-Performance Music Engine]
        GoEngine --> Transcoder[Transcoding & RingBuffer Worker Pool]
        Transcoder --> StreamSink[Telegram Voice Chat / PCM Stream]
    end

    subgraph Data & Storage
        BotEngine --> Repo[Data Repository]
        FastAPI --> Repo
        Repo --> PG[(PostgreSQL 16)]
        Repo --> Redis[(Redis 7 Cache & Queues)]
    end

    subgraph NextGen API & Dashboard
        WebUser([Web Dashboard / Developer]) --> Dashboard[TypeScript Web UI]
        Dashboard --> FastAPI[FastAPI REST API]
        FastAPI --> KeyAuth[API Key & Tier Rate Limiter]
        KeyAuth --> BotEngine
    end
```

## 2. Component Breakdown

### 2.1 Python AsyncIO Core & Bot
- **Routing**: Multi-prefix parser supporting `/command`, `!command`, and `.command`.
- **Event Bus**: Asynchronous decoupling of chat events, state updates, and metrics collection.
- **Error Handling**: Custom exception hierarchy, exponential backoff retries, and circuit breakers.

### 2.2 Golang High-Performance Music Engine (`golang/`)
- **Worker Pool**: 8 parallel workers processing audio transcodes and ring buffer allocations.
- **Safe Recovery**: Panic-safe goroutines with automatic recovery middleware on HTTP handlers.
- **Ring Buffer**: Thread-safe in-memory audio chunk caching to withstand network packet jitter.

### 2.3 NextGen FastAPI Server (`api/`)
- **Authentication**: `X-API-Key` headers enforcing tier-based rate limits (FREE: 10/min, PREMIUM: 100/min, PRO: 1000/min). Master owner bypass for administrative control.
- **Telemetry**: Prometheus-compatible metric exposition at `/metrics` and system health at `/health`.

### 2.4 Persistence Layer
- **PostgreSQL**: Production relational schema storing user records, active subscriptions, UTR records, and group settings.
- **Redis**: Low-latency cache, sliding-window rate limiters, session stores.
- **Graceful Fallback**: Automatically operates on in-memory storage if database services are temporarily offline.

