import pandas as pd
import os

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