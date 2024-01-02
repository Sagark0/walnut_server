import os.path
from datetime import datetime
import psycopg2
from django.conf import settings
import base64 
from bs4 import BeautifulSoup 

from . import utils

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def gmail(existing_transaction_ids):
    creds = None
    credentials_path = os.path.join(settings.BASE_DIR, "credentials.json")
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("gmail", "v1", credentials=creds)
        mails = fromPhonepe(service, existing_transaction_ids)

        return mails

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")

def fromPhonepe(service, existing_transaction_ids):
    after = " after:"+datetime.now().replace(day=1).strftime('%Y/%m/%d')
    query="from: noreply@phonepe.com subject:Sent to" + after
    results = service.users().messages().list(userId="sagar.ranchi31@gmail.com", q=query).execute()
    messages = results.get('messages')
    mails = []
    for msg in messages:
        txt = service.users().messages().get(
            userId="me", id=msg['id']).execute()
        if txt['id'] not in existing_transaction_ids:
            existing_transaction_ids.add(txt['id'])
            phonepeSnippet = utils.Phonepe(txt["snippet"])
            mailObject = phonepeSnippet.getMailObject()
            mailObject["transaction_id"] = txt["id"]
            mails.append(mailObject)
    return mails    

def fromHDFC(service, existing_transaction_ids):
    before = " before:"+datetime.now().strftime('%Y/%m/%d')
    after = " after:"+datetime.now().replace(day=1).strftime('%Y/%m/%d')
    query = "from:alerts@hdfcbank.net subject:(❗ You have done a UPI txn. Check details!)" + after
    results = service.users().messages().list(userId="me", q=query).execute()
    messages = results.get('messages')
    mails = []
    for msg in messages:
        txt = service.users().messages().get(
            userId="me", id=msg['id']).execute()
        if txt['id'] not in existing_transaction_ids:
            mailObject = {}
            mailObject["transaction_id"] = txt['id']
            snippet = txt['snippet']
            hdfcSnippet = utils.HDFC(snippet)
            mailObject["amount"] = hdfcSnippet.getAmount()
            mailObject["details"] = hdfcSnippet.getDetails()
            mailObject["date"] = hdfcSnippet.getDate()
            mailObject["category"] = "uncategorised"
            mailObject["time"] = "12:00:00"
            mails.append(mailObject)
    return mails
            