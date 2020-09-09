import smtplib
import os
from email.message import EmailMessage


def creds():
    with open('/home/johnny/creds') as f:
        credentials = f.read()
    return credentials.splitlines()


def send_email_report():
    email = creds()[2]
    password = creds()[3]
    directory = '/home/johnny/err_disabled/'

    msg = EmailMessage()
    msg['Subject'] = 'Your Reports Check it out!!'
    msg['From'] = email
    msg['To'] = email
    msg.set_content('Check you what interfaces are err-disabled')

    with open(directory, 'rb') as f:
        file_data = f.read()
        file_type = 'txt'

    # attachments = ['this will be a search in the directory']
    msg.add_attachment(file_data, maintype)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email, password)
        smtp.send_message(msg)
    print('Email Sent')


def check_files():
    pass


if __name__ == "__main__":
    send_email_report()
  