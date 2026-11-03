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
4. Python bridge aur Go engine mein same `GO_ENGINE_TOKEN` rakhiye. `GO_ENGINE_URL` internal Go service URL aur `GO_ENGINE_PUBLIC_URL` users ke liye reachable URL hai.
5. `JWT_SECRET` naam current code mein master `X-API-Key` secret ke liye use hota hai. Isko locally generate karke replace karein:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(48))"
   ```
6. Current manual payment invoice ke liye registered merchant/bank details bhariye. Razorpay, Stripe, PayU ya webhook credentials tab tak na bharein jab tak integration code add na ho.
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
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `REDIS_URL`
- `GO_ENGINE_URL`
- `GO_ENGINE_TOKEN`
- `JWT_SECRET`
- `PAYMENT_UPI_ID`
- `PAYMENT_MERCHANT_NAME`
- `PAYMENT_BANK_NAME`
- `PAYMENT_ACCOUNT_NAME`
- `PAYMENT_ACCOUNT_NUMBER`
- `PAYMENT_IFSC_CODE`
- `PAYMENT_BANK_BRANCH`
- `PAYMENT_CHECKOUT_URL`

Optional implemented values include `SUDO_USERS`, `START_IMG_URL`, `API_HOST`, `API_PORT`, `GO_ENGINE_PORT`, `GO_ENGINE_PUBLIC_URL`, `CORS_ORIGINS`, `AI_PROVIDER`, and `AI_API_KEY`.

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
| FFmpeg | Installed by Docker; no runtime env read and no Go FFmpeg subprocess |
| YouTube/media sources | No source-backed API key, cookies or proxy configuration |
| PostgreSQL/Redis | URLs implemented; pool/cache tuning is hard-coded |
| FastAPI/CORS | Host, port and CORS origins implemented |
| Website/frontend | Static UI has no environment-variable reads; frontend API URL is planned |
| AI | Local heuristic engine; `AI_API_KEY` is read but unused for external inference |
| Education/UPSC/programming | Bundled content; no environment reads |
| JWT/API security | API keys and master key exist; JWT/OAuth/refresh tokens do not |
| Premium/subscriptions | Tier logic exists; prices and quotas are code-defined |
| Payments | Manual UPI/NEFT/card invoice flow; external gateways and webhooks are planned |
| Moderation/welcome/groups | Modules exist; thresholds and group allowlists are not env-backed |
| Broadcast/rate limits | Modules exist; controls are code-defined |
| Logging/monitoring/errors | Modules exist; exporters, alerting and most tuning are not env-backed |
| Docker/VPS/EC2 | Docker/systemd files exist; cloud deployment integrations are not implemented |

The commented `MISSING` and `PLANNED` variables in `.env.example` are documentation only. Adding them does not enable those features.
