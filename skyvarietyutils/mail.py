# -*- coding: utf-8 -*-

import socket
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# config = {
#    'email': 'xx@gmail.com',
#    'from': 'xx <xx@xx.xx.xx>',
#    'password': 'xx',
#    'reply_to': 'xx@xx.xx.xx'
#  }
def send_gmail(config, subject, body, to):
  msg = MIMEMultipart('alternative')
  msg["Subject"] = subject
  msg["From"] = config['from']
  msg["To"] = to
  msg.add_header('reply-to', config['reply_to'])
  msg.attach(MIMEText(body, 'html'))

  server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
  server.ehlo()
  server.login(config['email'], config['password'])
  server.sendmail(config['email'], to, msg.as_string())
  server.close()
