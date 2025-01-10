import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
import email
from email.header import decode_header

load_dotenv()

# This file utilizes OAuth2 and the gmail API in order to access and process email data. 
# This is for email ingestion to the broader pipeline.

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=creds)
    return service

def fetch_emails(numFetch):
    # fetch emails
    try:
        service = authenticate_gmail()  # Authenticate and get Gmail API service
        results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
        messages = results.get('messages', [])
        
        if not messages:
            print("No messages found.")
            return {}
        
        emails = {}
        for message in messages[:numFetch]:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            
            subject = ""
            body = ""
            # Get email subject
            for header in msg['payload']['headers']:
                if header['name'] == 'Subject':
                    subject = header['value']
                    break
            
            # Get email body (assuming text/plain is in the first part)
            if 'parts' in msg['payload']:
                for part in msg['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        body = part['body']['data']
                        body = base64.urlsafe_b64decode(body).decode('utf-8')
                        break
            else:
                # For non-multipart messages
                body = msg['payload']['body']['data']
                body = base64.urlsafe_b64decode(body).decode('utf-8')
            
            emails[message['id']] = {"subject": subject, "body": body}
        
        return emails
        
    except Exception as e:
        raise RuntimeError(f"Failed to fetch emails: {e}")
    
    