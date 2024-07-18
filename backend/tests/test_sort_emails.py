import unittest
import os
from src.llm_processing.llm_processing import sort_emails
from src.models.models import Email, EmailIds

class TestSortEmailsIntegration(unittest.TestCase):

    def test_sort_emails(self):
        # Ensure the API key is set
        self.assertIsNotNone(os.getenv('GEMINI_API_KEY'), "GEMINI_API_KEY environment variable not set")

        # Sample email data
        emails = [
            {
                "email_id": "1",
                "sender": "sender1@example.com",
                "recipient": "recipient1@example.com",
                "subject": "This email is VERY Important 1",
                "content": "Content of email 1"
            },
            {
                "email_id": "2",
                "sender": "sender2@example.com",
                "recipient": "recipient2@example.com",
                "subject": "This email is mildly important 2",
                "content": "Content of email 2"
            },
            {
                "email_id": "3",
                "sender": "sender3@example.com",
                "recipient": "recipient3@example.com",
                "subject": "Subject 3",
                "content": "Content of email 3"
            }
        ]

        # Call the function
        result = sort_emails(emails)
        

        # Print the result for manual verification
        print("Sorted Email IDs:", result)

        # Assert that result is a list
        self.assertIsInstance(result, list)

        # Assert that each item in the list is a string
        self.assertTrue(all(isinstance(item, str) for item in result))

        # Optionally, check the actual content of the result
        self.assertEqual(result, ["some-id", "another-id"])

if __name__ == "__main__":
    unittest.main()
