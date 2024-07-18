"""
This module provides a wrapper around the Gmail API to fetch and label emails.

Classes:
    GmailAPI: A class to interact with the Gmail API for fetching and labeling emails.

Methods:
    authenticate: Authenticates the user and retrieves OAuth2 credentials.
    get_emails: Fetches emails from the user's Gmail account with optional filters.
    apply_label: Applies a label to a specific email.
"""

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from src.config import GMAIL_API_KEY

class GmailAPI:
    """
    A class to interact with the Gmail API for fetching and labeling emails.

    Attributes:
        service (Resource): A resource object for interacting with the Gmail API.
    """

    def __init__(self):
        """
        Initializes the GmailAPI instance by setting up the Gmail service.
        """
        self.credentials = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        """
        Authenticates the user and retrieves OAuth2 credentials.

        This method handles the OAuth2 flow to obtain the necessary credentials
        for accessing the Gmail API. If credentials are already available in the
        token file, it uses them; otherwise, it initiates the authentication flow.
        """
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']
        
        # Check if token.json file exists
        if os.path.exists('token.json'):
            self.credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # If there are no (valid) credentials available, let the user log in
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('./credentials.json', SCOPES)
                self.credentials = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.credentials.to_json())
        
        # Build the Gmail service
        self.service = build('gmail', 'v1', credentials=self.credentials)

    def get_emails(self, query=None):
        """
        Fetches emails from the user's Gmail account with optional filters.

        Args:
            query (str, optional): A query string to filter emails. This can be any
                                   valid Gmail search query. For example, 'is:unread'
                                   to fetch only unread emails, or 'from:example@gmail.com'
                                   to fetch emails from a specific sender. Defaults to None.

        Returns:
            list: A list of emails fetched from the Gmail account. Each email
                  is represented as a dictionary containing the email ID and content.
        """
        results = self.service.users().messages().list(userId='me', q=query, labelIds=['INBOX']).execute()
        messages = results.get('messages', [])
        emails = []
        for message in messages:
            msg = self.service.users().messages().get(userId='me', id=message['id']).execute()
            emails.append({
                'id': message['id'],
                'content': msg['snippet'],
            })
        return emails

    def apply_label(self, email_id, label):
        """
        Applies a label to a specific email.

        Args:
            email_id (str): The ID of the email to label.
            label (str): The label to apply to the email. Expected values are
                         'High Priority', 'Medium Priority', or 'Low Priority'.

        Raises:
            ValueError: If the label is not one of the expected values.
        """
        labels = {
            "High Priority": "Label_1",
            "Medium Priority": "Label_2",
            "Low Priority": "Label_3"
        }
        if label not in labels:
            raise ValueError(f"Invalid label: {label}")
        
        label_id = labels.get(label)
        self.service.users().messages().modify(userId='me', id=email_id, body={'addLabelIds': [label_id]}).execute()
