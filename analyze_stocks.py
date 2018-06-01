"""Implementation of Stock Analysis."""

import quandl
import json
import os
import pprint
import sys
from datetime import datetime
import numpy as np

quandl.ApiConfig.api_key = os.environ['QUANDL_CODE']

def extract_data(tickers = ['COF', 'GOOGL', 'MSFT'], start_date = '2017-01-01', end_date = '2017-06-30'):
    """Extract the open and close stock prices for chosen companies in the given date range."""
    dataframe = quandl.get_table('WIKI/PRICES', qopts = { 'columns': ['ticker', 'date', 'open', 'close'] }, \
                                 ticker = tickers, date = { 'gte': start_date, 'lte': end_date})
    dataframe['month'] = dataframe['date'].apply(lambda x:x.strftime('%Y-%m')) # Create month column
    return dataframe

def aggregate_and_convert_to_dictionary(raw_dataframe):
    """Using raw_data, aggregate by month and ticker and then convert to list of dictionaries."""
    df_agg  = raw_dataframe.groupby(['month', 'ticker']).mean() # aggregate and get average of open/close values
    output = json.loads(df_agg.to_json(orient='table')) # convert to json, then to dictionary
    return output['data']

def create_output(data):
    """Using input dictionary, format the output in a more desireable output."""
    output = {}
    for element in data:
        open_val = round(element['open'], 2)
        close_val = round(element['close'], 2)
        month = element['month']
        ticker = element['ticker']
        if element['ticker'] not in output:
            output[ticker] = {month : {'average_open': open_val, 'average_close' : close_val}}
        else:
            output[ticker][month] = {'average_open': open_val, 'average_close' : close_val}
    return output

def find_biggest_loser(data):
    """Using the input data, determine the stock which had most days closing lower then opening."""
    data['loser_flag'] = np.where(data['close'] < data['open'], 1, 0)
    loser_count_df = data.groupby(['ticker']).sum()
    biggest_loser = loser_count_df[loser_count_df['loser_flag'] == max(loser_count_df['loser_flag'])]
    biggest_loser = json.loads(biggest_loser.to_json(orient='table'))['data'][0]
    print('The biggest loser is ' + biggest_loser['ticker'] + ' which closed loser than it opened on ' +  str(biggest_loser['loser_flag']) + ' days.')
    return biggest_loser['ticker'], biggest_loser['loser_flag']



if __name__ == '__main__':
    pp = pprint.PrettyPrinter()
    raw_df = extract_data()
    agg_df = aggregate_and_convert_to_dictionary(raw_df)
    result = create_output(agg_df)
    print(raw_df)
    pp.pprint(result)
    if len(sys.argv) > 1 and sys.argv[1] == 'loser':
        print('\n')
        find_biggest_loser(raw_df)
