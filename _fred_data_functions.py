import fredapi as fa
import pandas as pd
import os 

from _config import fred_directory
from _support_functions import collect_API

def fred_indexes():
    """
    This function will list all of the indexes who's data will be colleccted
    
    """
    indexes = [
                # GDP Index
                'GDP' # # Seasonally Adjusted (Quarterly)

                # Unemployment Rate
                ,'UNRATE' # Seasonally Adjusted (Monthly)

                # Industrial Production
                ,'INDPRO' # Seasonally Adjusted (Monthly)

                # Consumer Price Index
                ,'CPIAUCSL' # Seasonally Adjusted (Monthly)

                # Personal Consumption Expenditure:
                ,'PCE' # Seasonally Adjusted (Monthly)

                # Producer Price Index (All Commodities):
                ,'PPIACO' # Not Seasonally Adjusted (Monthly)

                # U.S. National Home Price Index
                ,'CSUSHPISA' # Seasonally Adjusted (Monthly)

                # Construction Spending
                ,'TTLCONS' # Seasonally Adjusted (Monthly)

                # Stock Market:
                ,'SP500' # Not Seasonally Adjusted (Daily)

                # Retail Sales
                ,'RSXFS' # Seasonally Adjusted (Monthly)

                # Inflation

                # Home Sales

                # Manufacturing Demand

                # Home Building
    ]
    
    return indexes


def collect_fred_data():
    """
    This function will:
        (1) Pull in the Fred API and list of indexes
        (2) Create an object to collect data
        Note: You will need to pip install fredapi on the terminal
    """
    
    fred_API = collect_API('Fred')
    fred = fa.Fred(api_key = fred_API)

    for index in fred_indexes():

        # Will need to read and save all of the datasets
        index_series = pd.DataFrame(fred.get_series(index))
        
        dataframe = pd.DataFrame()
        dataframe['date'] = index_series.index
        dataframe['index_value'] = index_series.values
        dataframe['index_id'] = index
        dataframe.to_csv(f'{fred_directory}/{index}.csv', index=False)