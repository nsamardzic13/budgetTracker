import argparse
import json
import smtplib
import ssl
from email.message import EmailMessage


# arguments
parser = argparse.ArgumentParser()
parser.add_argument('--subject')
parser.add_argument('--filename')

args = parser.parse_args()
subject = args.subject

with open('email_credentials.json') as f:
    gmail_credentials = json.load(f)

# create mail content
mail_content = EmailMessage()
mail_content['From'] = gmail_credentials['from']
mail_content['To'] = gmail_credentials['to']
mail_content['Subject'] = subject
mail_content.set_content('Attached')

# attach file to the email
with open(args.filename, 'rb') as file:
    file_data = file.read()
    file_type = args.filename.split('.')[-1]
    file_name = file.name

mail_content.add_attachment(file_data, maintype='html', subtype=file_type, filename=file_name)
context = ssl.create_default_context()

# send the email
try:
    server = smtplib.SMTP(host=gmail_credentials['host'], port=gmail_credentials['port'])
    server.starttls(context=context)
    server.login(user=gmail_credentials['smtpUser'], password=gmail_credentials['password'])
    server.send_message(mail_content)
    server.close()
    print('Email sent successful')
except Exception as e:
    print('Something went wrong:')
    print(e)