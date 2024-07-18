# Email Prioritization Backend

## Setup

1. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

2. Set up environment variables in a `.env` file:
    ```
    GMAIL_API_KEY=your_gmail_api_key
    LLM_API_KEY=your_llm_api_key
    ```

3. Run the server:
    ```
    uvicorn src.main:app --reload
    ```
