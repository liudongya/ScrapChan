#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════╗
║              S C R A P C H A N           ║
║     Telegram API Credential Fetcher      ║
║                                          ║
║  Author  : yuchann                       ║
║  GitHub  : github.com/samsouta/ScrapChan ║
║  Version : 2.0.0                         ║
╚═══════════════════════════════════════════╝
"""

from dotenv import load_dotenv
load_dotenv()

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

from core.auth import request_otp, verify_otp
from core.scraper import fetch_app_credentials, create_app_if_missing
from utils.parser import format_credentials, extract_phone, extract_otp_code
from utils.logger import get_logger
from config import Development as Config

# ──────────────────────────────────────────────
#  Logger
# ──────────────────────────────────────────────
log = get_logger(__name__)

# ──────────────────────────────────────────────
#  Conversation States
# ──────────────────────────────────────────────
AWAIT_PHONE, AWAIT_OTP = range(2)

# ──────────────────────────────────────────────
#  In-memory session store  { user_id: {...} }
# ──────────────────────────────────────────────
SESSION_STORE: dict = {}


# ╔══════════════════════════════════════════╗
#  Handler: /start
# ╚══════════════════════════════════════════╝
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry point — greet the user and ask for phone number."""
    await update.message.reply_text(
        Config.START_TEXT,
        parse_mode=ParseMode.HTML,
    )
    return AWAIT_PHONE


# ╔══════════════════════════════════════════╗
#  Handler: Receive Phone Number
# ╚══════════════════════════════════════════╝
async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Validate phone number and request OTP from Telegram."""
    user = update.message.from_user
    phone = extract_phone(update.message)

    if not phone:
        await update.message.reply_text(
            Config.INVALID_PHONE_MSG,
            parse_mode=ParseMode.HTML,
        )
        return AWAIT_PHONE

    log.info("[%s] Phone received: %s", user.id, phone)

    try:
        otp_hash = request_otp(phone)
    except Exception as e:
        log.error("OTP request failed: %s", e)
        await update.message.reply_text(
            "❌ <b>Failed to send OTP.</b> Check your phone number and try again.",
            parse_mode=ParseMode.HTML,
        )
        return AWAIT_PHONE

    SESSION_STORE[user.id] = {
        "phone": phone,
        "otp_hash": otp_hash,
    }

    await update.message.reply_text(
        Config.OTP_PROMPT_MSG,
        parse_mode=ParseMode.HTML,
    )
    return AWAIT_OTP


# ╔══════════════════════════════════════════╗
#  Handler: Receive OTP Code
# ╚══════════════════════════════════════════╝
async def handle_otp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Verify OTP, scrape credentials, and return to user."""
    user = update.message.from_user
    session = SESSION_STORE.pop(user.id, None)

    if not session:
        await update.message.reply_text(
            "⚠️ Session expired. Please /start again.",
            parse_mode=ParseMode.HTML,
        )
        return ConversationHandler.END

    # Show a "processing" message we'll edit later
    status_msg = await update.message.reply_text(
        Config.PROCESSING_MSG,
        parse_mode=ParseMode.HTML,
    )

    otp_code = extract_otp_code(update.message)
    if not otp_code:
        await status_msg.edit_text(
            Config.INVALID_OTP_MSG,
            parse_mode=ParseMode.HTML,
        )
        return AWAIT_PHONE

    # Step 1 — Login and get session cookie
    ok, cookie = verify_otp(
        session["phone"],
        session["otp_hash"],
        otp_code,
    )

    if not ok:
        await status_msg.edit_text(
            f"❌ <b>Login failed:</b> <code>{cookie}</code>",
            parse_mode=ParseMode.HTML,
        )
        return ConversationHandler.END

    # Step 2 — Ensure an app exists, create one if not
    try:
        has_app, meta = fetch_app_credentials(cookie)
        if not has_app:
            create_app_if_missing(
                cookie,
                meta.get("tg_app_hash"),
                Config.APP_TITLE,
                Config.APP_SHORT_NAME,
                Config.APP_URL,
                Config.APP_PLATFORM,
                Config.APP_DESCRIPTION,
            )

        # Step 3 — Fetch final credentials
        ok, creds = fetch_app_credentials(cookie)
        if ok:
            reply = format_credentials(session["phone"], creds)
            reply += f"\n\n{Config.FOOTER_TEXT}"
            await status_msg.edit_text(reply, parse_mode=ParseMode.HTML)
        else:
            log.warning("[%s] Failed to fetch credentials: %s", user.id, creds)
            await status_msg.edit_text(Config.ERROR_MSG, parse_mode=ParseMode.HTML)

    except Exception as e:
        log.error("Scraping error for user %s: %s", user.id, e)
        await status_msg.edit_text(Config.ERROR_MSG, parse_mode=ParseMode.HTML)

    return ConversationHandler.END


# ╔══════════════════════════════════════════╗
#  Handler: /cancel
# ╚══════════════════════════════════════════╝
async def cmd_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Allow user to abort the current flow."""
    uid = update.message.from_user.id
    SESSION_STORE.pop(uid, None)
    await update.message.reply_text(
        Config.CANCEL_MSG,
        parse_mode=ParseMode.HTML,
    )
    return ConversationHandler.END


# ╔══════════════════════════════════════════╗
#  Handler: /help
# ╚══════════════════════════════════════════╝
async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help information."""
    await update.message.reply_text(
        Config.HELP_TEXT,
        parse_mode=ParseMode.HTML,
    )


# ╔══════════════════════════════════════════╗
#  Error Handler
# ╚══════════════════════════════════════════╝
async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log all errors caused by updates."""
    log.error("Update [%s] caused error: %s", update, context.error)


# ╔══════════════════════════════════════════╗
#  Bootstrap
# ╚══════════════════════════════════════════╝
def main():
    token = Config.TG_BOT_TOKEN
    if not token:
        raise RuntimeError("❌ TG_BOT_TOKEN is not set! Add it to your .env file.")

    log.info("LazyYu bot is starting up...")

    app = ApplicationBuilder().token(token).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", cmd_start)],
        states={
            AWAIT_PHONE: [
                MessageHandler(filters.TEXT | filters.CONTACT, handle_phone)
            ],
            AWAIT_OTP: [
                MessageHandler(filters.TEXT, handle_otp)
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cmd_cancel),
            CommandHandler("start", cmd_start),
        ],
    )

    app.add_handler(conv)
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_error_handler(handle_error)

    log.info("Running in POLLING mode ✅")
    app.run_polling()


if __name__ == "__main__":
    main()