#!/usr/bin/env python
import matplotlib
matplotlib.use('Agg')

import sys
import imaplib
import smtplib
import getpass
#import email
import datetime
import json
import Fun
import matplotlib.pyplot as plt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

M = imaplib.IMAP4_SSL('imap.gmail.com')

with open('email.json', 'r') as f:
    config = json.load(f)


try:
    M.login(config["get"]["EMAIL"], config["get"]["PASSWORD"])
except imaplib.IMAP4.error:
    print "LOGIN FAILED!!! "

rv, data = M.select("Inbox")
if rv == "OK":
    print "Processing mailbox...\n"
    nationwide = Fun.process_mailbox(M, "Nationwide") # todo "HSBC", "BARCLAYS"
    M.close()
M.logout()

nation_balance = [sublist[0] for sublist in nationwide]
#print nation_balance
bal = [sublist[1] for sublist in nation_balance]
bal = [x for x in bal if x is not None]
low = [sublist[0] for sublist in nation_balance]
low = [x for x in low if x is not None]
dayz = [sublist[2] for sublist in nation_balance]
dayz = [x for x in dayz if x is not None]

print bal
print dayz
plt.plot(dayz, bal)
#plt.show()
plt.savefig('nationAllBal.png')

# Send an HTML email with an embedded image and a plain text message for
# email clients that don't want to display the HTML.

# Define these once; use them twice!
strFrom = config["get"]["EMAIL"]
strTo = config["send"]["EMAIL"]

# Create the root message and fill in the from, to, and subject headers
msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = 'test message'
msgRoot['From'] = strFrom
msgRoot['To'] = strTo
msgRoot.preamble = 'This is a multi-part message in MIME format.'

# Encapsulate the plain and HTML versions of the message body in an
# 'alternative' part, so message agents can decide which they want to display.
msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)

msgText = MIMEText('This is the alternative plain text message.')
msgAlternative.attach(msgText)

# We reference the image in the IMG SRC attribute by the ID we give it below
msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
msgAlternative.attach(msgText)

# This example assumes the image is in the current directory
fp = open('nationAllBal.png', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()

# Define the image's ID as referenced above
msgImage.add_header('Content-ID', '<image1>')
msgRoot.attach(msgImage)

# Send the email (this example assumes SMTP authentication is required)
smtp = smtplib.SMTP('smtp.gmail.com:587')
smtp.ehlo()
smtp.starttls()
smtp.login(strFrom, config["get"]["PASSWORD"])
smtp.sendmail(strFrom, strTo, msgRoot.as_string())
smtp.quit()
