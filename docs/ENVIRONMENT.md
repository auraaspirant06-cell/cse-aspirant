# Environment Configuration

Yeh document project ke environment variables ka source-verified guide hai. Root `.env.example` ko copy karke `.env` banaiye. Existing `.env` ko kabhi overwrite na karein.

## Status ka matlab

- **IMPLEMENTED**: current source code variable ko read karta hai.
- **MISSING**: feature source mein hai, lekin environment setting abhi nahi hai.
- **PLANNED**: future integration ke liye documented placeholder hai; current code ise ignore karta hai.

## Simple Hindi Setup

1. Repository root mein command chalaiye:
   ```bash
   cp .env.example .env
   ```
2. `.env` mein sabse pehle Telegram values bhariye:
   - `BOT_TOKEN`: `@BotFather` se bot token.
   - `TELEGRAM_API_ID` aur `TELEGRAM_API_HASH`: `https://my.telegram.org` ke API development tools se.
   - `TELEGRAM_SESSION_STRING`: apne assistant user account ka Pyrogram session string. Isse kisi ke saath share na karein.
   - `OWNER_ID`: apna numeric Telegram user ID.
3. PostgreSQL aur Redis start karke `DATABASE_URL` aur `REDIS_URL` bhariye. Production mein strong database password aur TLS-enabled URLs use karein.
   Bundled Docker PostgreSQL ke liye `POSTGRES_USER`, `POSTGRES_PASSWORD`, aur `POSTGRES_DB` bhi bhariye; `DATABASE_URL` mein wahi user/password/database rakhiye.
4. Python bridge aur Go engine mein same `GO_ENGINE_TOKEN` rakhiye. `GO_ENGINE_URL` internal Go service URL aur `GO_ENGINE_PUBLIC_URL` users ke liye reachable URL hai. Docker runtime mein `FFMPEG_PATH=ffmpeg` rakhiye; Go startup is executable ko `PATH` mein check karta hai.
5. `MASTER_API_KEY` current master `X-API-Key` bypass ke liye dedicated secret hai. Isko locally generate karke replace karein:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(48))"
   ```
   `JWT_SECRET` ko API key ke roop mein reuse na karein; current project mein JWT implemented nahi hai.
6. Current manual UPI/NEFT/card invoice ke liye registered merchant/bank details bhariye. Razorpay, Stripe, PayU ya webhook credentials planned hain, implemented nahi.
7. `CORS_ORIGINS` mein sirf trusted website origins comma-separated format mein rakhiye, jaise `https://app.example.com`.
8. Tests chalaiye:
   ```bash
   pytest tests/test_config.py
   pytest
   cd golang && go test ./...
   ```

Docker Compose ke liye root se `docker compose --env-file .env -f deployment/docker-compose.yml up -d --build` chalaiye. Compose file root `.env` ko dono application containers mein pass karti hai.

## Manually Fill Karne Wali Values

Required implemented values:

- `BOT_TOKEN`
- `TELEGRAM_API_ID`
- `TELEGRAM_API_HASH`
- `TELEGRAM_SESSION_STRING`
- `OWNER_ID`
- `DATABASE_URL`
- `POSTGRES_PASSWORD`
- `REDIS_URL`
- `GO_ENGINE_URL`
- `GO_ENGINE_TOKEN`
- `MASTER_API_KEY`
- `PAYMENT_UPI_ID`
- `PAYMENT_MERCHANT_NAME`
- `PAYMENT_BANK_NAME`
- `PAYMENT_ACCOUNT_NAME`
- `PAYMENT_ACCOUNT_NUMBER`
- `PAYMENT_IFSC_CODE`
- `PAYMENT_BANK_BRANCH`
- `PAYMENT_CHECKOUT_URL`

Optional implemented values include `SUDO_USERS`, `START_IMG_URL`, `GO_ENGINE_PORT`, `GO_ENGINE_PUBLIC_URL`, `FFMPEG_PATH`, `API_HOST`, `API_PORT`, `CORS_ORIGINS`, `AI_PROVIDER`, `AI_API_KEY`, `VITE_API_BASE_URL`, and `VITE_API_KEY`. `POSTGRES_USER` and `POSTGRES_DB` are optional Compose values with defaults; `POSTGRES_PASSWORD` is required by Compose.

## Credentials Kahan Se Milenge

| Credential | Source |
| --- | --- |
| Telegram bot token | Telegram `@BotFather` |
| Telegram API ID/hash | `my.telegram.org` |
| Assistant session | Generate locally with a Pyrogram session tool using your own account |
| PostgreSQL URL | Database administrator or managed PostgreSQL provider |
| Redis URL | Redis administrator or managed Redis provider |
| AI provider key | Only the selected provider's official dashboard; current external calls are not implemented |
| Payment identity and bank details | Your registered merchant account and bank |
| Razorpay/Stripe/PayU credentials | Provider dashboard; currently planned only |
| Sentry DSN | Sentry project; currently planned only |

Never commit `.env`, session strings, API keys, payment credentials, or database passwords.

## Feature Audit

| Feature | Current environment state |
| --- | --- |
| Telegram, Pyrogram, assistant, PyTgCalls | Implemented through Telegram variables above; no separate PyTgCalls credential exists |
| Music and multi-group playback | Code exists; queue, worker, recovery and group limits are not env-configurable |
| Go engine | Port, public URL and shared bearer token are implemented |
| FFmpeg | Go executes `FFMPEG_PATH` with `exec.CommandContext`; Docker installs `ffmpeg` and Go startup checks accessibility |
| YouTube/media sources | No source-backed API key, cookies or proxy configuration |
| PostgreSQL/Redis | URLs implemented; pool/cache tuning is hard-coded |
| FastAPI/CORS | Host, port and CORS origins implemented |
| Website/frontend | `ui/src/api.ts` reads Vite `VITE_API_BASE_URL` and `VITE_API_KEY`; values are public in the browser and must not contain `MASTER_API_KEY` |
| AI | Local heuristic engine; `AI_API_KEY` is **READ BUT UNUSED** for external inference |
| Education/UPSC/programming | Bundled content; no environment reads |
| JWT/API security | API keys and dedicated `MASTER_API_KEY` exist; `JWT_SECRET` is read but unused; JWT/OAuth/refresh tokens do not |
| Premium/subscriptions | Tier logic exists; prices and quotas are code-defined |
| Payments | `PAYMENT_*` values configure implemented manual UPI/NEFT/card invoices; external gateways and webhooks are planned |
| Moderation/welcome/groups | Modules exist; thresholds and group allowlists are not env-backed |
| Broadcast/rate limits | Modules exist; controls are code-defined |
| Logging/monitoring/errors | Modules exist; exporters, alerting and most tuning are not env-backed |
| Docker/VPS/EC2 | Docker/systemd files exist; cloud deployment integrations are not implemented |

The commented `MISSING` and `PLANNED` variables in `.env.example` are documentation only. Adding them does not enable those features.

## Source Evidence

- Python variable loading and startup validation: `core/config.py`
- Master API-key authentication: `api/auth.py`
- AI provider/key loading: `ai/engine.py` and `core/config.py`
- Manual payment settings: `payments/gateway.py`
- Go stream authentication/public URL: `golang/internal/server/routes.go`
- FFmpeg execution: `golang/internal/audio/streamer.go`
- FFmpeg installation: `deployment/Dockerfile`
- Go startup checks: `golang/cmd/engine/main.go`
- Container propagation and PostgreSQL health check: `deployment/docker-compose.yml`
- Frontend build-time configuration: `ui/src/api.ts` and `ui/src/vite-env.d.ts`
