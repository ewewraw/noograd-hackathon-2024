from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from typing import Dict, Any, List
from pydantic import BaseModel


# Import the extract_email_data and extract_multiple_emails_data functions
from src.utils.email_utils import extract_email_data, extract_multiple_emails_data
from src.llm_processing.llm_processing import sort_emails


# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    if request.method == "OPTIONS":
        response = JSONResponse(status_code=204)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response
    response = await call_next(request)
    response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@app.get("/")
async def read_root():
    return {"message": "Hello, You!"}

@app.post("/process_email/")
async def process_email(raw_email: Dict[str, Any]) -> Dict[str, Any]:
    try:
        cleaned_email = extract_email_data(raw_email)
        return cleaned_email
    except Exception as e:
        logger.error(f"Error processing email: {e}")
        raise HTTPException(status_code=500, detail="Error processing email")
    
@app.post("/process_emails/")
async def process_emails(raw_emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    try:
        cleaned_emails = extract_multiple_emails_data(raw_emails)
        return cleaned_emails
    except Exception as e:
        logger.error(f"Error processing emails: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing emails: {str(e)}")
    
@app.post("/sort_emails/")
async def sort(raw_emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    try:
        cleaned_emails = extract_multiple_emails_data(raw_emails)
        sorted_emails = sort_emails(cleaned_emails)
        return sorted_emails
    except Exception as e:
        logger.error(f"Error sorting EMAILS: {e}")
        raise HTTPException(status_code=500, detail="Error sorting emails")


class AuthData(BaseModel):
    token: str

class SheetData(BaseModel):
    token: str
    data: dict

@app.post("/create-sheet/")
async def create_sheet(auth_data: AuthData):
    creds = Credentials(token=auth_data.token)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets().create(body={
        'properties': {'title': 'New Spreadsheet'}
    }).execute()
    sheet_id = sheet['spreadsheetId']
    return {"sheet_id": sheet_id}

@app.post("/write-data/")
async def write_data(sheet_data: SheetData):
    creds = Credentials(token=sheet_data.token)
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = sheet_data.data['sheet_id']
    values = sheet_data.data['values']
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range="Sheet1!A1",
        valueInputOption="RAW", body=body).execute()
    return {"result": result}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
