"""Configuration for the email extraction pipeline."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""

    imap_server: str = os.getenv("IMAP_SERVER", "imap.gmail.com")
    imap_port: int = int(os.getenv("IMAP_PORT", "993"))
    email_address: str = os.getenv("EMAIL_ADDRESS", "")
    email_password: str = os.getenv("EMAIL_PASSWORD", "")
    mailbox: str = os.getenv("MAILBOX", "INBOX")
    output_dir: str = os.getenv("OUTPUT_DIR", "data/attachments")


def get_settings() -> Settings:
    """Return validated application settings."""
    settings = Settings()

    if not settings.email_address or not settings.email_password:
        raise ValueError(
            "EMAIL_ADDRESS and EMAIL_PASSWORD must be configured. "
            "See .env.example."
        )

    return settings
