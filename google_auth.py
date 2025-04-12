import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes for google calendar API
SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar",
]


# Google calendar Authentication
def authenticate_calendar():
    creds = None
    if os.path.exists("calendartoken.json"):
        creds = Credentials.from_authorized_user_file("calendartoken.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(
                port=63275, access_type="offline", prompt="consent"
            )
        with open("calendartoken.json", "w") as token:
            token.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)
