#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ScrapChan — utils/logger.py
Centralized logging configuration.
"""

import logging

_configured = False


def _setup():
    global _configured
    if not _configured:
        logging.basicConfig(
            format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.INFO,
        )
        _configured = True


def get_logger(name: str) -> logging.Logger:
    """Return a named logger, ensuring global config is applied once."""
    _setup()
    return logging.getLogger(name)