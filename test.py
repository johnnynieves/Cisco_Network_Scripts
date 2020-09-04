import smtplib
import ssl
import os


def creds():
    with open('/home/johnny/creds') as f:
        credentials = f.read()
    return credentials.splitlines()


def send_email_report():
    email = 'network.site.manager@gmail.com'
    password = ''

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(email, password)

        subject = 'Network Reports'
        body = ' A bunch of reports you need to look at'

        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail('network.site.manager', 'johnny0nieves@gmail.com', msg)


if __name__ == "__main__":
    send_email_report()
