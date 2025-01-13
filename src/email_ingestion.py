from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
import base64
import json
import re
from html import unescape
from email.header import decode_header

load_dotenv()

# This file utilizes OAuth2 and the gmail API in order to access and process email data. 
# This is for email ingestion to the broader pipeline.

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Authenticate and get Gmail service."""
    with open('credentials.json', 'r') as credentials_file:
        client_config = json.load(credentials_file)
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=creds)
    return service

def decode_email_body(encoded_body):
    try:
        return base64.urlsafe_b64decode(encoded_body).decode('utf-8')
    except Exception as e:
        return f"Failed to decode body: {e}"

def clean_text(text):
    text = unescape(text)  # Unescape HTML entities
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
    text = text.replace('\r', '').replace('\n', ' ').strip()  # Remove newlines and extra spaces
    return text

def fetch_emails(numFetch):
    try:
        service = authenticate_gmail()  # Authenticate and get Gmail API service
        # i hate google cloud i hate google cloud

        results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=numFetch).execute()
        messages = results.get('messages', [])
        
        if not messages:
            print("No messages found.")
            return {}

        emails = {}
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()

            subject = ""
            body = ""
            html_body = "" #mayhaps this will fix the prolog issue

            for header in msg['payload']['headers']:
                if header['name'] == 'Subject':
                    subject, encoding = decode_header(header['value'])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or 'utf-8')
                    break

            # Extract the email body
            if 'parts' in msg['payload']:
                for part in msg['payload']['parts']:
                    mime_type = part.get('mimeType', '')
                    data = part.get('body', {}).get('data', '')

                    if mime_type == 'text/plain' and data:
                        body = decode_email_body(data)
                    elif mime_type == 'text/html' and data and not body:
                        html_body = decode_email_body(data)
            else:
                # For non-multipart messages
                body = decode_email_body(msg['payload']['body'].get('data', ''))

            # Use plain text if available, otherwise fallback to HTML
            final_body = body if body else html_body

            emails[message['id']] = {"subject": subject, "body": final_body}

        return emails

    except Exception as e:
        raise RuntimeError(f"Failed to fetch emails: {e}")