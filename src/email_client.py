"""IMAP client used to connect to and retrieve email messages."""

import imaplib
from email.message import Message
from typing import List


class EmailClient:
    """Small wrapper around Python's IMAP4_SSL client."""

    def __init__(self, server: str, port: int, username: str, password: str):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.connection = None

    def connect(self) -> None:
        """Open an encrypted IMAP connection and authenticate."""
        self.connection = imaplib.IMAP4_SSL(self.server, self.port)
        self.connection.login(self.username, self.password)

    def select_mailbox(self, mailbox: str = "INBOX") -> int:
        """Select a mailbox and return the number of messages."""
        if self.connection is None:
            raise RuntimeError("Connect before selecting a mailbox.")

        status, data = self.connection.select(mailbox)
        if status != "OK":
            raise RuntimeError(f"Unable to select mailbox: {mailbox}")

        return int(data[0])

    def fetch_latest(self, count: int = 10) -> List[bytes]:
        """Fetch the latest `count` messages as RFC822 byte strings."""
        if self.connection is None:
            raise RuntimeError("Connect before fetching messages.")

        status, data = self.connection.search(None, "ALL")
        if status != "OK":
            raise RuntimeError("Unable to search mailbox.")

        message_ids = data[0].split()
        selected_ids = message_ids[-count:] if count > 0 else []

        messages = []
        for message_id in reversed(selected_ids):
            status, response = self.connection.fetch(message_id, "(RFC822)")
            if status != "OK":
                continue

            for item in response:
                if isinstance(item, tuple):
                    messages.append(item[1])

        return messages

    def close(self) -> None:
        """Close the mailbox and log out."""
        if self.connection is not None:
            try:
                self.connection.close()
            except imaplib.IMAP4.error:
                pass
            self.connection.logout()
            self.connection = None
