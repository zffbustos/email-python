import json
import os
import pickle
import base64
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import requests

# Define the scope for Gmail API access
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail(credentials_file, token_file=None):
    """Authenticate the user with Gmail API."""
    creds = None
    # The token.pickle stores the user's access and refresh tokens and is
    # created automatically when the authorization flow completes for the first time.
    if token_file and os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # If there are no valid credentials, request the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_file or 'token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def get_email_details(message):
    """Extract the email details (From, To, Subject, Body) from a message."""
    headers = message['payload']['headers']

    # Extract 'From', 'To', and 'Subject'
    from_email = next(header['value'] for header in headers if header['name'] == 'From')
    to_email = next(header['value'] for header in headers if header['name'] == 'To')
    subject = next((header['value'] for header in headers if header['name'] == 'Subject'), '(No Subject)')

    # Extract the email body (plain text part)
    if 'parts' in message['payload']:
        for part in message['payload']['parts']:
            if part['mimeType'] == 'text/plain':
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                break
    else:
        # If the email is not multipart
        body = base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')

    return from_email, to_email, subject, body

def get_inbox_messages(credentials_file, token_file=None):
    """Fetch and print a list of emails from the inbox."""
    creds = authenticate_gmail(credentials_file,token_file)
    service = build('gmail', 'v1', credentials=creds)

    # Get the list of messages in the user's inbox
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    messages = results.get('messages', [])

    if not messages:
        print('No messages found.')
    else:
        print('Messages:')
        for message in messages:
            # Get the full message details
            msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
            from_email, to_email, subject, body = get_email_details(msg)
            print("-" * 50)  # Separator between emails
            # Print the message details
            print(f"From: {from_email}")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")

def get_credentials_from_vault(vault_addr, vault_token=None):
    if not vault_token:
        print('No token provided.')
        sys.exit(1)
    else:
        url = f"{vault_addr}/v1/secret/data/gmail-api"
        headers = {
            'X-Vault-Token': vault_token
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            secret = response.json()['data']['data']['secret/gmail-api/credentials']
            return json.loads(base64.b64decode(secret).decode('utf-8'))
        else:
            print(f"Error fetching secret from Vault: {response.text}")


def get_token_from_vault(vault_addr, vault_token=None):
    if not vault_token:
        print('No token provided.')
        sys.exit(1)
    else:
        url = f"{vault_addr}/v1/secret/data/gmail-api"
        headers = {
            'X-Vault-Token': vault_token
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            secret = response.json()['data']['data']['secret/gmail-api/token']
            return pickle.loads(base64.b64decode(secret))
        else:
            print(f"Error fetching secret from Vault: {response.text}")

def dump_credentials_to_file(credentials, token):
    with open('credentials.json', 'w') as f:
        json.dump(credentials, f)
    with open('token.pickle', 'wb') as f:
        pickle.dump(token, f)

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("Usage: python3 gmail_messages_stored_credentials.py <vault_address> <vault_token>")
        sys.exit(1)
    
#   Extract Vault credentials from environment variables
    VAULT_ADDRESS = sys.argv[1]
    VAULT_TOKEN = sys.argv[2]
#   Access Vault to obtain credentials and token
    credentials = get_credentials_from_vault(VAULT_ADDRESS, VAULT_TOKEN)
    token = get_token_from_vault(VAULT_ADDRESS, VAULT_TOKEN)
#   Dump credentials and token to files
    dump_credentials_to_file(credentials, token)
#   Call the function with the credentials file and token file
    get_inbox_messages('credentials.json', 'token.pickle')
