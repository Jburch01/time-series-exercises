import pandas as pd
import numpy as np

import requests



def get_table(name):
    df = pd.DataFrame()
    url = f'https://swapi.dev/api/{name}/'
    while url:
        page = requests.get(url)
        df = pd.concat([df, pd.DataFrame(page.json()['results'])], axis=0, ignore_index=True)
        url = page.json()['next']
    return df
        
    
    
def germany_opsd():
    return pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')