"""
This module provides functionality to label emails based on their priority score.

Functions:
    label_emails: Labels a list of emails based on their priority scores.
    determine_label: Determines the label for an email based on its priority score.
"""

from src.utils.gmail_api import GmailAPI

def label_emails(emails):
    """
    Labels a list of emails based on their priority scores.

    This function iterates over a list of emails, determines the appropriate label for each
    email based on its priority score, and applies the label using the Gmail API.

    Args:
        emails (list): A list of email dictionaries, each expected to have 'id' and 'priority_score' keys.
    """
    gmail = GmailAPI()
    for email in emails:
        label = determine_label(email['priority_score'])
        gmail.apply_label(email['id'], label)

def determine_label(priority_score):
    """
    Determines the label for an email based on its priority score.

    This function evaluates the priority score of an email and returns the corresponding
    label as a string. The labeling criteria are:
    - "High Priority" for scores above 75
    - "Medium Priority" for scores above 50 but not exceeding 75
    - "Low Priority" for scores of 50 or below

    Args:
        priority_score (int): The priority score of the email.

    Returns:
        str: The label corresponding to the priority score.
    """
    if priority_score > 75:
        return "High Priority"
    elif priority_score > 50:
        return "Medium Priority"
    else:
        return "Low Priority"
