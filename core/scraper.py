#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ScrapChan — core/scraper.py
Scrapes my.telegram.org/apps and optionally creates a new app.
"""

import random
import requests
from bs4 import BeautifulSoup
from utils.logger import get_logger

log = get_logger(__name__)

_APPS_URL = "https://my.telegram.org/apps"
_CREATE_URL = "https://my.telegram.org/apps/create"


def fetch_app_credentials(stel_cookie: str):
    """
    Scrape the my.telegram.org/apps page for APP ID and API HASH.

    Args:
        stel_cookie: Session cookie returned after successful login.

    Returns:
        Tuple (has_app: bool, data: dict)
        - has_app=True  → data contains full credential dict
        - has_app=False → data contains {"tg_app_hash": "..."} for app creation
    """
    headers = {"Cookie": stel_cookie}
    resp = requests.get(_APPS_URL, headers=headers, timeout=15)
    soup = BeautifulSoup(resp.text, "html.parser")
    page_title = soup.title.string if soup.title else ""

    if "configuration" in page_title.lower():
        inputs = soup.find_all("span", {"class": "input-xlarge"})
        help_blocks = soup.find_all("p", {"class": "help-block"})

        credentials = {
            "App Configuration": {
                "app_id": inputs[0].string,
                "api_hash": inputs[1].string,
            },
            "MTProto Servers": {
                "test": {
                    "ip": inputs[4].string,
                    "dc": help_blocks[-2].text.strip(),
                },
                "production": {
                    "ip": inputs[5].string,
                    "dc": help_blocks[-1].text.strip(),
                },
            },
            "disclaimer": "It is forbidden to pass this value to third parties.",
        }
        log.info("Successfully scraped credentials.")
        return True, credentials

    # No app found — extract tg_app_hash for creation
    tg_app_hash = soup.find("input", {"name": "hash"})
    hash_value = tg_app_hash.get("value") if tg_app_hash else ""
    log.info("No existing app found. tg_app_hash extracted.")
    return False, {"tg_app_hash": hash_value}


def create_app_if_missing(
    stel_cookie: str,
    tg_app_hash: str,
    app_title: str,
    app_shortname: str,
    app_url: str,
    app_platforms: list,
    app_desc: str,
):
    """
    Create a new Telegram app on my.telegram.org/apps.

    Args:
        stel_cookie:   Session cookie.
        tg_app_hash:   Hash value from the create-app form.
        app_title:     Display title for the app.
        app_shortname: Short alphanumeric name (5–32 chars).
        app_url:       Optional URL for the app.
        app_platforms: List of valid platform strings to randomly pick from.
        app_desc:      Description of the app.
    """
    headers = {"Cookie": stel_cookie}
    payload = {
        "hash": tg_app_hash,
        "app_title": app_title,
        "app_shortname": app_shortname,
        "app_url": app_url,
        "app_platform": random.choice(app_platforms),
        "app_desc": app_desc,
    }
    log.info("Creating new Telegram app: %s", app_title)
    resp = requests.post(_CREATE_URL, data=payload, headers=headers, timeout=15)
    log.info("App creation response status: %s", resp.status_code)
    return resp