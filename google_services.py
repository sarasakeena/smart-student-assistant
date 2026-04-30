import os
import logging
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.cloud import storage

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Scopes for Google APIs
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/cloud-platform'
]

class GoogleServices:
    """Production-ready handler for Google Drive, Sheets, Gmail, and Cloud Storage."""

    def __init__(self, credentials_path='credentials.json', token_path='token.json'):
        self.creds = self._authenticate(credentials_path, token_path)
        self.drive_service = build('drive', 'v3', credentials=self.creds)
        self.sheets_service = build('sheets', 'v4', credentials=self.creds)
        self.gmail_service = build('gmail', 'v1', credentials=self.creds)
        # Cloud Storage typically requires a Service Account, but we'll try initializing it
        try:
            self.storage_client = storage.Client()
        except Exception as e:
            logger.warning(f"Cloud Storage client could not be initialized without service account: {e}")
            self.storage_client = None

    def _authenticate(self, credentials_path, token_path):
        """Handles OAuth2 authentication flow."""
        creds = None
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(credentials_path):
                    logger.error(f"{credentials_path} not found. Please provide it from Google Cloud Console.")
                    return None
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        return creds

    def upload_resume_to_drive(self, file_path, folder_id=None):
        """
        Uploads a resume file to a specific Google Drive folder.
        
        :param file_path: Path to the local file.
        :param folder_id: ID of the Drive folder.
        :return: ID of the uploaded file.
        """
        try:
            file_metadata = {'name': os.path.basename(file_path)}
            if folder_id:
                file_metadata['parents'] = [folder_id]
            
            media = MediaFileUpload(file_path, resumable=True)
            file = self.drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            logger.info(f"File uploaded successfully to Drive. File ID: {file.get('id')}")
            return file.get('id')
        except Exception as e:
            logger.error(f"Error uploading to Drive: {e}")
            return None

    def save_application_to_sheets(self, spreadsheet_id, job_data):
        """
        Appends a new job application row to a Google Sheet.
        
        :param spreadsheet_id: ID of the Google Sheet.
        :param job_data: List of values [Company, Role, Date, Status].
        """
        try:
            range_name = 'Sheet1!A:D'
            body = {'values': [job_data]}
            result = self.sheets_service.spreadsheets().values().append(
                spreadsheet_id=spreadsheet_id, range=range_name,
                valueInputOption='RAW', body=body).execute()
            logger.info(f"Appended row to Sheets. {result.get('updates').get('updatedCells')} cells updated.")
        except Exception as e:
            logger.error(f"Error saving to Sheets: {e}")

    def send_email_draft(self, recipient, subject, body):
        """
        Creates and sends an email draft via Gmail API.
        
        :param recipient: Email address of the recipient.
        :param subject: Email subject line.
        :param body: Email content.
        """
        try:
            message = MIMEText(body)
            message['to'] = recipient
            message['from'] = 'me'
            message['subject'] = subject
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            self.gmail_service.users().messages().send(userId='me', body={'raw': raw}).execute()
            logger.info(f"Email sent successfully to {recipient}")
        except Exception as e:
            logger.error(f"Error sending email: {e}")

    def list_uploaded_resumes(self, folder_id):
        """
        Lists all files in a specific Google Drive folder.
        
        :param folder_id: ID of the Drive folder.
        :return: List of file objects.
        """
        try:
            query = f"'{folder_id}' in parents"
            results = self.drive_service.files().list(q=query, fields="files(id, name)").execute()
            items = results.get('files', [])
            return items
        except Exception as e:
            logger.error(f"Error listing files from Drive: {e}")
            return []

if __name__ == "__main__":
    # Test block with mock behavior description
    logger.info("Initializing Google Services Test...")
    # To test for real, place a 'credentials.json' in this folder.
    # services = GoogleServices()
    # services.send_email_draft("test@example.com", "Test Subject", "Hello from Python!")
