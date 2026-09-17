import unittest
from email.message import EmailMessage

from src.email_parser import extract_email, parse_email


class TestEmailParser(unittest.TestCase):

    def test_extracts_metadata_and_text(self):
        msg = EmailMessage()
        msg["Subject"] = "Portfolio Test"
        msg["From"] = "sender@example.com"
        msg["To"] = "receiver@example.com"
        msg.set_content("Hello from the test email.")

        result = extract_email(parse_email(msg.as_bytes()))

        self.assertEqual(result["subject"], "Portfolio Test")
        self.assertEqual(result["from"], "sender@example.com")
        self.assertIn("Hello from the test email.", result["text_body"])
        self.assertEqual(result["attachments"], [])

    def test_extracts_attachment(self):
        msg = EmailMessage()
        msg["Subject"] = "Attachment Test"
        msg["From"] = "sender@example.com"
        msg.set_content("See attachment.")
        msg.add_attachment(
            b"sample data",
            maintype="text",
            subtype="plain",
            filename="sample.txt",
        )

        result = extract_email(parse_email(msg.as_bytes()))

        self.assertEqual(len(result["attachments"]), 1)
        self.assertEqual(result["attachments"][0]["filename"], "sample.txt")
        self.assertEqual(result["attachments"][0]["size_bytes"], 11)


if __name__ == "__main__":
    unittest.main()
