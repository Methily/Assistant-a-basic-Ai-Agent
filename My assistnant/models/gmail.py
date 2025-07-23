from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import base64
import email
from email.mime.text import MIMEText
import config

class GmailClient:
    def __init__(self):
        """Initialize Gmail client."""
        self.creds = None
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Handle OAuth2 authentication for Gmail."""
        if os.path.exists(config.GOOGLE_TOKEN_PATH):
            self.creds = Credentials.from_authorized_user_file(
                config.GOOGLE_TOKEN_PATH, config.GOOGLE_SCOPES
            )

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    config.get_google_credentials(), config.GOOGLE_SCOPES
                )
                self.creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            os.makedirs(os.path.dirname(config.GOOGLE_TOKEN_PATH), exist_ok=True)
            with open(config.GOOGLE_TOKEN_PATH, 'w') as token:
                token.write(self.creds.to_json())

        self.service = build('gmail', 'v1', credentials=self.creds)

    def get_unread_emails(self, max_results=5):
        """
        Get unread emails from Gmail.
        
        Args:
            max_results (int): Maximum number of emails to return
        """
        try:
            results = self.service.users().messages().list(
                userId='me',
                labelIds=['UNREAD'],
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])
            if not messages:
                return "No unread emails found."

            email_list = []
            for message in messages:
                msg = self.service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='full'
                ).execute()

                headers = msg['payload']['headers']
                subject = next(h['value'] for h in headers if h['name'] == 'Subject')
                sender = next(h['value'] for h in headers if h['name'] == 'From')
                
                # Get email body
                if 'parts' in msg['payload']:
                    parts = msg['payload']['parts']
                    body = ''
                    for part in parts:
                        if part['mimeType'] == 'text/plain':
                            body = base64.urlsafe_b64decode(
                                part['body']['data']
                            ).decode('utf-8')
                            break
                else:
                    body = base64.urlsafe_b64decode(
                        msg['payload']['body']['data']
                    ).decode('utf-8')

                email_list.append(f"From: {sender}\nSubject: {subject}\n\n{body[:200]}...")

            return "\n\n".join(email_list)
        except Exception as e:
            return f"Error fetching emails: {str(e)}"

    def send_email(self, to, subject, body):
        """
        Send an email using Gmail.
        
        Args:
            to (str): Recipient email address
            subject (str): Email subject
            body (str): Email body
        """
        try:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject

            raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            self.service.users().messages().send(
                userId='me',
                body={'raw': raw}
            ).execute()
            return f"Email sent successfully to {to}"
        except Exception as e:
            return f"Error sending email: {str(e)}"

    def mark_as_read(self, message_id):
        """
        Mark an email as read.
        
        Args:
            message_id (str): ID of the email to mark as read
        """
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            return "Email marked as read"
        except Exception as e:
            return f"Error marking email as read: {str(e)}"

if __name__ == "__main__":
    # Test Gmail integration
    gmail = GmailClient()
    
    # Test getting unread emails
    emails = gmail.get_unread_emails()
    print("Unread emails:")
    print(emails)
    
    # Test sending an email
    result = gmail.send_email(
        "test@example.com",
        "Test Email",
        "This is a test email from Nova assistant."
    )
    print("\nSend email result:")
    print(result) 