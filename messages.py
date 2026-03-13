#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ScrapChan — messages.py
All user-facing message strings. Edit here to customise bot text.
"""


class Messages:

    START_TEXT = """
╔══════════════════════════════╗
      👾  <b>ScrapChan Bot</b>
╚══════════════════════════════╝

Hey! 👋 I'll fetch your Telegram <b>APP ID</b> and <b>API HASH</b> for you — no browser needed.

<b>How it works:</b>
1️⃣ Send me your phone number <i>(with country code)</i>
2️⃣ Enter the OTP Telegram sends you
3️⃣ Done — I'll reply with your credentials ✅

━━━━━━━━━━━━━━━━━━━━━━━
📲 <b>Please send your phone number now.</b>
<i>Example: +601xxxxxxxx</i>

🔒 <i>Your credentials are never stored.</i>
"""

    OTP_PROMPT_MSG = """
✅ <b>Phone number received!</b>

Telegram has sent you a <b>Login Code</b>.
Please send it here now.

<i>Tip: You can forward the Telegram notification message directly — I'll extract the code automatically.</i>
"""

    PROCESSING_MSG = "<code>⏳ Received. Logging in and fetching credentials...</code>"

    HELP_TEXT = """
<b>ScrapChan — Help</b>

I fetch your Telegram APP ID &amp; API HASH without you needing to visit <code>my.telegram.org</code>.

<b>Commands:</b>
/start  — Begin the credential fetch flow
/cancel — Abort the current session
/help   — Show this message

<b>Need support?</b>
Contact: <a href="https://t.me/samsouta">@samsouta</a>
"""

    CANCEL_MSG = "👋 <b>Session cancelled.</b> Send /start whenever you're ready."

    INVALID_PHONE_MSG = """
❌ <b>Invalid phone number.</b>

Please include your country code.
<i>Example: +601xxxxxxxx</i>
"""

    INVALID_OTP_MSG = "❌ <b>Could not read the OTP code.</b> Please send only the code, e.g. <code>12345</code>."

    ERROR_MSG = """
⚠️ <b>Something went wrong.</b>

Please try again with /start.
If the issue persists, fetch manually at <a href="https://my.telegram.org/apps">my.telegram.org/apps</a>.
"""