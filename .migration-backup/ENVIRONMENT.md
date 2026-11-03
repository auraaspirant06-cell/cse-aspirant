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
   - `TELEGRAM_API_ID` aur `TELEGRAM_API_HASH`: `my.telegram.org` ke API development tools se.
   - `TELEGRAM_SESSION_STRING`: apne assistant user account ka Pyrogram session string. Isse kisi ke saath share na karein.
   - `OWNER_ID`: apna numeric Telegram user ID.
