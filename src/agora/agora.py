"""
    Usage (from the project root folder):

        python -m agora.agora --verbose ./data ./output

    For test (load only 200 rows per CSV file):

        python -m agora.agora --verbose --test ./data ./output

    Skip the generation of monthly graphs:

        python -m agora.agora --verbose --skip-monthly ./data ./output

    Test and skip monthly graphs:

        python -m agora.agora --verbose --test --skip-monthly ./data ./output

    Note: make sure to initialise the Python environment first! (read the file README.md)

        pipenv shell
        pipenv install --dev
"""

from typing import Pattern, Match, Dict, OrderedDict, Optional, List
import argparse
import collections
from datetime import datetime
import os
import re
import pandas as pd
from numpy import float64
from .graph_type import GraphType
from .md_type import MdType
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
    draw_transactions_total_counts, \
    draw_whole_period_transaction_amounts_per_vendor, \
    draw_whole_period_transactions_counts_per_vendor
from .markdown_dumper import data_top_btc_dumper, data_total_dumper
from .fs_tools import create_directory
import seaborn as sns
from .stat import calculate_boxplot_data, BoxPlotData


# Set options for Pandas.
pd.set_option("display.max_rows", None, "display.max_columns", None)

# Apply Seaborn default theme.
sns.set_theme()

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


USE_MINIMAL_SET = True
"""
Tell whether to load only the minimal set of data from the CSV files. The value True means that we want
to load only the minimal set of data. This will greatly accelerate the entire process.
"""
TOP_COUNT = 30
TEST_MODE_COUNT = 1000


