# CSE ASPIRANT – NEXTGEN API GUIDE

The **NextGen API** provides RESTful endpoints to manage bot music playback, query academy resources, submit payments, and generate developer API keys.

## Base URL
- Production: `http://localhost:8000` (or `https://api.yourdomain.com`)
- Interactive OpenAPI Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Authentication

All protected endpoints require an API key passed via the `X-API-Key` HTTP header:

```http
X-API-Key: csea_pro_xxxxxxxxxxxxxxxxxxxx
```

### Rate Limits by Tier
| Tier | Quota (Requests / Minute) | Max Music Queue |
| :--- | :--- | :--- |
| **FREE** | 10 | 15 tracks |
| **PREMIUM** | 100 | 100 tracks |
| **PRO** | 1000 | 500 tracks |
| **OWNER / SUDO** | Unlimited (Bypass) | Unlimited |

---

## Key Endpoints

### 1. Health & Metrics
- `GET /health` : Returns complete system diagnostics, CPU/RAM, and database statuses.
- `GET /metrics` : Prometheus-formatted counters and gauges.

### 2. API Key Management
- `POST /api/v1/keys/generate`
  - Body: `{"user_id": 123456, "tier": "PRO"}`
  - Response: `{"success": true, "data": {"key": "csea_pro_..."}}`
- `POST /api/v1/keys/revoke`
  - Body: `{"key": "csea_pro_..."}`

### 3. Music Control
- `POST /api/v1/music/play`
  - Body: `{"chat_id": -100123456, "query_or_url": "Lofi Study Beats", "requester_id": 123}`
- `POST /api/v1/music/pause/{chat_id}`
- `POST /api/v1/music/resume/{chat_id}`
- `POST /api/v1/music/skip/{chat_id}`
- `GET /api/v1/music/status/{chat_id}`

### 4. Education & Academy
- `GET /api/v1/education/summary?lang=en` : Academy dashboard summary.
- `GET /api/v1/education/upsc/strategy?lang=hi` : Bilingual UPSC preparation blueprint.
- `GET /api/v1/education/cs/{subject}?lang=en` : Core computer science overviews (`os`, `dbms`, `cn`, `dsa`).
- `GET /api/v1/education/quiz/random` : Interactive mock question with answer keys.
- `GET /api/v1/education/planner?exam=UPSC&hours=8&lang=en` : Automated study timetable.

### 5. Payments & UTR Reconciliation
- `GET /api/v1/payments/invoice/{user_id}?plan=PREMIUM&amount=199` : Generates dynamic UPI intent and NEFT instructions.
- `POST /api/v1/payments/submit`
  - Body: `{"user_id": 123456, "utr": "421098234812", "amount": 199.0, "method": "UPI"}`

