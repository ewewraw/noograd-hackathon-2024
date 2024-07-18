import unittest
from src.utils.email_utils import extract_email_data, extract_multiple_emails_data
from src.models.models import Email

class TestExtractEmailData(unittest.TestCase):

    def setUp(self):
        self.raw_email_1 = {
            "id": "some-id-1",
            "threadId": "some-thread-id",
            "labelIds": ["UNREAD", "CATEGORY_FORUMS"],
            "snippet": "This is the first email content.",
            "payload": {
                "mimeType": "multipart/signed",
                "headers": [
                    {"name": "From", "value": "sender1@example.com"},
                    {"name": "To", "value": "recipient1@example.com"},
                    {"name": "Subject", "value": "Subject 1"}
                ]
            },
            "sizeEstimate": 26129,
            "historyId": "some-history-id",
            "internalDate": "1721212134000"
        }

        self.raw_email_2 = {
            "id": "some-id-2",
            "threadId": "some-thread-id",
            "labelIds": ["UNREAD", "CATEGORY_FORUMS"],
            "snippet": "This is the second email content.",
            "payload": {
                "mimeType": "multipart/signed",
                "headers": [
                    {"name": "From", "value": "sender2@example.com"},
                    {"name": "To", "value": "recipient2@example.com"},
                    {"name": "Subject", "value": "Subject 2"}
                ]
            },
            "sizeEstimate": 26129,
            "historyId": "some-history-id",
            "internalDate": "1721212134000"
        }

        self.raw_emails = [self.raw_email_1, self.raw_email_2]

    def test_extract_email_data(self):
        expected_email_1 = Email(
            email_id="some-id-1",
            sender="sender1@example.com",
            recipient="recipient1@example.com",
            subject="Subject 1",
            content="This is the first email content."
        )

        expected_email_2 = Email(
            email_id="some-id-2",
            sender="sender2@example.com",
            recipient="recipient2@example.com",
            subject="Subject 2",
            content="This is the second email content."
        )

        extracted_email_1 = extract_email_data(self.raw_email_1)
        extracted_email_2 = extract_email_data(self.raw_email_2)

        self.assertEqual(extracted_email_1, expected_email_1)
        self.assertEqual(extracted_email_2, expected_email_2)

    def test_extract_multiple_emails_data(self):
        expected_emails = [
            Email(
                email_id="some-id-1",
                sender="sender1@example.com",
                recipient="recipient1@example.com",
                subject="Subject 1",
                content="This is the first email content."
            ),
            Email(
                email_id="some-id-2",
                sender="sender2@example.com",
                recipient="recipient2@example.com",
                subject="Subject 2",
                content="This is the second email content."
            )
        ]

        extracted_emails = extract_multiple_emails_data(self.raw_emails)

        self.assertEqual(extracted_emails, expected_emails)

if __name__ == '__main__':
    unittest.main()
