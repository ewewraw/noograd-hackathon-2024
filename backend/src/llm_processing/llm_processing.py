"""
This module provides functionality to process emails using a language model (LLM) to determine their priority.

Functions:
    process_email: Processes one email to determine its priority score using an LLM.
    process_emails: Process multiple emails and return a sorted list of email_ids
"""

import os
import google.generativeai as genai
import typing_extensions as typing
import json

from src.config import GEMINI_API_KEY
from src.models.models import Email, EmailIds


genai.configure(api_key=GEMINI_API_KEY)

def process_email(email):
    """
    Processes an email to determine its priority score using an LLM.

    This function sends the email content to an LLM (language model) to analyze and rank
    the importance of the email. The priority score is then added to the email data.

    Args:
        email (dict): A dictionary representing an email, expected to contain at least
                      the 'content' key with the email content.

    Returns:
        dict: The updated email dictionary with an added 'priority_score' key containing
              the priority score determined by the LLM.
    """
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(f"Rank the importance of this email: {email.content}")
    email.priority_score = response.text.strip()
    return email


def sort_emails(emails: typing.List[Email]) -> list[str]:
    """
    Process a list of emails and return a sorted list of email ids based on their priority.

    Args:
        emails (List[Email]): A list of Email objects.

    Returns:
        List[str]: A sorted list of email IDs.
    """
    model = genai.GenerativeModel('gemini-1.5-pro-latest')

    # Construct the prompt
    email_data = [{"email_id": email["email_id"], "subject": email["subject"], "content": email["content"], "sender": email["sender"], "recipient": email["recipient"]} for email in emails]
    prompt = f"""Here is a list of emails with their subject, content, sender, and recipient: {email_data}. 
    Sort these emails based on their importance and return the sorted list of email IDs using valid JSON."""
    #print(prompt)
    # Call the API
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=list[EmailIds]
        )
    )

    try:
        sorted_email_ids = json.loads(response.text)
        return sorted_email_ids
    except json.JSONDecodeError:
        raise ValueError("Failed to parse the response as JSON")

