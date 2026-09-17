# Email Extraction & Attachment Processing Pipeline

A Python-based email ingestion pipeline that connects to an IMAP mailbox, retrieves recent emails, parses semi-structured MIME messages, extracts metadata and message content, and saves attachments for downstream processing.

## Portfolio Project

This project demonstrates how an email inbox can be treated as a data source in an ETL/ELT workflow.

**Pipeline:**

```text
IMAP Mailbox
     |
     v
Secure Connection
     |
     v
Fetch Recent Emails
     |
     v
MIME / Email Parser
   /      |       \
  v       v        v
Metadata Text     HTML
          |
          v
      Attachments
          |
          v
   Local Data Store
```

## Features

- Secure IMAP over SSL
- Environment-based credential management
- Configurable mailbox and message limit
- RFC822 email retrieval
- MIME/multipart email parsing
- MIME header decoding
- Plain-text and HTML body extraction
- Attachment detection and persistence
- Modular project structure
- Unit tests using Python's standard library

## Project Structure

```text
python-email-extraction-pipeline/
├── src/
│   ├── config.py
│   ├── email_client.py
│   ├── email_parser.py
│   ├── attachment_handler.py
│   └── main.py
├── tests/
│   └── test_email_parser.py
├── data/
│   └── attachments/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.9+
- An IMAP-enabled email account
- For Gmail, an App Password is recommended when two-step verification is enabled.

No external Python dependencies are required.

## Setup

Clone the repository and enter the project directory:

```bash
git clone https://github.com/YOUR_USERNAME/python-email-extraction-pipeline.git
cd python-email-extraction-pipeline
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Copy `.env.example` to `.env` and configure your mailbox credentials.

**Never commit `.env` to GitHub.**

## Running the Pipeline

Because the project uses environment variables, export them in your shell or load them using your preferred environment-variable workflow.

Example on Windows PowerShell:

```powershell
$env:EMAIL_ADDRESS="your-email@example.com"
$env:EMAIL_PASSWORD="your-app-password"
python -m src.main --limit 10
```

Example on macOS/Linux:

```bash
export EMAIL_ADDRESS="your-email@example.com"
export EMAIL_PASSWORD="your-app-password"
python -m src.main --limit 10
```

Specify another output directory:

```bash
python -m src.main --limit 5 --output-dir data/attachments
```

## Testing

Run:

```bash
python -m unittest discover -s tests -v
```

The tests validate email metadata extraction, plain-text body extraction, and attachment parsing without requiring a real mailbox.

## Security

The original prototype used credentials directly in Python source code. The portfolio version intentionally removes that pattern and reads credentials from environment variables.

Never publish:

- Email passwords
- App passwords
- API keys
- OAuth secrets
- Private email contents
- Real customer attachments

If credentials have ever been committed to a public repository, rotate/revoke them immediately.

## Engineering Improvements Over the Prototype

The original scripts were consolidated into reusable modules:

1. **Configuration** — centralizes connection settings.
2. **Email client** — isolates IMAP connection and retrieval.
3. **Email parser** — handles MIME parsing, metadata, text, HTML and attachments.
4. **Attachment handler** — handles persistence separately from parsing.
5. **CLI entry point** — makes the pipeline configurable from the command line.
6. **Tests** — validates core parsing logic without connecting to an external mailbox.

## Potential Extensions

For a more production-oriented version, this project could be extended with:

- PostgreSQL or BigQuery storage for email metadata
- Airflow scheduling
- Incremental ingestion using message IDs / UIDs
- Duplicate detection
- Structured JSON output
- Data-quality validation
- Object storage such as Azure Blob Storage or GCS
- Docker deployment
- Logging and monitoring
- OCR for document attachments
- NLP classification of incoming emails
- A dashboard showing email volume, senders and attachment statistics

## Skills Demonstrated

**Python · Data Engineering · ETL · IMAP · Email/MIME Parsing · Data Ingestion · File Processing · API/Protocol Integration · Secure Configuration · Testing · Modular Software Design**

## Original Concept

The project evolved from Python scripts that connected to Gmail through IMAP, retrieved email messages using RFC822, extracted subjects and senders, processed multipart messages, and downloaded attachments. The portfolio version reorganizes those ideas into a maintainable project structure.

## License

MIT License
