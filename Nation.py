import datetime

def email_type(the_text, mesg_date):
    low_bal = False
    balance = None
    the_date = None
    transactions = []
    dates = []
    type_trans = []
    transaction_set = []

    #print the_text
    the_text = the_text.splitlines()

    #print "Local Date:", real_date.strftime("%a, %d %b %Y %H:%M:%S")
    if len(the_text) is 1:
        line_text = str.split(the_text[0])
        list_lenth = len(line_text)

        if '\xc2\xa3500.' in line_text[list_lenth-1]:
            low_bal = True
            balance = make_float(line_text[3])
            the_date = date_sort(line_text[5:8], mesg_date)

    else:
        line_text = str.split(the_text[0])
        balance = make_float(line_text[3])
        the_date = date_sort(line_text[5:8], mesg_date)

        the_text.pop(0)
        for trans in the_text:
            line_text = str.split(trans)
            dates.append(date_make(line_text[0:2], mesg_date))
            transactions.append(make_float(line_text[3]))
            type_trans.append(line_text[2])
            transaction_set.append([transactions, dates, type_trans])

    return [[low_bal, balance, the_date],transaction_set]

def date_sort(mini_date, rough_date):
    mini_date = ' '.join(mini_date)
    mini_date = mini_date + str(rough_date.strftime(" %Y"))
    mini_date = mini_date.replace(".", "")
    mini_date = datetime.datetime.strptime(mini_date, "%d %b %H:%M %Y")
    #print "Local Date:", mini_date.strftime("%a, %d %b %Y %H:%M")
    return mini_date

def date_make(mini_date, rough_date):
    mini_date = ' '.join(mini_date)
    mini_date = mini_date + str(rough_date.strftime(" %Y"))
    mini_date = mini_date.replace(".", "")
    mini_date = datetime.datetime.strptime(mini_date, "%d %b %Y")
    #print "Local Date:", mini_date.strftime("%a, %d %b %Y %H:%M")
    return mini_date

def make_float(themouny):
    the_float = float(themouny[2:-1])
    if themouny[-1:] == "-":
        the_float = - the_float
    return the_float