def csv_loader(path: str, load_minimal: bool = USE_MINIMAL_SET, max_rows: Optional[int] = None) -> pd.DataFrame:
    """
    Load data from CSV file.

    This function skips the rows that contain empty vendor names.

    :param path: path to the CSV file to load.
    :param load_minimal: tell whether to load only the minimum set of data or not.
                         If the parameter value is True, then only the minimum set of data is loaded.
    :param max_rows: maximum number of rows to load.
                     The value None means "no maximum value".
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

    if load_minimal:
        data: pd.DataFrame = pd.read_csv(filepath_or_buffer=path,
                                         sep=',',
                                         quotechar='"',
                                         dialect='excel',
                                         usecols=['btc', 'ship_from', 'vendor_name'],
                                         nrows=max_rows)
    else:
        # We keep this section of the code just in case we need more data later.
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
                                         },
                                         nrows=max_rows)
    return data.loc[data['vendor_name'].apply(regex_filter)]


def process_month(csv_input: str,
                  output_path: str,
                  df: pd.DataFrame,
                  md_reports_paths: Dict[MdType, str],
                  debug: bool = False,
                  verbose: bool = False) -> None:
    """
    Create graphs for a given month.

    :param csv_input: name of the CSV file that contain the data for the month. Example: 01-june2014.csv
    :param output_path: path to the base of the output directory, used to store the generated documents.
    :param df: data frame that contains the data for the month.
    :param md_reports_paths: names of the Markdown formatted generated documents.
    :param debug: debug flag.
    :param verbose: verbose flag.
    """
    left_shift = 0.3
    if debug:
        print("*" * 10 + csv_input + "*" * 10)
        print(df[['vendor_name', 'usd', 'btc', 'rate']])

    outputs = get_output_graph_files(output_path, csv_input[:-4])
    date = csv_input

    # 1. Transactions per vendor: boxplot / hbar / table.
    #    - Number of transactions per vendor.
    #    - Average transaction per vendor.
    #    - Maximum transaction per vendor.
    #    - Total amount of transaction per vendor.

    # boxplot
    df_vendor_count = draw_transactions_counts_repartition(df, "vendor_name", outputs[GraphType.BOXPLOT_VENDOR_TRANSACTION_COUNTS], date, left_shift)
    df_vendor_average_value = draw_transactions_average_amounts_repartition(df, "vendor_name", outputs[GraphType.BOXPLOT_VENDOR_TRANSACTION_AVERAGE_BTC], date, left_shift)
    df_vendor_max_value = draw_transactions_max_amounts_repartition(df, "vendor_name", outputs[GraphType.BOXPLOT_VENDOR_TRANSACTION_MAX_BTC], date, left_shift)
    df_vendor_sum_value = draw_transactions_sum_amounts_repartition(df, "vendor_name", outputs[GraphType.BOXPLOT_VENDOR_TRANSACTION_SUM_BTC], date, left_shift)

    # hbar
    draw_transactions_count_greater_than(df_vendor_count, "vendor_name", TOP_COUNT, outputs[GraphType.HBAR_VENDOR_TRANSACTION_COUNTS], date, left_shift)
    draw_transactions_average_amounts_greater_than(df_vendor_average_value, "vendor_name", TOP_COUNT, outputs[GraphType.HBAR_VENDOR_TRANSACTION_AVERAGE_BTC], date, left_shift)
    draw_transactions_max_amounts_greater_than(df_vendor_max_value, "vendor_name", TOP_COUNT, outputs[GraphType.HBAR_VENDOR_TRANSACTION_MAX_BTC], date, left_shift)
    draw_transactions_sum_amounts_greater_than(df_vendor_sum_value, "vendor_name", TOP_COUNT, outputs[GraphType.HBAR_VENDOR_TRANSACTION_SUM_BTC], date, left_shift)

    md = data_top_btc_dumper(df_vendor_count,
                             df_vendor_average_value,
                             df_vendor_max_value,
                             df_vendor_sum_value,
                             'vendor_name')
    if verbose:
        print('Create file {}'.format(md_reports_paths[MdType.MD_VENDOR_TRANSACTION]))
    with open(md_reports_paths[MdType.MD_VENDOR_TRANSACTION], "a") as fd:
        fd.write("# {}\n\n".format(csv_input[3:-4]))
        fd.write("{}\n\n".format(md))

    # 2. Transactions per shipping locality: boxplot / hbar / table.
    #    - Number of transactions per shipping locality.
    #    - Average transaction per shipping locality.
    #    - Maximum transaction per shipping locality.
    #    - Total amount of transaction per shipping locality.

    # boxplot
    df_ship_from_count = draw_transactions_counts_repartition(df, "ship_from", outputs[GraphType.BOXPLOT_SHIP_FROM_TRANSACTION_COUNTS], date, left_shift)
    df_ship_from_average_value = draw_transactions_average_amounts_repartition(df, "ship_from", outputs[ GraphType.BOXPLOT_SHIP_FROM_TRANSACTION_AVERAGE_BTC], date, left_shift)
    df_ship_from_max_value = draw_transactions_max_amounts_repartition(df, "ship_from", outputs[GraphType.BOXPLOT_SHIP_FROM_TRANSACTION_MAX_BTC], date, left_shift)
    df_ship_from_sum_value = draw_transactions_sum_amounts_repartition(df, "ship_from", outputs[GraphType.BOXPLOT_SHIP_FROM_TRANSACTION_SUM_BTC], date, left_shift)

    # hbar
    draw_transactions_count_greater_than(df_ship_from_count, "ship_from", TOP_COUNT, outputs[GraphType.HBAR_SHIP_FROM_TRANSACTION_COUNTS], date, left_shift)
    draw_transactions_average_amounts_greater_than(df_ship_from_average_value, "ship_from", TOP_COUNT, outputs[GraphType.HBAR_SHIP_FROM_TRANSACTION_AVERAGE_BTC], date, left_shift)
    draw_transactions_max_amounts_greater_than(df_ship_from_max_value, "ship_from", TOP_COUNT, outputs[GraphType.HBAR_SHIP_FROM_TRANSACTION_MAX_BTC], date, left_shift)
    draw_transactions_sum_amounts_greater_than(df_ship_from_sum_value, "ship_from", TOP_COUNT, outputs[GraphType.HBAR_SHIP_FROM_TRANSACTION_SUM_BTC], date, left_shift)

    md = data_top_btc_dumper(df_ship_from_count,
                             df_ship_from_average_value,
                             df_ship_from_max_value,
                             df_ship_from_sum_value,
                             'ship_from')
    if verbose:
        print('Create file {}'.format(md_reports_paths[MdType.MD_SHIP_FROM_TRANSACTION]))
    with open(md_reports_paths[MdType.MD_SHIP_FROM_TRANSACTION], "a") as fd:
        fd.write("# {}\n\n".format(csv_input[3:-4]))
        fd.write("{}\n\n".format(md))


def get_output_graph_files(output_directory: str, prefix: str) -> Dict[GraphType, str]:
    """
    Calculate the paths to the output graph files, and create the required directory of needed.

    :param output_directory: path to the output directory.
    :param prefix: the prefix of the files.
    :return: a dictionary that contains the generated file names, sorted by type of representations.
    """
    paths: Dict[GraphType, str] = {
        GraphType.BOXPLOT_VENDOR_TRANSACTION_COUNTS: "{}/vendor/transactions-count/{}".format(output_directory, "{}/transactions-counts-boxplot".format(prefix)),
        GraphType.BOXPLOT_VENDOR_TRANSACTION_AVERAGE_BTC: "{}/vendor/transactions-average/{}".format(output_directory, "{}/transactions-average-btc-boxplot".format(prefix)),
        GraphType.BOXPLOT_VENDOR_TRANSACTION_MAX_BTC: "{}/vendor/transactions-max/{}".format(output_directory, "{}/transactions-max-btc-boxplot".format(prefix)),
        GraphType.BOXPLOT_VENDOR_TRANSACTION_SUM_BTC: "{}/vendor/transactions-sum/{}".format(output_directory, "{}/transactions-sum-btc-boxplot".format(prefix)),

        GraphType.HBAR_VENDOR_TRANSACTION_COUNTS: "{}/vendor/transactions-count/{}".format(output_directory, "{}/transactions-count-hbar".format(prefix)),
        GraphType.HBAR_VENDOR_TRANSACTION_AVERAGE_BTC: "{}/vendor/transactions-average/{}".format(output_directory, "{}/transactions-average-btc-hbar".format(prefix)),
        GraphType.HBAR_VENDOR_TRANSACTION_MAX_BTC: "{}/vendor/transactions-max/{}".format(output_directory, "{}/transactions-max-btc-hbar".format(prefix)),
        GraphType.HBAR_VENDOR_TRANSACTION_SUM_BTC: "{}/vendor/transactions-sum/{}".format(output_directory, "{}/transactions-sum-btc-hbar".format(prefix)),

        GraphType.BOXPLOT_SHIP_FROM_TRANSACTION_COUNTS: "{}/ship-from/transactions-count/{}".format(output_directory, "{}/transactions-counts-boxplot".format(prefix)),
        GraphType.BOXPLOT_SHIP_FROM_TRANSACTION_AVERAGE_BTC: "{}/ship-from/transactions-average/{}".format(output_directory, "{}/transactions-average-btc-boxplot".format(prefix)),
        GraphType.BOXPLOT_SHIP_FROM_TRANSACTION_MAX_BTC: "{}/ship-from/transactions-max/{}".format(output_directory, "{}/transactions-max-btc-boxplot".format(prefix)),
        GraphType.BOXPLOT_SHIP_FROM_TRANSACTION_SUM_BTC: "{}/ship-from/transactions-sum/{}".format(output_directory, "{}/transactions-sum-btc-boxplot".format(prefix)),

        GraphType.HBAR_SHIP_FROM_TRANSACTION_COUNTS: "{}/ship-from/transactions-count/{}".format(output_directory, "{}/transactions-count-hbar".format(prefix)),
        GraphType.HBAR_SHIP_FROM_TRANSACTION_AVERAGE_BTC: "{}/ship-from/transactions-average/{}".format(output_directory, "{}/transactions-average-btc-hbar".format(prefix)),
        GraphType.HBAR_SHIP_FROM_TRANSACTION_MAX_BTC: "{}/ship-from/transactions-max/{}".format(output_directory, "{}/transactions-max-btc-hbar".format(prefix)),
        GraphType.HBAR_SHIP_FROM_TRANSACTION_SUM_BTC: "{}/ship-from/transactions-sum/{}".format(output_directory, "{}/transactions-sum-btc-hbar".format(prefix)),
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


def get_month_max_upper_fence(data: pd.DataFrame, column: str) -> float:
    """
    Given a data frame that contains "data per month", this function returns the maximum value for the upper fence
    calculated from the data associated with each month.

    :param data: data frame that contains at least 2 columns:
                 - a column named "month"
                 - another column which name is given by the parameter "column".
    :param column: the name of the column upon which the upper fence values are calculated.
    :return: the maximum upper fence value.
    """
    months = data['month'].unique()
    upper_fences: List[float] = []
    for month in months:
        df: pd.DataFrame = data.query('month == "{}"'.format(month))
        bp = calculate_boxplot_data(df, column)
        upper_fences.append(bp.upper_fence)
    return max(upper_fences)


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
    parser.add_argument('--test',
                        dest='test',
                        action='store_true',
                        default=False,
                        help='activate the test mode')
    parser.add_argument('--skip-monthly',
                        dest='skip_monthly',
                        action='store_true',
                        default=False,
                        help='skip the generation of monthly graphs')
    parser.add_argument('--skip-if_exists',
                        dest='skip_if_exists',
                        action='store_true',
                        default=False,
                        help='skip the generation a graph if ot already exists')
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
    test_mode: bool = args.test
    skip_monthly: bool = args.skip_monthly
    skip_if_exists: bool = args.skip_if_exists

    if verbose:
        print('input directory:       {}'.format(input_path))
        print('output directory:      {}'.format(output_path))
        print('test mode activated:   {}'.format("yes" if test_mode else "no"))
        print('skip monthly graphs:   {}'.format("yes" if skip_monthly else "no"))
        print('skip if exists:        {}'.format("yes" if skip_if_exists else "no"))

    md_reports_paths = get_output_md_files(output_path)
    dataframes: OrderedDict[str, pd.DataFrame] = collections.OrderedDict()
    """
       This data frame contains all data loaded from the CSV files. The structure of this data frame is:
       { month1 => dataframe1,
         month2 => dataframe2,
         ... }
         
       With "month<N>": "june2014", "july2014"... 
       The structure of "dataframe<N>" depends on the CSV loading policies. With minimal loading, we have 3 columns:
           - 'btc'
           - 'ship_from'
           - 'vendor_name'       
    """

    # --------------------------------------------------------------------------
    # Generated documents for all months, individually.
    # --------------------------------------------------------------------------

    if verbose:
        print("-" * 50)
        message = "Load CSV files" if skip_monthly else "Generate monthly graphs"
        print(message)
        print("-" * 50)

    for csv_input in INPUTS:

        # Load CSV file.
        csv_path = "{}/{}".format(input_path, csv_input)
        maximum = TEST_MODE_COUNT if test_mode else None
        if verbose:
            print('Loading "{}" (maximum row: {})'.format(csv_path, "not set" if maximum is None else maximum))
        df: pd.DataFrame = csv_loader(csv_path, USE_MINIMAL_SET, maximum)

        # Drop columns in an attempt to reduce the quantity of memory used.
        if not USE_MINIMAL_SET:
            df.drop(columns=["hash", "name", "description"])

        # Store the dataframe for later use.
        dataframes[csv_input[3:-4]] = df

        if not skip_monthly:
            process_month(csv_input, output_path, df, md_reports_paths, debug, verbose)

    # --------------------------------------------------------------------------
    # Generated documents for the whole series of months.
    # --------------------------------------------------------------------------

    if verbose:
        print("-" * 50)
        print("Generate documents for the entire time scale")
        print("-" * 50)

    # VBAR that shows transactions variations:
    # - total amounts.
    # - total counts.
    gd_path = "{}/transaction/{}".format(output_path, "total-btc-vbar")
    create_directory(gd_path)
    total_amounts = draw_transactions_total_amounts(dataframes,
                                                    'btc',
                                                    gd_path,
                                                    "Total amount of transactions in BTC",
                                                    0.2)

    gd_path = "{}/transaction/{}".format(output_path, "total-count-vbar")
    create_directory(gd_path)
    total_counts = draw_transactions_total_counts(dataframes,
                                                  gd_path,
                                                  "Total number of transactions",
                                                  0.2)

    # Markdown table that shows transactions variations:
    # - total amounts.
    # - total counts.
    gd_path = "{}/transaction/{}".format(output_path, "total-transactions.md")
    create_directory(gd_path)
    with open(gd_path, "w") as fd:
        md = data_total_dumper(total_amounts)
        fd.write("# Total transaction amounts in BTC per month\n\n")
        fd.write("{}\n\n".format(md))
        md = data_total_dumper(total_counts)
        fd.write("# Total number of transactions per month\n\n")
        fd.write("{}\n\n".format(md))

    # List of boxplot: repartition of transaction amounts per vendor.
    gd_path = "{}/transaction/{}".format(output_path, "boxplot-amount-per-vendor-year")
    if skip_if_exists and os.path.exists(gd_path):
        pass
    else:
        create_directory(gd_path)
        d = draw_whole_period_transaction_amounts_per_vendor(dataframes,
                                                             'btc',
                                                             gd_path,
                                                             0.2)

    # List of boxplot: repartition of transaction counts per vendor.
    gd_path = "{}/transaction/{}".format(output_path, "boxplot-count-per-vendor-year")
    if skip_if_exists and os.path.exists(gd_path):
        pass
    else:
        create_directory(gd_path)
        d = draw_whole_period_transactions_counts_per_vendor(dataframes,
                                                             gd_path,
                                                             0.2)
        maximum = get_month_max_upper_fence(d, 'count')

        gd_path = "{}/transaction/{}".format(output_path, "boxplot-top-count-per-vendor-year")
        create_directory(gd_path)
        draw_whole_period_transactions_counts_per_vendor(dataframes,
                                                         gd_path,
                                                         0.2,
                                                         -700,
                                                         1500)


run()
