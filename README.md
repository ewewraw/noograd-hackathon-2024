# Inbox0 - A Smart Gmail Prioritization Tool

**Team Members:** Natalia Markoborodova, Dirk Breeuwer

## Introduction

Inbox0 is a Chrome extension designed to improve your email management experience. We tackle the common challenge of efficiently managing and prioritizing a high volume of incoming emails, particularly in professional settings.

**Problem:**

* Average new emails per day: **XX**
* Percentage of important/urgent emails: **X%**
* Hours spent sorting/prioritizing emails: **XX**
* Potential yearly time savings: **XX hours**

## Solution

Our solution seamlessly integrates with Gmail to streamline your inbox. It fetches unread emails, employs the power of Google Gemini to intelligently prioritize them, and generates a concise summary email highlighting the most crucial messages and their key details.

**Key Features:**

* Fetches unread emails from your Gmail account.
* Leverages Google Gemini's LLM capabilities to sort emails by importance and extract vital information.
* Delivers a sorted list of email IDs with summaries, action items, and upcoming deadlines.

## Technical Architecture

TODO: [Architecture diagram]

**Components:**

* **Chrome Extension:** Handles user authentication, connects to the Gmail API to retrieve unread emails.
* **Backend (Python Flask):** Processes and sorts emails using Google Gemini, constructs and sends the summary email.

**Technologies Used:**

* OAuth
* Google Gemini LLM
* Gmail API
* Docker

## Demonstration

TODO: [Link to a demo]

* Fetching emails from Gmail
* Processing and sorting using Google Gemini
* Displaying the final sorted list with key information

## Future Enhancements

* **Improved Prioritization:** Incorporate additional signals for refined prioritization:
    * Sender details (job level, relationship, etc.)
    * Recipient details
    * Deadline urgency
    * Historical email handling patterns
    * UI

## Getting Started

1. **Clone the repository:** `git clone https://github.com/your-username/Inbox0.git`
2. **Install dependencies:** 
    * Backend: `cd backend && pip install -r requirements.txt`
    * Frontend: `cd frontend && npm install`
3. **Set up environment variables:**
    * Create `.env` files in `backend` directory and fill in the required API keys and credentials.
    * Update `frontend/manifest.json` with your keys and credentials.
4. **Run the application:**
    * Backend: `cd backend && python app.py`
    * Frontend: `cd frontend && npm run build` (then load the unpacked extension in Chrome)

