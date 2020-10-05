from __future__ import print_function

import os.path
import pickle
import time
import base64

from texttable import Texttable

from colorama import init
from colorama import Fore,Style,Back
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build




# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """


    init()
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
    message_count = int(input("How many messages do you wanna see? No.: "))
    print("\n")
    if not messages:
        print('No messages found.')
    else:
        print(Fore.LIGHTRED_EX + '###Messages:####')
        print(Style.RESET_ALL)
        print("\n")
        datetime =''
        fromSender = ''
        subject = ''
        b = ''

        t = Texttable()


    for message in messages[:message_count]:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()

            #print(msg)
            payload = msg['payload']['headers']
            #print(payload)
            for p in payload:
                pdate = p['name']
                if p['name'] == 'Date':
                    datetime = p['value']
                    #print(datetime)
                if p['name'] == 'From':
                    fromSender = p['value']
                    #print(fromSender)
                if p['name'] == 'Subject':
                    subject = p['value']


            #body = msg['payload']['parts'][0]['body']['data']
            #b = base64.urlsafe_b64decode(body.encode('ASCII').decode('utf-8'))
            #print("body")
            #print(b)

            print("Subject:")
            print(subject)
            print(Fore.GREEN + "From:")
            print(fromSender)
            print(Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "Received datetime:")
            print(datetime)
            print(Style.RESET_ALL)
            print("<--MESSAGE-->:")
            print(msg['snippet'])
            time.sleep(2)
            print("----------------------#")
            print("\n")

            #t.add_rows([['Messages received:', ''],['From', fromSender], ['Received datetime', datetime], ['MESSAGE', msg['snippet']], [' ', ' ']])

    #print(t.draw())





if __name__ == '__main__':
    main()