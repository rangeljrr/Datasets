import pandas as pd
import os
from datetime import datetime as dt

def collect_API(API_name):
    """ 
    This function is used mainly to pull in the API Keys
    Current Options:
        - Fred
    """

    # To request an API for Fred, you will need to create an account here:
    # https://fredaccount.stlouisfed.org/login/secure/
    APIs = pd.read_csv('_API_book.csv')
    API_key = APIs[APIs['Source'] == API_name]['Key'][0]
    return API_key

def check_directory(directory):
    """ This function will check if the Fred directory exists """
    if os.path.isdir(directory) == False:
        os.mkdir(directory)
        
def create_date_range():
    # Need to create a master file to store all indexes
    now = dt.now()
    min_month = '2010-01-01'
    max_month = '{}-{}-01'.format(now.year, now.month)
    months = pd.period_range(min_month, max_month, freq='M')
    months = pd.DataFrame(months, columns=['date'])
    
    return months