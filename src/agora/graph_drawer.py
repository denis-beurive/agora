"""
This file implements all the functions used to generate graphs.
"""

import pandas as pd
from typing import OrderedDict
from .stat import get_count_per_column_value, \
    get_average_per_column_value, \
    get_max_per_column_value, \
    get_sum_per_column_value
from .graph import hbar, vbar, single_boxplot, multiple_boxplot_seaborn


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


def draw_transactions_sum_amounts_repartition(data: pd.DataFrame,
                                              ref_name: str,
                                              output_path: str,
                                              title: str) -> pd.DataFrame:
    """
    Generate a boxplot graph that represents the repartition of transactions, considering the sum of all
    transaction amounts in BTC per "reference". The "reference" is a column name specified by the parameter
    "ref_name". Typically, the "reference" can be: "vendor_name" or "ship_from".

    :param data: the data frame.
    :param ref_name: the name of the column to use as reference.
    :param output_path: path to the file used to store the representation.
    :param title: the title of the graph.
    :return: a data frame that contains 2 columns:
         - the first column contains the "reference" names (and its name is given by the parameter "ref_name").
         - the second column contains the sum of all transaction amounts per "reference" (which name is given
           within the first column), in BTC. The name of this column is "btc".
    """
    sub_data = get_sum_per_column_value(data, ref_name, 'btc')
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

    Please note that vendors whose total number of transactions is lower than a given value are ignored.

    IMPORTANT: the JS "autoscale" does not work well! If you don't see a "reference", try to zoom!

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
    Generate a horizontal BAR diagram that represents the average transaction amount (in BTC) per "reference".

    Please note that vendors whose average transaction amount is lower than a given value are ignored.

    IMPORTANT: the JS "autoscale" does not work well! If you don't see a "reference", try to zoom!

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
    Generate a horizontal BAR diagram that represents the maximum transaction amount (in BTC) per "reference".

    Please note that vendors whose average transaction amount is lower than a given value are ignored.

    IMPORTANT: the JS "autoscale" does not work well! If you don't see a "reference", try to zoom!

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


def draw_transactions_sum_amounts_greater_than(data: pd.DataFrame,
                                               ref_name: str,
                                               ceiling: float,
                                               output_path: str,
                                               title: str) -> pd.DataFrame:
    """
    Generate a horizontal BAR diagram that represents the total amount of transaction (in BTC) per "reference".

    Please note that vendors whose total amount of transactions is lower than a given value are ignored.

    IMPORTANT: the JS "autoscale" does not work well! If you don't see a "reference", try to zoom!

    :param data: the input data. This is a data frame that contains 2 columns:
                 - the first column contains the "reference" names (and its name is given by the parameter "ref_name").
                 - the second column is the total amount of transactions for the vendor, in BTC
                   (and its columns is "btc").
    :param ref_name: the name of the column to use as reference.
    :param ceiling: the average transaction amount above which the data is printed (on the generated graph).
    :param output_path: the path to the file used to store the graph.
    :param title: the title of the graph.
    :return: a data frame that contains 2 columns:
        - the first column contains the "reference" names (and its name is given by the parameter "ref_name").
        - the second column contains the total amount of transactions per "reference" (which name is given
          within the first column), in BTC. The name of this column is "btc".
    """
    sub_data = data[data["btc"] > ceiling]
    sub_data = sub_data.sort_values(by="btc", axis=0, inplace=False)
    hbar(sub_data, "btc", ref_name, "Maximum amount per transactions", output_path, title)
    return sub_data


def draw_transactions_total_amounts(transactions: OrderedDict[str, pd.DataFrame],
                                    ref_name: str,
                                    legend: str,
                                    output_path: str,
                                    title: str) -> pd.DataFrame:
    """
    Draw a vertical HBAR graph that represents the variation of the total amount of transaction over time.

    :param transactions: an ordered dictionary which keys are the dates and the values are data frames that
                         contain the data loaded from the CSV file ("01-june2014.csv"...).
    :param ref_name: the name of the column that represents the transaction amount.
                     The value of this parameter should be "btc" or "usd".
    :param legend: the legend.
    :param output_path: the path to the file used to store the graph.
    :param title: the title of the graph.
    :return: a data frame that contains 2 columns:
             - a column named "date".
             - a column named "total".
    """

    df = pd.DataFrame()
    df['date'] = transactions.keys()
    df['total'] = [d[ref_name].sum() for d in transactions.values()]

    # df looks something like:
    #
    #         date      total
    #    0    january   1000
    #    1    february  2000
    #    ...  ...       ...

    vbar(df,
         abscissa="date",
         ordinate="total",
         legend=legend,
         output_path=output_path,
         title=title)
    return df


def draw_transactions_total_counts(transactions: OrderedDict[str, pd.DataFrame],
                                   legend: str,
                                   output_path: str,
                                   title: str) -> pd.DataFrame:
    """
    Draw a vertical HBAR graph that represents the variation of the total number of transaction over time.

    :param transactions: an ordered dictionary which keys are the dates and the values are data frames that
                         contain the data loaded from the CSV file ("01-june2014.csv"...).
    :param legend: the legend.
    :param output_path: the path to the file used to store the graph.
    :param title: the title of the graph.
    :return: a data frame that contains 2 columns:
             - a column named "date".
             - a column named "total".
    """

    df = pd.DataFrame()
    df['date'] = transactions.keys()
    df['total'] = [len(d.index) for d in transactions.values()]

    # df looks something like:
    #
    #         date      total
    #    0    january   1000
    #    1    february  2000
    #    ...  ...       ...

    vbar(df,
         abscissa="date",
         ordinate="total",
         legend=legend,
         output_path=output_path,
         title=title)
    return df


def draw_transactions_year(data: OrderedDict[str, pd.DataFrame],
                           ref_name: str,
                           output_path: str,
                           title: str) -> pd.DataFrame:
    """
    Generate a graph that represents the repartition of transactions (in BTC) per vendor and per month,
    in the form of a series of boxplots. Each boxplot shows the repartition of transactions  (in BTC) per vendor for
    a given month.

    :param data: the input data. This is an ordered dictionary which keys are the dates and the values the associated
                 dataframes. Please note that the dataframes must contain a column named "ref_name" (see next
                 parameter).
    :param ref_name: the name of the column to use as data.
    :param output_path: the path to the file used to store the graph.
    :param title: the title of the graph.
    :return: a Dataframes that contains 2 columns:
    - the first columns contains the names of the months.
    - the second columns contains the data associated with the months.
    """

    # We build a dataframe that looks something like:
    #
    #              btc     month
    #       0        0       jan
    #       1        1       jan
    #       2        2       jan
    #       ...
    #       n        0       feb
    #       n+1     11       feb
    #       n+2     22       feb
    #       ...

    dataframe = pd.DataFrame([], columns=['btc', 'month'])
    month: str
    btc_values: pd.DataFrame
    for month, btc_values in data.items():
        n = pd.DataFrame(btc_values[ref_name])
        n['month'] = month
        dataframe = dataframe.append(n, ignore_index=True)
    multiple_boxplot_seaborn(dataframe, 'month', 'btc')
    return dataframe
