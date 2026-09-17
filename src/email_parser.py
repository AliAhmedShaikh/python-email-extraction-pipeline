"""Utilities for parsing MIME email messages."""

from email import policy
from email.header import decode_header
from email.parser import BytesParser
from email.message import Message
from typing import Dict, List, Optional


def decode_mime_header(value: Optional[str]) -> str:
    """Decode an RFC/MIME header into readable text."""
    if not value:
        return ""

    parts = []
    for fragment, encoding in decode_header(value):
        if isinstance(fragment, bytes):
            parts.append(fragment.decode(encoding or "utf-8", errors="replace"))
        else:
            parts.append(fragment)
    return "".join(parts)


def parse_email(raw_message: bytes) -> Message:
    """Convert raw RFC822 bytes into an email Message object."""
    return BytesParser(policy=policy.default).parsebytes(raw_message)


def extract_email(message: Message) -> Dict:
    """Extract metadata, plain text, HTML and attachment information."""
    attachments: List[Dict[str, object]] = []
    text_parts: List[str] = []
    html_parts: List[str] = []

    for part in message.walk():
        if part.is_multipart():
            continue

        filename = part.get_filename()
        content_type = part.get_content_type()
        payload = part.get_payload(decode=True)

        if filename:
            attachments.append(
                {
                    "filename": decode_mime_header(filename),
                    "content_type": content_type,
                    "size_bytes": len(payload or b""),
                    "payload": payload or b"",
                }
            )
            continue

        if content_type == "text/plain" and payload:
            text_parts.append(payload.decode(
                part.get_content_charset() or "utf-8", errors="replace"
            ))
        elif content_type == "text/html" and payload:
            html_parts.append(payload.decode(
                part.get_content_charset() or "utf-8", errors="replace"
            ))

    return {
        "subject": decode_mime_header(message.get("Subject")),
        "from": decode_mime_header(message.get("From")),
        "to": decode_mime_header(message.get("To")),
        "date": message.get("Date", ""),
        "message_id": message.get("Message-ID", ""),
        "text_body": "\n".join(text_parts).strip(),
        "html_body": "\n".join(html_parts).strip(),
        "attachments": attachments,
    }
