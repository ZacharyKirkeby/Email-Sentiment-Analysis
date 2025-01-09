import imaplib
import email
from email.header import decode_header

# This file handles email ingestion - uses imap to import things

def fetch_emails():
    
    # Connect to email server
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login("your_email@example.com", "your_password")

    # Select inbox
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

    # Close connection
    imap.logout()
    return emails
