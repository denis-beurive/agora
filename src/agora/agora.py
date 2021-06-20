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
from .stat import get_count_per_column_value, get_average_per_column_value
from .graph import hbar, single_boxplot


class GraphType(Enum):
    BOXPLOT_VENDOR_TRANSACTION_COUNTS = 0
    BOXPLOT_VENDOR_TRANSACTION_AVERAGE_BTC = 1
    HBAR_VENDOR_TRANSACTION_COUNTS = 2
    HBAR_VENDOR_TRANSACTION_AVERAGE_BTC = 3
    BOXPLOT_SHIP_FROM_TRANSACTION_COUNTS = 4
    BOXPLOT_SHIP_FROM_TRANSACTION_AVERAGE_BTC = 5
    HBAR_SHIP_FROM_TRANSACTION_COUNTS = 6
    HBAR_SHIP_FROM_TRANSACTION_AVERAGE_BTC = 7


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
    '14-july2015.csv',
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

    def regex_filter(vendor_name: str):
        """
        This function is used to avoid the selection of non-significant vendor names.

        :param vendor_name: a vendor name.
        :return: if the given name is significant, then the function returns the value True.
                 Otherwise, it returns the value False.
        """
        filter_pattern: Pattern = re.compile('^\\s*\\n')
        if vendor_name:
            m: Match = re.search(filter_pattern, vendor_name)
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


def draw_transactions_counts_repartition(data: pd.DataFrame, ref_name: str, output_path: str, title: str) -> pd.DataFrame:
    """
    Generate a boxplot graph that represents the repartition of transactions, considering the total number of
    transactions per "reference". The "reference" is a column name specified by the parameter "ref_name". Typically,
    the "reference" can be: "vendor_name" or "ship_from".

    :param data: the data frame.
    :param ref_name: the name of the column to use as reference.
    :param output_path: path to the file used to store the representation.
    :param title: the title of the graph.
    :return: a data frame tha contains 2 columns:
             - the first column contains the "reference" names (and its name is given by the parameter "ref_name").
             - the second column contains the total number of transactions per "reference". The name of this column
               is "count".
    """
    sub_data = get_count_per_column_value(data, ref_name)
    counts: pd.Series = sub_data['count']
    df = pd.DataFrame({
        'x': pd.Series(['transactions' for _ in range(len(counts))]),
        'y': counts
    })
    single_boxplot(df, 'x', 'y', output_path, title)
    return sub_data


def draw_transactions_average_amounts_repartition(data: pd.DataFrame, ref_name: str, output_path: str, title: str) -> pd.DataFrame:
    """
    Generate a boxplot graph that represents the repartition of transactions, considering the total number of
    transactions per "reference".

    Generate a boxplot graph that represents that repartition of transactions, considering the average transaction
    amount in BTC per "reference". The "reference" is a column name specified by the parameter "ref_name". Typically,
    the "reference" can be: "vendor_name" or "ship_from".

    :param data: the data frame.
    :param ref_name: the name of the column to use as reference.
    :param output_path: path to the file used to store the representation.
    :param title: the title of the graph.
    :return: a data frame tha contains 2 columns:
         - the first column contains the "reference" names (and its name is given by the parameter "ref_name").
         - the second column contains the average transaction amount per "reference" (which name is given
           within the first column), in BTC. The name of this column is "btc".
    """
    sub_data = get_average_per_column_value(data, ref_name, 'btc')
    btc: pd.Series = sub_data['btc']
    df = pd.DataFrame({
        'x': pd.Series(['btc' for _ in range(len(btc))]),
        'y': btc
    })
    single_boxplot(df, 'x', 'y', output_path, title)
    return sub_data


def draw_transactions_count_greater_than(data: pd.DataFrame, ref_name: str, ceiling: int, output_path: str, title: str) -> None:
    """
    Generate a horizontal BAR diagram that represents the total number of transactions per "reference".

    Please note that vendor whose total number of transactions is lower than a given value are ignored.

    :param data: the input data. This is a data frame that contains 2 columns:
                 - the first column contains the "reference" names (and its name is given by the parameter "ref_name").
                 - the second column contains the total number of transactions per "reference". The name of this column
                   is "count".
    :param ref_name: the name of the column to use as reference.
    :param ceiling: the total number of transactions above which the data is printed (on the generated graph).
    :param output_path: the path to the file used to store the graph.
    :param title: the title of the graph.
    """
    sub_data = data[data["count"] > ceiling]
    sub_data.sort_values(by="count", axis=0, inplace=True)
    hbar(sub_data, "count", ref_name, "Number of transactions", output_path, title)


