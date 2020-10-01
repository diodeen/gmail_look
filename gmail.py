from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import time

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    #results = service.users().labels().list(userId='me').execute()
    #labels = results.get('labels', [])

    #Get Messages
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    #if not labels:
    message_count = int(input("How many messages do you wanna see"))
    print("\n")
    if not messages:
        print('No messages found.')
    else:
        print('###Messages:####')
        print("\n")
        datetime =''
        fromSender = ''

        for message in messages[:message_count]:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()

            payload = msg['payload']['headers']
            #print(payload)
            for p in payload:
                pdate = p['name']
                if p['name'] == 'Date':
                    datetime = p['value']
                    print(datetime)
                if p['name'] == 'From':
                    fromSender = p['value']
                    print(fromSender)

            print("From:")
            print(fromSender)
            print("Received datetime:")
            print(datetime)
            print("<--MESSAGE-->:")
            print(msg['snippet'])
            time.sleep(2)
            print("----------------------#")
            print("\n")
if __name__ == '__main__':
    main()