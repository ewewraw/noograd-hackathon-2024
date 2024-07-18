"""
This module provides functionality to fetch emails using the Gmail API.

Functions:
    fetch_emails: Fetches emails from the user's Gmail account with optional filters.
"""

from src.utils.gmail_api import GmailAPI

def fetch_emails(query: str = None):
    """
    Fetches emails from the user's Gmail account with optional filters.

    This function creates an instance of the GmailAPI class and uses it to
    retrieve emails from the user's Gmail account. The emails can be filtered
    based on a query string.

    Args:
        query (str, optional): A query string to filter emails. This can be any
                               valid Gmail search query. For example, 'is:unread'
                               to fetch only unread emails, or 'from:example@gmail.com'
                               to fetch emails from a specific sender. Defaults to None.

    Returns:
        list: A list of emails fetched from the Gmail account. Each email
              is represented as a dictionary containing the email ID and content.
    """
    gmail = GmailAPI()
    return gmail.get_emails(query)
