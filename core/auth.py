#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ScrapChan — core/auth.py
Handles OTP request and login verification against my.telegram.org
"""

import requests
from utils.logger import get_logger

log = get_logger(__name__)

_BASE_URL = "https://my.telegram.org/auth"


def request_otp(phone: str) -> str:
    """
    Send OTP request to my.telegram.org.

    Args:
        phone: Phone number in international format (e.g. +601xxxxxxxx)

    Returns:
        random_hash string required for the login step.
    """
    url = f"{_BASE_URL}/send_password"
    log.info("Requesting OTP for phone: %s", phone)
    resp = requests.post(url, data={"phone": phone}, timeout=15)
    resp.raise_for_status()
    return resp.json()["random_hash"]


def verify_otp(phone: str, random_hash: str, otp_code: str):
    """
    Submit OTP code to my.telegram.org and retrieve session cookie.

    Args:
        phone:       Phone number in international format.
        random_hash: Hash returned by request_otp().
        otp_code:    OTP code the user received on Telegram.

    Returns:
        Tuple (success: bool, value: str)
        - On success : (True,  stel_token cookie string)
        - On failure : (False, error message string)
    """
    url = f"{_BASE_URL}/login"
    payload = {
        "phone": phone,
        "random_hash": random_hash,
        "password": otp_code,
    }
    log.info("Verifying OTP for phone: %s", phone)
    resp = requests.post(url, data=payload, timeout=15)

    if resp.text.strip() == "true":
        cookie = resp.headers.get("Set-Cookie", "")
        log.info("Login successful for phone: %s", phone)
        return True, cookie

    log.warning("Login failed for phone %s — response: %s", phone, resp.text)
    return False, resp.text