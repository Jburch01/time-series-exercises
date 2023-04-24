import pandas as pd
from datetime import timedelta, datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

from env import get_db_url
import os
# from acquire import wrangle_store_data

import warnings
warnings.filterwarnings("ignore")

# plotting defaults
plt.rc('figure', figsize=(13, 7))
plt.style.use('seaborn-whitegrid')
plt.rc('font', size=16)

from acquire import germany_opsd



def get_store_data():
    '''
    Returns a dataframe of all store data in the tsa_item_demand database and saves a local copy as a csv file.
    '''
    query = '''
    SELECT *
    FROM items
    JOIN sales USING(item_id)
    JOIN stores USING(store_id) 
    '''
    
    df = pd.read_sql(query, get_db_url('tsa_item_demand'))
    
    df.to_csv('tsa_item_demand.csv', index=False)
    
    return df


def wrangle_store_data():
    filename = 'tsa_store_data.csv'
    
    if os.path.isfile(filename):
        df = pd.read_csv(filename, index_col=0)
    else:
        df = get_store_data()
        
    return df


def prep_store_data():
    df = wrangle_store_data()
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    df = df.set_index('sale_date')
    df['month'] = df.index.month_name()
    df['day'] = df.index.day_name()
    df['sales_total'] = df.sale_amount * df.item_price
    return df



def prep_germany_opsd():
    df = germany_opsd()
    df.Date = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    df['month'] = df.index.month_name()
    df['year'] = df.index.year
    df.fillna(0, inplace=True)
    df['Wind_Solar'] = df['wind'] + df['solar']
    return df