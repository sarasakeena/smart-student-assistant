import unittest
from unittest.mock import patch, MagicMock
from google_services import GoogleServices

class TestGoogleServices(unittest.TestCase):
    @patch('google_services.build')
    @patch('google_services.GoogleServices._authenticate')
    def setUp(self, mock_auth, mock_build):
        # Mocking credentials and build services
        mock_auth.return_value = MagicMock()
        self.services = GoogleServices()
        
        self.mock_drive = mock_build.return_value
        self.mock_sheets = mock_build.return_value
        self.mock_gmail = mock_build.return_value

    @patch('google_services.MediaFileUpload')
    def test_upload_resume_to_drive(self, mock_media):
        # Setup mock for Drive files().create().execute()
        mock_execute = MagicMock(return_value={'id': 'fake_drive_id'})
        self.services.drive_service.files().create().execute = mock_execute
        
        result = self.services.upload_resume_to_drive("dummy.pdf", "folder_123")
        self.assertEqual(result, 'fake_drive_id')
        self.assertTrue(self.services.drive_service.files().create.called)

    def test_save_application_to_sheets(self):
        # Setup mock for Sheets spreadsheets().values().append().execute()
        mock_execute = MagicMock(return_value={'updates': {'updatedCells': 4}})
        self.services.sheets_service.spreadsheets().values().append().execute = mock_execute
        
        # This shouldn't raise any errors
        self.services.save_application_to_sheets("sheet_id", ["Google", "Engineer", "2024", "Applied"])
        self.assertTrue(self.services.sheets_service.spreadsheets().values().append.called)

    def test_send_email_draft_logic(self):
        # Setup mock for Gmail users().messages().send().execute()
        mock_execute = MagicMock(return_value={'id': 'msg_123'})
        self.services.gmail_service.users().messages().send().execute = mock_execute
        
        self.services.send_email_draft("test@test.com", "Sub", "Body")
        self.assertTrue(self.services.gmail_service.users().messages().send.called)

if __name__ == "__main__":
    unittest.main()
