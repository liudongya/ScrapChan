# 👾 ScrapChan

> **Get your Telegram APP ID & API HASH — without ever opening a browser.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Author](https://img.shields.io/badge/Author-yuchann-orange?style=flat-square)](https://github.com/samsouta)

---

## ✨ What is ScrapChan?

**ScrapChan** is a Telegram bot that automates the login flow on `my.telegram.org` — so you can grab your `APP ID` and `API HASH` directly inside Telegram, in seconds.

No browser. No manual copy-paste. Just your phone number and an OTP.

---

## 🚀 How It Works

```
/start  →  Send phone number  →  Enter OTP  →  Get credentials ✅
```

1. Start the bot with `/start`
2. Send your phone number (e.g. `+601xxxxxxxx`)
3. Enter the OTP Telegram sends you
4. The bot replies with your **APP ID** and **API HASH**

---

## ⚠️ Security Notice

> **Your credentials are never stored.**
> This bot processes everything in memory and discards session data immediately after use.

- **Run your own private instance** — never send credentials to a bot you don't control.
- Telegram explicitly states: *"It is forbidden to pass this value to third parties."*
- ScrapChan is for **personal, educational use only**.

---

## 📁 Project Structure

```
ScrapChan/
├── main.py              # Bot entry point
├── config.py            # Configuration (env vars + defaults)
├── messages.py          # All user-facing message strings
├── requirements.txt     # Python dependencies
├── Procfile             # Heroku/Railway deployment
├── runtime.txt          # Python version pin
├── LICENSE              # MIT License
│
├── core/
│   ├── auth.py          # OTP request & login (my.telegram.org)
│   └── scraper.py       # App credential scraping & creation
│
└── utils/
    ├── parser.py        # Input extraction & output formatting
    └── logger.py        # Centralized logging
```

---

## 🛠️ Setup & Run

### 1. Clone the repo

```bash
git clone https://github.com/samsouta/ScrapChan.git
cd ScrapChan
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your config

```bash
cp config.py config_local.py   # optional for local overrides
```

Set your bot token as an environment variable:

```bash
export TG_BOT_TOKEN="your_bot_token_from_botfather"
```

### 4. Run the bot

```bash
python main.py
```

---

## ☁️ Deploy to Railway (Free)

1. Fork this repo
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Set the environment variable: `TG_BOT_TOKEN`
4. Done ✅

---

## 🔧 Environment Variables

| Variable          | Required | Default              | Description                        |
|-------------------|----------|----------------------|------------------------------------|
| `TG_BOT_TOKEN`    | ✅ Yes   | —                    | Bot token from @BotFather          |
| `WEBHOOK`         | No       | `False`              | Set to anything to enable webhook  |
| `URL`             | No       | —                    | Your app URL (webhook mode only)   |
| `PORT`            | No       | `5000`               | Port for webhook                   |
| `APP_TITLE`       | No       | `ScrapChan`             | Title for auto-created apps        |
| `APP_SHORT_NAME`  | No       | `ScrapChan`             | Short name for auto-created apps   |
| `FOOTER_TEXT`     | No       | ScrapChan credit line   | Footer appended to bot replies     |

---

## 📦 Dependencies

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [requests](https://github.com/psf/requests)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4)

---

## 📄 License

MIT © 2025 [yuchann](https://github.com/samsouta)

---

<p align="center">Made with ☕ by yuchann</p>