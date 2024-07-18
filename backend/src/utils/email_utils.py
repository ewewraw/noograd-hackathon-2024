from src.models.models import Email

def extract_email_data(raw_email) -> Email:
    """
    Extract relevant information from raw email data.

    Args:
        raw_email (dict): The raw email data from the Gmail API.

    Returns:
        Email: A dictionary with the extracted email information.
    """
    headers = {header['name']: header['value'] for header in raw_email['payload']['headers']}
    email = {
        "email_id": raw_email["id"],
        "sender": headers.get("From", ""),
        "recipient": headers.get("To", ""),
        "subject": headers.get("Subject", ""),
        "content": raw_email["snippet"]
    }
    return email

def extract_multiple_emails_data(raw_emails) -> list:
    """
    Extract relevant information from an array of raw email data.

    Args:
        raw_emails (list): A list of raw email data from the Gmail API.

    Returns:
        list: A list of dictionaries with the extracted email information.
    """
    emails = []
    for raw_email in raw_emails:
        email = extract_email_data(raw_email)
        emails.append(email)
    return emails