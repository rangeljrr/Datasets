import fredapi as fa
import pandas as pd
import os 
from datetime import datetime as dt

from _config import fred_directory
from _support_functions import collect_API, create_date_range

def fred_indexes():
    """
    This function will list all of the indexes who's data will be colleccted
    
    """
    indexes = {# GDP Index
               'GDP':'Q' # # Seasonally Adjusted (Quarterly)

                # Unemployment Rate
                ,'UNRATE':'M' # Seasonally Adjusted (Monthly)

                # Industrial Production
                ,'INDPRO':'M' # Seasonally Adjusted (Monthly)

                # Consumer Price Index
                ,'CPIAUCSL':'M' # Seasonally Adjusted (Monthly)

                # Personal Consumption Expenditure:
                ,'PCE':'M' # Seasonally Adjusted (Monthly)

                # Producer Price Index (All Commodities):
                ,'PPIACO':'M' # Not Seasonally Adjusted (Monthly)

                # U.S. National Home Price Index
                ,'CSUSHPISA':'M' # Seasonally Adjusted (Monthly)

                # Construction Spending
                ,'TTLCONS':'M' # Seasonally Adjusted (Monthly)

                # Stock Market:
                ,'SP500':'D' # Not Seasonally Adjusted (Daily)

                # Retail Sales
                ,'RSXFS':'M' # Seasonally Adjusted (Monthly)

                # Inflation

                # Home Sales

                # Manufacturing Demand

                # Home Building
    }
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

    for index in list(fred_indexes().keys()):

        # Will need to read and save all of the datasets
        index_series = pd.DataFrame(fred.get_series(index))
        
        dataframe = pd.DataFrame()
        dataframe['date'] = index_series.index
        dataframe['index_value'] = index_series.values
        dataframe['index_id'] = index
        dataframe.to_csv(f'{fred_directory}/{index}.csv', index=False)
        

def convert_Q_to_M(dataframe):
    """ This function will convert a quarterly dataframe to monthly 
        using a linear interpolation """
    date_range = create_date_range()
    dataframe = date_range.merge(dataframe, how='left', on = 'date')
    dataframe['index_value'] = dataframe['index_value'].interpolate(method='linear')
    
    return dataframe

def convert_D_to_M(dataframe):
    """ This function will convert a daily dataframe to monthly 
        using a linear interpolation """

    return dataframe.resample(on='date', rule='M').max().reset_index(drop=True)

def create_master_file():
    
    """ This function will take in any file type Q M D and merge it all into one dataset """
    
    indexes = list(fred_indexes().keys())
    index_types = list(fred_indexes().values())

    master_file = create_date_range()

    for i in range(len(indexes)):

        index = indexes[i]
        index_type = index_types[i]


        iter_df = pd.read_csv(f'{fred_directory}/{index}.csv').iloc[:,0:2]
        iter_df['date'] = pd.to_datetime(iter_df['date'])
        #iter_df.date = [i.to_period('M') for i in iter_df.date]

        if index_type == 'Q':
            iter_df.date = [i.to_period('M') for i in iter_df.date]
            iter_df = convert_Q_to_M(iter_df)

        elif index_type == 'M':
            iter_df.date = [i.to_period('M') for i in iter_df.date]
            pass

        elif index_type == 'D':
            iter_df = convert_D_to_M(iter_df)
            iter_df.date = [i.to_period('M') for i in iter_df.date]

        # We need to change the column name from index_id to the name of te index
        iter_df.columns = ['date',index]

        master_file = master_file.merge(iter_df, how='left', on = 'date')
        
    master_file.to_csv(f'{fred_directory}/MASTER.csv', index=False)