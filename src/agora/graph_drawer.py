"""
This file implements all the functions used to generate graphs.
"""

import pandas as pd
from .stat import get_count_per_column_value, get_average_per_column_value, get_max_per_column_value
from .graph import hbar, single_boxplot


def draw_transactions_counts_repartition(data: pd.DataFrame,
                                         ref_name: str,
                                         output_path: str,
                                         title: str) -> pd.DataFrame:
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


def draw_transactions_average_amounts_repartition(data: pd.DataFrame,
                                                  ref_name: str,
                                                  output_path: str,
                                                  title: str) -> pd.DataFrame:
    """
    Generate a boxplot graph that represents the repartition of transactions, considering the average transaction
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


def draw_transactions_max_amounts_repartition(data: pd.DataFrame,
                                              ref_name: str,
                                              output_path: str,
                                              title: str) -> pd.DataFrame:
    """
    Generate a boxplot graph that represents the repartition of transactions, considering the maximum transaction
    amount in BTC per "reference". The "reference" is a column name specified by the parameter "ref_name". Typically,
    the "reference" can be: "vendor_name" or "ship_from".

    :param data: the data frame.
    :param ref_name: the name of the column to use as reference.
    :param output_path: path to the file used to store the representation.
    :param title: the title of the graph.
    :return: a data frame that contains 2 columns:
         - the first column contains the "reference" names (and its name is given by the parameter "ref_name").
         - the second column contains the maximum transaction amount per "reference" (which name is given
           within the first column), in BTC. The name of this column is "btc".
    """
    sub_data = get_max_per_column_value(data, ref_name, 'btc')
    btc: pd.Series = sub_data['btc']
    df = pd.DataFrame({
        'x': pd.Series(['btc' for _ in range(len(btc))]),
        'y': btc
    })
    single_boxplot(df, 'x', 'y', output_path, title)
    return sub_data


def draw_transactions_count_greater_than(data: pd.DataFrame,
                                         ref_name: str,
                                         ceiling: int,
                                         output_path: str,
                                         title: str) -> pd.DataFrame:
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
    :return: a data frame that contains 2 columns:
        - the first column contains the "reference" names (and its name is given by the parameter "ref_name").
        - the second column contains the number of transaction "reference" (which name is given
          within the first column). The name of this column is "count".
    """
    sub_data = data[data["count"] > ceiling]
    sub_data = sub_data.sort_values(by="count", axis=0, inplace=False)
    hbar(sub_data, "count", ref_name, "Number of transactions", output_path, title)
    return sub_data


def draw_transactions_average_amounts_greater_than(data: pd.DataFrame,
                                                   ref_name: str,
                                                   ceiling: float,
                                                   output_path: str,
                                                   title: str) -> pd.DataFrame:
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
    :return: a data frame that contains 2 columns:
        - the first column contains the "reference" names (and its name is given by the parameter "ref_name").
        - the second column contains the average transaction amount per "reference" (which name is given
          within the first column), in BTC. The name of this column is "btc".
    """
    sub_data = data[data["btc"] > ceiling]
    sub_data = sub_data.sort_values(by="btc", axis=0, inplace=False)
    hbar(sub_data, "btc", ref_name, "Average amount per transactions", output_path, title)
    return sub_data


def draw_transactions_max_amounts_greater_than(data: pd.DataFrame,
                                               ref_name: str,
                                               ceiling: float,
                                               output_path: str,
                                               title: str) -> pd.DataFrame:
    """
    Generate a horizontal BAR diagram that represents the maximum transaction amount (in BTC) per vendor.

    Please note that vendor whose average transaction amount is lower than a given value are ignored.

    IMPORTANT: the JS "autoscale" does not work well! If you don't see a vendor, try to zoom!

    :param data: the input data. This is a data frame that contains 2 columns:
                 - the first column contains the "reference" names (and its name is given by the parameter "ref_name").
                 - the second column is the maximum transaction amount for the vendor, in BTC
                   (and its columns is "btc").
    :param ref_name: the name of the column to use as reference.
    :param ceiling: the average transaction amount above which the data is printed (on the generated graph).
    :param output_path: the path to the file used to store the graph.
    :param title: the title of the graph.
    :return: a data frame that contains 2 columns:
        - the first column contains the "reference" names (and its name is given by the parameter "ref_name").
        - the second column contains the maximum transaction per "reference" (which name is given within the first
          column), in BTC. The name of this column is "btc".
    """
    sub_data = data[data["btc"] > ceiling]
    sub_data = sub_data.sort_values(by="btc", axis=0, inplace=False)
    hbar(sub_data, "btc", ref_name, "Maximum amount per transactions", output_path, title)
    return sub_data
