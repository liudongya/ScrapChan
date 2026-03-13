#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ScrapChan — utils/parser.py
Input extraction and output formatting utilities.
"""

from utils.logger import get_logger

log = get_logger(__name__)


def extract_phone(ptb_message) -> str | None:
    """
    Extract phone number from a PTB Message object.
    Supports plain text, phone_number entity, and contact share.

    Returns:
        Phone string or None if invalid.
    """
    # Contact share (user tapped "Share Contact")
    if ptb_message.contact and ptb_message.contact.phone_number:
        return ptb_message.contact.phone_number

    if ptb_message.text:
        # Entity-tagged phone number
        for entity in ptb_message.entities:
            if entity.type == "phone_number":
                return ptb_message.text[entity.offset: entity.offset + entity.length]
        # Plain text fallback
        return ptb_message.text.strip()

    return None


def extract_otp_code(ptb_message) -> str | None:
    """
    Extract the OTP / web login code from a PTB Message object.

    Telegram sometimes forwards the OTP inside a multi-line message
    formatted as:
        Web login code: XXXXX
        <code>

    Returns:
        OTP string or None if extraction fails.
    """
    if not ptb_message.text:
        return None

    text = ptb_message.text
    lower = text.lower()

    # Forwarded Telegram security message format
    if "web login code" in lower:
        lines = text.split("\n")
        if len(lines) >= 2:
            return lines[1].strip()

    # Plain single-line OTP
    if "\n" not in text:
        return text.strip()

    log.warning("Could not extract OTP from message: %s", text)
    return None


def format_credentials(phone: str, data: dict) -> str:
    """
    Convert the credential dictionary into a clean Telegram HTML message.

    Args:
        phone: The user's phone number.
        data:  Dictionary returned by fetch_app_credentials().

    Returns:
        Formatted HTML string ready to send via Telegram.
    """
    app_cfg = data.get("App Configuration", {})
    mtproto = data.get("MTProto Servers", {})
    production = mtproto.get("production", {})
    test = mtproto.get("test", {})
    disclaimer = data.get("disclaimer", "")

    lines = [
        "╔══════════════════════════╗",
        "        🔑  <b>ScrapChan Results</b>       ",
        "╚══════════════════════════╝",
        "",
        f"📱 <b>Phone</b>: <code>{phone}</code>",
        "",
        "━━━━  <b>App Configuration</b>  ━━━━",
        f"🆔 <b>APP ID</b>:   <code>{app_cfg.get('app_id', 'N/A')}</code>",
        f"🔐 <b>API HASH</b>: <code>{app_cfg.get('api_hash', 'N/A')}</code>",
        "",
        "━━━━  <b>MTProto Servers</b>  ━━━━",
        f"🟢 <b>Production</b>: <code>{production.get('ip', 'N/A')}</code>  <i>{production.get('dc', '')}</i>",
        f"🧪 <b>Test</b>:       <code>{test.get('ip', 'N/A')}</code>  <i>{test.get('dc', '')}</i>",
        "",
        f"⚠️ <i>{disclaimer}</i>",
    ]
    return "\n".join(lines)