#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ScrapChan — config.py
Configuration for both production (Webhook) and development (Polling) modes.
"""

import os
from messages import Messages


class Config:
    # ── Required ────────────────────────────────────────────────
    TG_BOT_TOKEN: str = os.environ.get("TG_BOT_TOKEN", "")

    # ── Webhook (production) ─────────────────────────────────────
    URL: str = os.environ.get("URL", "https://example.com/")
    PORT: int = int(os.environ.get("PORT", 5000))

    # ── Telegram App defaults (used when creating a new app) ─────
    APP_TITLE: str       = os.environ.get("APP_TITLE",       "ScrapChan")
    APP_SHORT_NAME: str  = os.environ.get("APP_SHORT_NAME",  "ScrapChan")
    APP_URL: str         = os.environ.get("APP_URL",         "")
    APP_PLATFORM: list   = [
        "android", "ios", "wp", "bb",
        "desktop", "web", "ubp", "other",
    ]
    APP_DESCRIPTION: str = os.environ.get(
        "APP_DESCRIPTION",
        "Fetched via ScrapChan — github.com/samsouta/ScrapChan",
    )

    # ── Bot messages ─────────────────────────────────────────────
    START_TEXT: str      = os.environ.get("START_TEXT",      Messages.START_TEXT)
    OTP_PROMPT_MSG: str  = os.environ.get("OTP_PROMPT_MSG",  Messages.OTP_PROMPT_MSG)
    PROCESSING_MSG: str  = os.environ.get("PROCESSING_MSG",  Messages.PROCESSING_MSG)
    HELP_TEXT: str       = os.environ.get("HELP_TEXT",       Messages.HELP_TEXT)
    CANCEL_MSG: str      = os.environ.get("CANCEL_MSG",      Messages.CANCEL_MSG)
    INVALID_PHONE_MSG    = Messages.INVALID_PHONE_MSG
    INVALID_OTP_MSG      = Messages.INVALID_OTP_MSG
    ERROR_MSG            = Messages.ERROR_MSG

    # ── Footer appended to successful credential reply ───────────
    FOOTER_TEXT: str = os.environ.get(
        "FOOTER_TEXT",
        "🤖 <b>Powered by <a href='https://github.com/samsouta/ScrapChan'>ScrapChan</a></b> — by yuchann",
    )


class Development(Config):
    """Local development — override any values below as needed."""
    pass