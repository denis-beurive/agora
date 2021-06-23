"""
    Usage (from the project root folder):

        python -m agora.agora --verbose ./data ./output

    Note: make sure to initialise the Python environment first! (read the file README.md)

        pipenv install --dev
"""

from typing import Any, Pattern, Match, Dict, OrderedDict
import argparse
import collections
from datetime import datetime
import os
import re
import pandas as pd
from numpy import float64
from .graph_type import GraphType
from .md_type import MdType
from .stat import BoxPlotData, calculate_boxplot_data
from .graph_drawer import \
    draw_transactions_counts_repartition, \
    draw_transactions_average_amounts_repartition, \
    draw_transactions_max_amounts_repartition, \
    draw_transactions_sum_amounts_repartition, \
    draw_transactions_count_greater_than, \
    draw_transactions_average_amounts_greater_than, \
    draw_transactions_max_amounts_greater_than, \
    draw_transactions_sum_amounts_greater_than, \
    draw_transactions_total_amounts, \
    draw_transactions_total_counts
from .markdown_dumper import data_top_btc_dumper, data_total_dumper
from .fs_tools import create_directory


# Set options for Pandas.
pd.set_option("display.max_rows", None, "display.max_columns", None)

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


def csv_loader(path: str) -> pd.DataFrame:
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
                                         'btc': float64,
                                         'usd': float64,
                                         'rate': float64,
                                         'ship_from': str,
                                         'vendor_name': str,
                                         'name': str
                                     })
    return data.loc[data['vendor_name'].apply(regex_filter)]


def get_output_graph_files(output_directory: str, prefix: str) -> Dict[GraphType, str]:
    """
    Calculate the paths to the output graph files, and create the required directory of needed.

    :param output_directory: path to the output directory.
    :param prefix: the prefix of the files.
    :return: a dictionary that contains the generated file names, sorted by type of representations.
    """
    paths: Dict[GraphType, str] = {
        GraphType.BOXPLOT_VENDOR_TRANSACTION_COUNTS: "{}/vendor/transactions-count/{}".format(output_directory, "{}-vendor-transactions-counts-boxplot.html".format(prefix)),
        GraphType.BOXPLOT_VENDOR_TRANSACTION_AVERAGE_BTC: "{}/vendor/transactions-average/{}".format(output_directory, "{}-vendor-transactions-average-btc-boxplot.html".format(prefix)),
        GraphType.BOXPLOT_VENDOR_TRANSACTION_MAX_BTC: "{}/vendor/transactions-max/{}".format(output_directory, "{}-vendor-transactions-max-btc-boxplot.html".format(prefix)),
        GraphType.BOXPLOT_VENDOR_TRANSACTION_SUM_BTC: "{}/vendor/transactions-sum/{}".format(output_directory, "{}-vendor-transactions-sum-btc-boxplot.html".format(prefix)),

        GraphType.HBAR_VENDOR_TRANSACTION_COUNTS: "{}/vendor/transactions-count/{}".format(output_directory, "{}-vendor-transactions-count-hbar.html".format(prefix)),
        GraphType.HBAR_VENDOR_TRANSACTION_AVERAGE_BTC: "{}/vendor/transactions-average/{}".format(output_directory, "{}-vendor-transactions-average-btc-hbar.html".format(prefix)),
        GraphType.HBAR_VENDOR_TRANSACTION_MAX_BTC: "{}/vendor/transactions-max/{}".format(output_directory, "{}-vendor-transactions-max-btc-hbar.html".format(prefix)),
        GraphType.HBAR_VENDOR_TRANSACTION_SUM_BTC: "{}/vendor/transactions-sum/{}".format(output_directory, "{}-vendor-transactions-sum-btc-hbar.html".format(prefix)),

        GraphType.BOXPLOT_SHIP_FROM_TRANSACTION_COUNTS: "{}/ship-from/transactions-count/{}".format(output_directory, "{}-ship-from-transactions-counts-boxplot.html".format(prefix)),
        GraphType.BOXPLOT_SHIP_FROM_TRANSACTION_AVERAGE_BTC: "{}/ship-from/transactions-average/{}".format(output_directory, "{}-ship-from-transactions-average-btc-boxplot.html".format(prefix)),
        GraphType.BOXPLOT_SHIP_FROM_TRANSACTION_MAX_BTC: "{}/ship-from/transactions-max/{}".format(output_directory, "{}-ship-from-transactions-max-btc-boxplot.html".format(prefix)),
        GraphType.BOXPLOT_SHIP_FROM_TRANSACTION_SUM_BTC: "{}/ship-from/transactions-sum/{}".format(output_directory, "{}-ship-from-transactions-sum-btc-boxplot.html".format(prefix)),

        GraphType.HBAR_SHIP_FROM_TRANSACTION_COUNTS: "{}/ship-from/transactions-count/{}".format(output_directory, "{}-ship-from-transactions-count-hbar.html".format(prefix)),
        GraphType.HBAR_SHIP_FROM_TRANSACTION_AVERAGE_BTC: "{}/ship-from/transactions-average/{}".format(output_directory, "{}-ship-from-transactions-average-btc-hbar.html".format(prefix)),
        GraphType.HBAR_SHIP_FROM_TRANSACTION_MAX_BTC: "{}/ship-from/transactions-max/{}".format(output_directory, "{}-ship-from-transactions-max-btc-hbar.html".format(prefix)),
        GraphType.HBAR_SHIP_FROM_TRANSACTION_SUM_BTC: "{}/ship-from/transactions-sum/{}".format(output_directory, "{}-ship-from-transactions-sum-btc-hbar.html".format(prefix)),
    }

    for path in paths.values():
        create_directory(path)

    return paths


