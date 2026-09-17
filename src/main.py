"""Command-line entry point for the email extraction pipeline."""

import argparse
import json

from .attachment_handler import save_attachments
from .config import get_settings
from .email_client import EmailClient
from .email_parser import extract_email, parse_email


def run(limit: int, output_dir: str) -> None:
    settings = get_settings()

    client = EmailClient(
        settings.imap_server,
        settings.imap_port,
        settings.email_address,
        settings.email_password,
    )

    try:
        client.connect()
        total = client.select_mailbox(settings.mailbox)
        print(f"Connected to {settings.mailbox}. Messages available: {total}")

        raw_messages = client.fetch_latest(limit)

        for index, raw_message in enumerate(raw_messages, start=1):
            email_data = extract_email(parse_email(raw_message))
            saved = save_attachments(email_data, output_dir)

            result = {
                "subject": email_data["subject"],
                "from": email_data["from"],
                "date": email_data["date"],
                "attachments_saved": [str(path) for path in saved],
            }

            print(f"\nEmail {index}")
            print(json.dumps(result, indent=2, ensure_ascii=False))

    finally:
        client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract recent emails and save their attachments."
    )
    parser.add_argument(
        "--limit", type=int, default=10,
        help="Number of latest emails to process (default: 10).",
    )
    parser.add_argument(
        "--output-dir", default=None,
        help="Attachment output directory.",
    )
    args = parser.parse_args()

    settings = get_settings()
    run(args.limit, args.output_dir or settings.output_dir)
