"""Testing of the Analysis."""

import pytest
import pandas
import analyze_stocks

test_df = pandas.DataFrame({'ticker': ['GOOGL','MSFT','COL','GOOGL', 'MSFT', 'GOOGL'],
                            'date': ['2017-02-01', '2017-02-01', '2017-03-13','2017-05-01', '2017-04-17', '2017-02-03'],
                            'open': [12.234, 13, 42.54, 12.44, 50, 34],
                            'close': [43, 12, 1, 3, 4.2, 56],
                            'month': ['2017-02', '2017-02', '2017-03', '2017-05', '2017-04', '2017-02']})

agg_df = analyze_stocks.aggregate_and_convert_to_dictionary(test_df)
result = analyze_stocks.create_output(agg_df)
biggest_loser = analyze_stocks.find_biggest_loser(test_df)

def test_average_open():
    assert result['GOOGL']['2017-02']['average_open'] == 23.12

def test_average_close():
    assert result['GOOGL']['2017-02']['average_close'] == 49.5

def test_all_companies_included():
    assert len(result) == 3

def test_biggest_loser():
    assert biggest_loser == ('MSFT', 2)
