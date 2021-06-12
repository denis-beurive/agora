"""
    Usage (from the project root folder):

        python -m agora.agora --verbose ./data ./output

    Note: make sure to initialise the Python environment first! (read the file README.md)

        pipenv install --dev
"""

from typing import Any, Pattern, Match, Dict
import argparse
import pandas as pd
from datetime import datetime
import os
import re
from enum import Enum
from .stat import get_count_per_column_value, \
    get_median_per_column_value, \
    get_average_per_column_value, \
    get_stat_per_column_value
from .graph import hbar, single_boxplot


class GraphType(Enum):
    TRANSACTION_COUNTS = 0
    TRANSACTION_BTC = 1


INPUTS = [
    '01-june2014.csv',
    '02-july2014.csv',
    '03-aug2014.csv',
    '04-sept2014.csv',
    '05-oct2014.csv',
    '06-nov2014.csv',
    '07-dec2014.csv',
    '08-jan2015.csv',
    '09-feb2015.csv',
    '10-mar2015.csv',
    '11-apr2015.csv',
    '12-may2015.csv',
    '13-june2015.csv',
    '14-july2015.csv'
]


def classname(obj: Any) -> str:
    cls = type(obj)
    module = cls.__module__
    name = cls.__qualname__
    if module is not None and module != "__builtin__":
        name = module + "." + name
    return name


def load_csv(path: str) -> pd.DataFrame:
    """
    Load data from CSV file.

    This function skips the rows that contain empty vendor names.

    :param path: path to the CSV file to load.
    :return: the loaded data.
    """

    def regex_filter(val: str):
        filter_pattern: Pattern = re.compile('^\\s*\\n')
        if val:
            m: Match = re.search(filter_pattern, val)
            return m is None
        else:
            return True

    data: pd.DataFrame = pd.read_csv(filepath_or_buffer=path,
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
    return data.loc[data['vendor_name'].apply(regex_filter)]


def draw_transactions_counts_repartition(data: pd.DataFrame, output_path: str) -> None:
    sub_data = get_count_per_column_value(data, 'vendor_name')
    counts: pd.Series = sub_data['count']
    df = pd.DataFrame({
        'x': pd.Series(['transactions' for _ in range(len(counts))]),
        'y': counts
    })
    single_boxplot(df, 'x', 'y', output_path)


def draw_transactions_values_repartition(data: pd.DataFrame, output_path: str) -> None:
    sub_data = get_average_per_column_value(data, 'vendor_name', 'btc')
    btc: pd.Series = sub_data['btc']
    df = pd.DataFrame({
        'x': pd.Series(['btc' for _ in range(len(btc))]),
        'y': btc
    })
    single_boxplot(df, 'x', 'y', output_path)


def get_output_files(output_directory: str, basename: str) -> Dict[GraphType, str]:
    return {
        GraphType.TRANSACTION_COUNTS: "{}/{}".format(output_directory,
                                                     "{}-transactions-counts-boxplot.html".format(basename)),
        GraphType.TRANSACTION_BTC: "{}/{}".format(output_directory,
                                                  "{}-transactions-btc-boxplot.html".format(basename))
    }

def run():
    parser = argparse.ArgumentParser(description='Agora stat builder')
    parser.add_argument('--verbose',
                        dest='verbose',
                        action='store_true',
                        default=False,
                        help='activate the verbose mode')
    parser.add_argument('input_path',
                        action='store',
                        nargs=1,
                        type=str,
                        help='path to the input directory')
    parser.add_argument('output_path',
                        action='store',
                        nargs=1,
                        type=str,
                        help='path to the output directory')

    args = parser.parse_args()
    input_path: str = os.path.abspath(args.input_path[0])
    output_path: str = os.path.abspath(args.output_path[0])
    verbose: bool = args.verbose

    if verbose:
        print('input:  {}'.format(input_path))
        print('output: {}'.format(output_path))

    for csv_input in INPUTS:

        # Load CSV file.
        csv_path = "{}/{}".format(input_path, csv_input)
        if verbose:
            print('{}> Loading "{}"'.format(csv_input, csv_path))
        df: pd.DataFrame = load_csv(csv_path)

        outputs = get_output_files(output_path, os.path.basename(csv_input))

        draw_transactions_counts_repartition(df, outputs[GraphType.TRANSACTION_COUNTS])
        draw_transactions_values_repartition(df, outputs[GraphType.TRANSACTION_BTC])


run()
