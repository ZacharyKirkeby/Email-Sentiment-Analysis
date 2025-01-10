import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# This file handles email ingestion

# Load environment variables from .env file
load_dotenv()

def fetch_emails():
    # Get credentials from environment variables - #security
        # TODO - redo off of IMAP, IMAP is deprecated
    #  
    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")
    imap_server = os.getenv("IMAP_SERVER", "imap.gmail.com")  # Default to Gmail IMAP

    if not email_address or not email_password:
        raise ValueError("Email credentials are not set. Please check your .env file.")
    try:
        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login(email_address, email_password)
        imap.select("inbox")
        _, messages = imap.search(None, "ALL")
        emails = {}
        for num in messages[0].split():
            _, msg = imap.fetch(num, "(RFC822)")
            for response_part in msg:
                if isinstance(response_part, tuple):
                    # Parse email
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_header(msg["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()
                    emails[num.decode()] = {"subject": subject, "body": body}
        imap.logout()
        return emails

    except imaplib.IMAP4.error as e:
        raise RuntimeError(f"Failed to fetch emails: {e}")