def get_output_md_files(output_directory: str) -> Dict[MdType, str]:
    """
    Calculate the paths to the output markdown files.

    :param output_directory: path to the output directory.
    :return: a dictionary that contains the generated file names, sorted by type of representations.
    """
    paths: Dict[MdType, str] = {
        MdType.MD_VENDOR_TRANSACTION: "{}/vendor/transactions.md".format(output_directory),
        MdType.MD_SHIP_FROM_TRANSACTION: "{}/ship-from/transactions.md".format(output_directory)
    }

    for path in paths.values():
        create_directory(path)

    return paths


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
    parser.add_argument('--debug',
                        dest='debug',
                        action='store_true',
                        default=False,
                        help='activate the debug mode')
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
    debug: bool = args.debug

    if verbose:
        print('input directory:  {}'.format(input_path))
        print('output directory: {}'.format(output_path))

    md_reports_paths = get_output_md_files(output_path)
    for path in md_reports_paths.values():
        if os.path.exists(path):
            os.remove(path)

    dataframes: OrderedDict[str, pd.DataFrame] = collections.OrderedDict()

    for csv_input in INPUTS:

        # Load CSV file.
        csv_path = "{}/{}".format(input_path, csv_input)
        if verbose:
            print('{}> Loading "{}"'.format(csv_input, csv_path))
        df: pd.DataFrame = csv_loader(csv_path)

        # Drop columns in an attempt to reduce the quantity of memory used.
        df.drop(columns=["hash", "name","description"])

        # Store the dataframe for later use.
        dataframes[csv_input[3:-4]] = df

        if debug:
            print("*"*10 + csv_input + "*"*10)
            print(df[['vendor_name', 'usd', 'btc', 'rate']])

        outputs = get_output_graph_files(output_path, csv_input[:-4])
        if verbose:
            for path in outputs.values():
                print("- {}".format(path))

        # 1. Transactions per vendor: boxplot / hbar / table.
        #    - Number of transactions per vendor.
        #    - Average transaction per vendor.
        #    - Maximum transaction per vendor.
        #    - Total amount of transaction per vendor.

        # boxplot
        df_vendor_count = draw_transactions_counts_repartition(df, "vendor_name", outputs[GraphType.BOXPLOT_VENDOR_TRANSACTION_COUNTS], "{}: Number of transactions per vendor".format(csv_input))
        df_vendor_average_value = draw_transactions_average_amounts_repartition(df, "vendor_name", outputs[GraphType.BOXPLOT_VENDOR_TRANSACTION_AVERAGE_BTC], "{}: Average transaction in BTC per vendor".format(csv_input))
        df_vendor_max_value = draw_transactions_max_amounts_repartition(df, "vendor_name", outputs[GraphType.BOXPLOT_VENDOR_TRANSACTION_MAX_BTC], "{}: Maximum transaction in BTC per vendor".format(csv_input))
        df_vendor_sum_value = draw_transactions_sum_amounts_repartition(df, "vendor_name", outputs[GraphType.BOXPLOT_VENDOR_TRANSACTION_SUM_BTC], "{}: Total amount of transaction in BTC per vendor".format(csv_input))

        # hbar
        bp_data_count: BoxPlotData = calculate_boxplot_data(df, "btc")
        bp_data_average_amounts: BoxPlotData = calculate_boxplot_data(df_vendor_average_value, "btc")
        bp_data_max_amounts: BoxPlotData = calculate_boxplot_data(df_vendor_max_value, "btc")
        bp_data_sum_amounts: BoxPlotData = calculate_boxplot_data(df_vendor_sum_value, "btc")

        draw_transactions_count_greater_than(df_vendor_count, "vendor_name", bp_data_count.upper_fence, outputs[GraphType.HBAR_VENDOR_TRANSACTION_COUNTS], "{}: Number of transactions per vendor".format(csv_input))
        draw_transactions_average_amounts_greater_than(df_vendor_average_value, "vendor_name", bp_data_average_amounts.upper_fence, outputs[GraphType.HBAR_VENDOR_TRANSACTION_AVERAGE_BTC], "{}: Average transaction in BTC per vendor".format(csv_input))
        draw_transactions_max_amounts_greater_than(df_vendor_max_value, "vendor_name", bp_data_max_amounts.upper_fence, outputs[GraphType.HBAR_VENDOR_TRANSACTION_MAX_BTC], "{}: Maximum transaction in BTC per vendor".format(csv_input))
        draw_transactions_sum_amounts_greater_than(df_vendor_sum_value, "vendor_name", bp_data_sum_amounts.upper_fence, outputs[GraphType.HBAR_VENDOR_TRANSACTION_SUM_BTC], "{}: Total amount of transaction in BTC per vendor".format(csv_input))

        md = data_top_btc_dumper(df_vendor_count,
                                 df_vendor_average_value,
                                 df_vendor_max_value,
                                 df_vendor_sum_value,
                                 'vendor_name')
        if verbose:
            print("- {}".format(md_reports_paths[MdType.MD_VENDOR_TRANSACTION]))
        with open(md_reports_paths[MdType.MD_VENDOR_TRANSACTION], "a") as fd:
            fd.write("# {}\n\n".format(csv_input[3:-4]))
            fd.write("{}\n\n".format(md))

        # 2. Transactions per shipping locality: boxplot / hbar / table.
        #    - Number of transactions per shipping locality.
        #    - Average transaction per shipping locality.
        #    - Maximum transaction per shipping locality.
        #    - Total amount of transaction per shipping locality.

        # boxplot
        df_ship_from_count = draw_transactions_counts_repartition(df, "ship_from", outputs[GraphType.BOXPLOT_SHIP_FROM_TRANSACTION_COUNTS], "{}: Number of transactions per shipping locality".format(csv_input))
        df_ship_from_average_value = draw_transactions_average_amounts_repartition(df, "ship_from", outputs[GraphType.BOXPLOT_SHIP_FROM_TRANSACTION_AVERAGE_BTC], "{}: Average transaction in BTC per shipping locality".format(csv_input))
        df_ship_from_max_value = draw_transactions_max_amounts_repartition(df, "ship_from", outputs[GraphType.BOXPLOT_SHIP_FROM_TRANSACTION_MAX_BTC], "{}: Maximum transaction in BTC per shipping locality".format(csv_input))
        df_ship_from_sum_value = draw_transactions_sum_amounts_repartition(df, "ship_from", outputs[GraphType.BOXPLOT_SHIP_FROM_TRANSACTION_SUM_BTC], "{}: Total amount of transaction in BTC per shipping locality".format(csv_input))

        # hbar
        bp_data_count: BoxPlotData = calculate_boxplot_data(df, "btc")
        bp_data_average_amounts: BoxPlotData = calculate_boxplot_data(df_ship_from_average_value, "btc")
        bp_data_max_amounts: BoxPlotData = calculate_boxplot_data(df_ship_from_max_value, "btc")
        bp_data_sum_amounts: BoxPlotData = calculate_boxplot_data(df_ship_from_sum_value, "btc")

        draw_transactions_count_greater_than(df_ship_from_count, "ship_from", bp_data_count.upper_fence, outputs[GraphType.HBAR_SHIP_FROM_TRANSACTION_COUNTS], "{}: Number of transactions per shipping locality".format(csv_input))
        draw_transactions_average_amounts_greater_than(df_ship_from_average_value, "ship_from", bp_data_average_amounts.upper_fence, outputs[GraphType.HBAR_SHIP_FROM_TRANSACTION_AVERAGE_BTC], "{}: Average transaction in BTC per shipping locality".format(csv_input))
        draw_transactions_max_amounts_greater_than(df_ship_from_max_value, "ship_from", bp_data_max_amounts.upper_fence, outputs[GraphType.HBAR_SHIP_FROM_TRANSACTION_MAX_BTC], "{}: Maximum transaction in BTC per shipping locality".format(csv_input))
        draw_transactions_sum_amounts_greater_than(df_ship_from_sum_value, "ship_from", bp_data_sum_amounts.upper_fence, outputs[GraphType.HBAR_SHIP_FROM_TRANSACTION_SUM_BTC], "{}: Total amount of transactions in BTC per shipping locality".format(csv_input))

        md = data_top_btc_dumper(df_ship_from_count,
                                 df_ship_from_average_value,
                                 df_ship_from_max_value,
                                 df_ship_from_sum_value,
                                 'ship_from')
        if verbose:
            print("- {}".format(md_reports_paths[MdType.MD_SHIP_FROM_TRANSACTION]))
        with open(md_reports_paths[MdType.MD_SHIP_FROM_TRANSACTION], "a") as fd:
            fd.write("# {}\n\n".format(csv_input[3:-4]))
            fd.write("{}\n\n".format(md))

    # VBAR that shows transactions variation:
    # - total amounts.
    # - total_counts.
    gd_path = "{}/transaction/{}".format(output_path, "total-btc-vbar.html")
    create_directory(gd_path)
    if verbose:
        print("- {}".format(output_path))
    total_amounts = draw_transactions_total_amounts(dataframes,
                                                    'btc',
                                                    'total amount of transactions in BTC',
                                                    gd_path,
                                                    "Total amount of transactions in BTC")

    gd_path = "{}/transaction/{}".format(output_path, "total-count-vbar.html")
    create_directory(gd_path)
    if verbose:
        print("- {}".format(output_path))
    total_counts = draw_transactions_total_counts(dataframes,
                                                  'total number of transactions',
                                                  gd_path,
                                                  "Total number of transactions")

    # Markdown table that shows transactions variation:
    # - total amounts.
    # - total_counts.
    gd_path = "{}/transaction/{}".format(output_path, "total-transactions.md")

    create_directory(gd_path)
    if verbose:
        print("- {}".format(gd_path))

    with open(gd_path, "w") as fd:
        md = data_total_dumper(total_amounts)
        fd.write("# Total transaction amounts in BTC per month\n\n")
        fd.write("{}\n\n".format(md))
        md = data_total_dumper(total_counts)
        fd.write("# Total number of transaction per month\n\n")
        fd.write("{}\n\n".format(md))


run()
