from email import message
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from fileinput import filename
import os.path
import base64
from pydoc import plain
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
import pickle


CLIENT_SECRET_FILE = 'credentials.json'
SCOPES = ['https://mail.google.com/']


#Create Email Service
def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service

    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None


# Add attachment to email
def add_attachment(file, msg):
    content_type, encoding = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'

    main_type, sub_type = content_type.split('/', 1)


    with open(file, 'rb') as fp:
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        file_name = os.path.basename(file)
        encoders.encode_base64(msg)
        msg.add_header('Content-Disposition', 'attachment', filename=file_name)
        messag.attach(msg)


service = Create_Service(CLIENT_SECRET_FILE, 'gmail', 'v1', SCOPES)


# Single line message
msg = "Hello" 

# Create Message Structure
messag = MIMEMultipart()
messag['from'] = "Sender's Name<Sender's Email>"
messag['to'] = "Reciever's Email"
messag['subject'] = "Subject of Email"
msg = MIMEText(msg, 'plain')
messag.attach(msg)

#Uncomment the following code to add an attachment
#file = "file_name"
#add_attachment(file, msg)


raw_string = base64.urlsafe_b64encode(messag.as_bytes()).decode()

EMAILmessage = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
print(EMAILmessage)