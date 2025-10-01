from __future__ import annotations
from loguru import logger
import os
import sys
from typing import Any, Dict


REDACT_KEYS = {"authorization", "password", "token", "secret", "api_key", "openai_api_key"}


def setup_logging(level: str = "INFO") -> None:
    logger.remove()
    logger.add(sys.stdout, level=level, backtrace=False, diagnose=False)


def redact(data: Dict[str, Any]) -> Dict[str, Any]:
    redacted: Dict[str, Any] = {}
    for k, v in data.items():
        if k.lower() in REDACT_KEYS:
            redacted[k] = "[REDACTED]"
        else:
            redacted[k] = v
    return redacted


__all__ = ["logger", "setup_logging", "redact"]
