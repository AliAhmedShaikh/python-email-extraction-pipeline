"""Persistence utilities for email attachments."""

from pathlib import Path
from typing import Dict, List


def save_attachments(
    email_data: Dict,
    output_dir: str = "data/attachments",
) -> List[Path]:
    """Save extracted attachments and return their paths."""
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)

    saved = []
    for attachment in email_data.get("attachments", []):
        filename = Path(str(attachment["filename"])).name
        target = root / filename
        target.write_bytes(attachment["payload"])
        saved.append(target)

    return saved