def draw_transactions_average_amount_greater_than(data: pd.DataFrame,
                                                  ref_name: str,
                                                  ceiling: float,
                                                  output_path: str,
                                                  title: str) -> None:
    """
    Generate a horizontal BAR diagram that represents the average transaction amount (in BTC) per vendor.

    Please note that vendor whose average transaction amount is lower than a given value are ignored.

    :param data: the input data. This is a data frame that contains 2 columns:
                 - the first column contains the "reference" names (and its name is given by the parameter "ref_name").
                 - the second column is the average transaction amount for the vendor, in BTC
                   (and its columns is "btc").
    :param ref_name: the name of the column to use as reference.
    :param ceiling: the average transaction amount above which the data is printed (on the generated graph).
    :param output_path: the path to the file used to store the graph.
    :param title: the title of the graph.
    """
    sub_data = data[data["btc"] > ceiling]
    sub_data.sort_values(by="btc", axis=0, inplace=True)
    hbar(sub_data, "btc", ref_name, "Average amount per transactions", output_path, title)


def get_output_files(output_directory: str, prefix: str) -> Dict[GraphType, str]:
    """
    Calculate the paths to the output files.

    :param output_directory: path to the output directory.
    :param prefix: the prefix of the files.
    :return: a dictionary that contains the generated file names, sorted by type of representations.
    """
    return {
        GraphType.BOXPLOT_VENDOR_TRANSACTION_COUNTS: "{}/vendor/transactions-count/{}".format(output_directory, "{}-vendor-transactions-counts-boxplot.html".format(prefix)),
        GraphType.BOXPLOT_VENDOR_TRANSACTION_AVERAGE_BTC: "{}/vendor/transactions-average/{}".format(output_directory, "{}-vendor-transactions-average-btc-boxplot.html".format(prefix)),
        GraphType.HBAR_VENDOR_TRANSACTION_COUNTS: "{}/vendor/transactions-count/{}".format(output_directory, "{}-vendor-transactions-count-hbar.html".format(prefix)),
        GraphType.HBAR_VENDOR_TRANSACTION_AVERAGE_BTC: "{}/vendor/transactions-average/{}".format(output_directory, "{}-vendor-transactions-average-btc-hbar.html".format(prefix)),
        GraphType.BOXPLOT_SHIP_FROM_TRANSACTION_COUNTS: "{}/ship-from/transactions-count/{}".format(output_directory, "{}-ship-from-transactions-counts-boxplot.html".format(prefix)),
        GraphType.BOXPLOT_SHIP_FROM_TRANSACTION_AVERAGE_BTC: "{}/ship-from/transactions-average/{}".format(output_directory, "{}-ship-from-transactions-average-btc-boxplot.html".format(prefix)),
        GraphType.HBAR_SHIP_FROM_TRANSACTION_COUNTS: "{}/ship-from/transactions-count/{}".format(output_directory, "{}-ship-from-transactions-count-hbar.html".format(prefix)),
        GraphType.HBAR_SHIP_FROM_TRANSACTION_AVERAGE_BTC: "{}/ship-from/transactions-average/{}".format(output_directory, "{}-ship-from-transactions-average-btc-hbar.html".format(prefix))
    }


def run():
    """
    Execute the module.
    """
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
        print('input directory:  {}'.format(input_path))
        print('output directory: {}'.format(output_path))

    for csv_input in INPUTS:

        # Load CSV file.
        csv_path = "{}/{}".format(input_path, csv_input)
        if verbose:
            print('{}> Loading "{}"'.format(csv_input, csv_path))
        df: pd.DataFrame = load_csv(csv_path)

        outputs = get_output_files(output_path, os.path.basename(csv_input))

        df_vendor_count = draw_transactions_counts_repartition(df, "vendor_name", outputs[GraphType.BOXPLOT_VENDOR_TRANSACTION_COUNTS], "Number of transactions per vendor")
        df_vendor_average_value = draw_transactions_average_amounts_repartition(df, "vendor_name", outputs[GraphType.BOXPLOT_VENDOR_TRANSACTION_AVERAGE_BTC], "Average transaction in BTC per vendor")
        draw_transactions_count_greater_than(df_vendor_count, "vendor_name", 108, outputs[GraphType.HBAR_VENDOR_TRANSACTION_COUNTS], "Number of transactions per vendor")
        draw_transactions_average_amount_greater_than(df_vendor_average_value, "vendor_name", 1.82, outputs[GraphType.HBAR_VENDOR_TRANSACTION_AVERAGE_BTC], "Average transaction per vendor")

        df_ship_from_count = draw_transactions_counts_repartition(df, "ship_from", outputs[GraphType.BOXPLOT_SHIP_FROM_TRANSACTION_COUNTS], "Number of transactions per shipping locality")
        df_ship_from_average_value = draw_transactions_average_amounts_repartition(df, "ship_from", outputs[GraphType.BOXPLOT_SHIP_FROM_TRANSACTION_AVERAGE_BTC], "Average transaction in BTC per shipping locality")
        draw_transactions_count_greater_than(df_ship_from_count, "ship_from", 729, outputs[GraphType.HBAR_SHIP_FROM_TRANSACTION_COUNTS], "Number of transactions per shipping locality")
        draw_transactions_average_amount_greater_than(df_ship_from_average_value, "ship_from", 2.982, outputs[GraphType.HBAR_SHIP_FROM_TRANSACTION_AVERAGE_BTC], "Average transaction in BTC per shipping locality")


run()
