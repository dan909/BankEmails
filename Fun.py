import sys
import imaplib
import getpass
import email
import datetime
import Nation
import re
import pandas as pd

def process_mailbox(M, email_name):
    all_emails = []
    all_data = []

    bank = pd.DataFrame({ 'BalanceLow': [],
                          'Balance': [],
                          'Date': [],
                          'Transactions': [],
                          'Dates': [],
                          'Types': []})
    #print bank.columns

    # rv is the type, OK or NO. data is the actual data
    # Get emails from Nationwide #"Nationwide@unknown.email"
    rv, data = M.search("utf-8", '(FROM ' + email_name + '@unknown.email)')
    data = data[0].split()
    all_emails.extend(data)

    if rv != "OK":
        print "No messages found for " + email_name

    for num in all_emails:

        rv, email_data = M.fetch(num, '(RFC822)')
        msg = email.message_from_string(email_data[0][1])

        #print "Message %s: %s" % (num, msg["Subject"])
        #print "Raw Date:", msg["Date"]
        real_date = msg["Date"]

        date_tuple = email.utils.parsedate_tz(msg["Date"])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            #print "Local Date:", local_date.strftime("%a, %d %b %Y %H:%M:%S")
            real_date = local_date

        #print "Body:\n%s" % (msg.get_payload(decode=True))
        if email_name is 'Nationwide':
            item = Nation.email_type(msg.get_payload(decode=True), real_date)
            #print item
            #print " "

            all_data.append(item)
    return all_data