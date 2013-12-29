#!/usr/bin/env python

import requests
import os
import csv
from creds import USERNAME, PASSWORD, EMPLOYEE_ID

CSV_FILE    = 'invoices.csv'
USER_AGENT  = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.114 Safari/537.36' 

def get_login_cookies():
    """Login and get the session cookie for further requests"""
    data = {
        'email': USERNAME,
        'password': PASSWORD
    }
    r = requests.post('https://www.intouchaccounting.com/portal/auth/login', 
                      data=data, 
                      allow_redirects=True, 
                      headers={'User-Agent': USER_AGENT})
    return dict(r.cookies)

def add_expense(date, detail, amount, moreinfo, cookies):
    """Upload the expense"""

    detail_to_post_params = {
        'Lunch': { 
            'expensetype': 1,
            'subcat': 1,
            'detail': 'Lunch',
            'moreinfo': moreinfo,
            'total': amount,
            'vat': 0,
            'net': amount,
            'expensetypetxt': 19,
            'date': date
        }
    }
    if detail not in detail_to_post_params:
        print 'Skipping %s (Not supported)' % detail
        return False, None

    data = detail_to_post_params[detail]
    data['employeeid'] = EMPLOYEE_ID

    r = requests.post('https://www.intouchaccounting.com/portal/expense/insert', 
                      data=data,
                      cookies=cookies,
                      headers={'User-Agent': USER_AGENT})
    print 'Added expense %s) %s - %s' % (date, detail, amount)
    return True, r

def read_expenses(filename):
    """
    The csv file should be formatted as: DATE (DD/MM/YYYY), Detail, Amount, MoreInfo
    """

    expenses = []
    if not os.path.isfile(filename):
        raise Exception('Could not read: %s' % filename)

    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            expenses.append(row)
    return expenses

if __name__ == '__main__':
    cookies = get_login_cookies()
    expenses = read_expenses('expenses.csv')
    for date, detail, amount, moreinfo in expenses:
        add_expense(date, detail, amount, moreinfo, cookies)

    """
    add_expense('09/08/13', 6.00, 'Lunch', 'Receipt', cookies)
    """


