import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.axes
from numpy import ndarray
from pprint import pprint


INPUT_FILE = '/home/denis/Documents/github/agora/data/01-june2014.csv'


def transactions_per_vendor(in_data: pd.DataFrame):
    plt.subplots(figsize=(20, 200))
    vendor_name: pd.Series = in_data.get('vendor_name')
    c: pd.Series = vendor_name.value_counts()
    g = c.plot(kind='barh')
    g.get_figure().savefig('transaction_per_vendor.png')


def transactions_per_origin(in_data: pd.DataFrame):
    plt.subplots(figsize=(20, 200))
    location_from: pd.Series = in_data.get('ship_from')
    c: pd.Series = location_from.value_counts()
    g = c.plot(kind='barh')
    g.get_figure().savefig('transaction_per_origin.png')


def run():
    # Load the data.
    data: pd.DataFrame = pd.read_csv(filepath_or_buffer=INPUT_FILE,
                                     sep=',',
                                     quotechar='"',
                                     dialect='excel',
                                     parse_dates=['Date'],
                                     date_parser=lambda x: datetime.strptime(x, '%Y-%m-%d'),
                                     dtype={
                                         'hash': str,
                                         'btc': float,
                                         'usd': float,
                                         'rate': float,
                                         'ship_from': str,
                                         'vendor_name': str,
                                         'name': str
                                     })

    # ship_from: pd.Series = data.get('ship_from')
    # ids: ndarray = ship_from.unique()
    # for name in ids:
    #     print("  - {}".format(name))



    # print(g.__class__)
    # ids: ndarray = vendor_name.unique()
    # for name in ids:
    #     print("  - {}".format(name))
    # print("\n".join(ids))
    # print(ship_from.unique())

    # transactions_per_vendor(data)
    transactions_per_origin(data)
