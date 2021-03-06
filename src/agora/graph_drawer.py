"""
This file implements all the functions used to generate graphs.
"""

import pandas as pd
from typing import OrderedDict, Optional
from .stat import get_count_per_column_value, \
    get_average_per_column_value, \
    get_max_per_column_value, \
    get_sum_per_column_value
from .graph import hbar, vbar, single_boxplot, multiple_boxplot


def draw_transactions_counts_repartition(data: pd.DataFrame,
                                         ref_name: str,
                                         output_path: str,
                                         date: str,
                                         left_offset: float) -> pd.DataFrame:
    """
    Generate a boxplot graph that represents the repartition of transactions, considering the total number of
    transactions per "reference". The "reference" is a column name specified by the parameter "currency". Typically,
    the "reference" can be: "vendor_name" or "ship_from".

    :param data: the data frame.
    :param ref_name: the name of the column to use as reference.
    :param output_path: path to the file used to store the representation.
    :param date: the date.
    :param left_offset: offset between the left edge of the image and the y-axis.
    :return: a data frame tha contains 2 columns:
             - the first column contains the "reference" names (and its name is given by the parameter "currency").
             - the second column contains the total number of transactions per "reference". The name of this column
               is "count".
    """
    sub_data = get_count_per_column_value(data, ref_name)
    counts: pd.Series = sub_data['count']
    df = pd.DataFrame({
        ref_name: pd.Series(['transactions' for _ in range(len(counts))]),
        'count': counts
    })
    reference = "vendor" if ref_name == "vendor_name" else "shipping locality"
    title = "{} - Total number of transactions per {}".format(date, reference)
    single_boxplot(df,
                   ref_name,
                   'count',
                   None,
                   None,
                   output_path,
                   title,
                   left_offset)
    return sub_data


def draw_transactions_average_amounts_repartition(data: pd.DataFrame,
                                                  ref_name: str,
                                                  output_path: str,
                                                  date: str,
                                                  left_offset: float) -> pd.DataFrame:
    """
    Generate a boxplot graph that represents the repartition of transactions, considering the average transaction
    amount in BTC per "reference". The "reference" is a column name specified by the parameter "currency". Typically,
    the "reference" can be: "vendor_name" or "ship_from".

    :param data: the data frame.
    :param ref_name: the name of the column to use as reference ("vendor_name" or "ship_from").
    :param output_path: path to the file used to store the representation.
    :param date: the date.
    :param left_offset: offset between the left edge of the image and the y-axis.
    :return: a data frame tha contains 2 columns:
         - the first column contains the "reference" names (and its name is given by the parameter "currency").
         - the second column contains the average transaction amount per "reference" (which name is given
           within the first column), in BTC. The name of this column is "btc".
    """
    sub_data = get_average_per_column_value(data, ref_name, 'btc')
    btc: pd.Series = sub_data['btc']

    df = pd.DataFrame({
        ref_name: pd.Series(['btc' for _ in range(len(btc))]),
        'btc': btc
    })
    reference = "vendor" if ref_name == "vendor_name" else "shipping locality"
    title = "{} - Average transaction amount in BTC per {}".format(date, reference)
    single_boxplot(df,
                   ref_name,
                   'btc',
                   None,
                   None,
                   output_path,
                   title,
                   left_offset)
    return sub_data


def draw_transactions_max_amounts_repartition(data: pd.DataFrame,
                                              ref_name: str,
                                              output_path: str,
                                              date: str,
                                              left_offset: float) -> pd.DataFrame:
    """
    Generate a boxplot graph that represents the repartition of transactions, considering the maximum transaction
    amount in BTC per "reference". The "reference" is a column name specified by the parameter "currency". Typically,
    the "reference" can be: "vendor_name" or "ship_from".

    :param data: the data frame.
    :param ref_name: the name of the column to use as reference.
    :param output_path: path to the file used to store the representation.
    :param date: the date.
    :param left_offset: offset between the left edge of the image and the y-axis.
    :return: a data frame that contains 2 columns:
         - the first column contains the "reference" names (and its name is given by the parameter "currency").
         - the second column contains the maximum transaction amount per "reference" (which name is given
           within the first column), in BTC. The name of this column is "btc".
    """
    sub_data = get_max_per_column_value(data, ref_name, 'btc')
    btc: pd.Series = sub_data['btc']
    df = pd.DataFrame({
        ref_name: pd.Series(['btc' for _ in range(len(btc))]),
        'btc': btc
    })
    reference = "vendor" if ref_name == "vendor_name" else "shipping locality"
    title = "{} - Maximum transaction amount in BTC per {}".format(date, reference)
    single_boxplot(df,
                   ref_name,
                   'btc',
                   None,
                   None,
                   output_path,
                   title,
                   left_offset)
    return sub_data


def draw_transactions_sum_amounts_repartition(data: pd.DataFrame,
                                              ref_name: str,
                                              output_path: str,
                                              date: str,
                                              left_offset: float) -> pd.DataFrame:
    """
    Generate a boxplot graph that represents the repartition of transactions, considering the sum of all
    transaction amounts in BTC per "reference". The "reference" is a column name specified by the parameter
    "currency". Typically, the "reference" can be: "vendor_name" or "ship_from".

    :param data: the data frame.
    :param ref_name: the name of the column to use as reference.
    :param output_path: path to the file used to store the representation.
    :param date: the date.
    :param left_offset: offset between the left edge of the image and the y-axis.
    :return: a data frame that contains 2 columns:
         - the first column contains the "reference" names (and its name is given by the parameter "currency").
         - the second column contains the sum of all transaction amounts per "reference" (which name is given
           within the first column), in BTC. The name of this column is "btc".
    """
    sub_data = get_sum_per_column_value(data, ref_name, 'btc')
    btc: pd.Series = sub_data['btc']
    df = pd.DataFrame({
        ref_name: pd.Series(['btc' for _ in range(len(btc))]),
        'btc': btc
    })
    reference = "vendor" if ref_name == "vendor_name" else "shipping locality"
    title = "{} - Sum of all transaction amounts in BTC per {}".format(date, reference)
    single_boxplot(df,
                   ref_name,
                   'btc',
                   None,
                   None,
                   output_path,
                   title,
                   left_offset)
    return sub_data


def draw_transactions_count_greater_than(data: pd.DataFrame,
                                         ref_name: str,
                                         top_count: int,
                                         output_path: str,
                                         date: str,
                                         left_offset: float) -> Optional[pd.DataFrame]:
    """
    Generate a horizontal BAR diagram that represents the total number of transactions per "reference",
    for transactions counts greater than a given ceiling.

    Reference can be: vendor or shipping locality.

    Please note that vendors whose total number of transactions is lower than a given value are ignored.

    :param data: the input data. This is a data frame that contains 2 columns:
                 - the first column contains the "reference" names (and its name is given by the parameter "currency").
                 - the second column contains the total number of transactions per "reference". The name of this column
                   is "count".
    :param ref_name: the name of the column to use as reference.
    :param top_count: the number of "top" "references" to print.
    :param output_path: the path to the file used to store the graph.
    :param date: the date.
    :param left_offset: offset between the left edge of the image and the y-axis.
    :return: a data frame that contains 2 columns:
                - the first column contains the "reference" names (and its name is given by the parameter "currency").
                - the second column contains the number of transaction "reference" (which name is given
                  within the first column). The name of this column is "count".
             or None if the ceiling value is too high.

    """
    # sub_data = data[data["count"] > ceiling]
    sub_data = data.nlargest(top_count, "count")

    sub_data = sub_data.sort_values(by="count", axis=0, inplace=False)
    if len(sub_data) == 0:
        return None
    reference = "vendor" if ref_name == "vendor_name" else "shipping locality"
    title = "{} - Total number of transactions per {}".format(date, reference)
    hbar(sub_data,
         "count",
         ref_name,
         "Total number of transactions",
         reference,
         output_path,
         title,
         left_offset)
    return sub_data


def draw_transactions_average_amounts_greater_than(data: pd.DataFrame,
                                                   ref_name: str,
                                                   top_count: int,
                                                   output_path: str,
                                                   date: str,
                                                   left_offset: float) -> Optional[pd.DataFrame]:
    """
    Generate a horizontal BAR diagram that represents the average transaction amount (in BTC) per "reference",
    for transactions amounts greater than a given ceiling.

    Reference can be: vendor or shipping locality.

    Please note that "references" whose average transaction amount is lower than a given value are ignored.

    :param data: the input data. This is a data frame that contains 2 columns:
                 - the first column contains the "reference" names (and its name is given by the parameter "currency").
                 - the second column is the average transaction amount for the vendor, in BTC
                   (and its columns is "btc").
    :param ref_name: the name of the column to use as reference.
    :param top_count: the number of "top" "references" to print.
    :param output_path: the path to the file used to store the graph.
    :param date: the date.
    :param left_offset: offset between the left edge of the image and the y-axis.
    :return: if there is at least one "reference" (vendor or shipping locality) that has
             a data frame that contains 2 columns:
                - the first column contains the "reference" names (and its name is given by the parameter "currency").
                - the second column contains the average transaction amount per "reference" (which name is given
                  within the first column), in BTC. The name of this column is "btc".
             or None if the ceiling value is too high.
    """
    # sub_data = data[data["btc"] > ceiling]
    sub_data = data.nlargest(top_count, "btc")
    sub_data = sub_data.sort_values(by="btc", axis=0, inplace=False)

    if len(sub_data) == 0:
        return None

    reference = "vendor" if ref_name == "vendor_name" else "shipping locality"
    title = "{} - Average amount per transactions in BTC per {}".format(date, reference)
    hbar(sub_data,
         "btc",
         ref_name,
         "Average amount per transactions in BTC",
         reference,
         output_path,
         title,
         left_offset)
    return sub_data


def draw_transactions_max_amounts_greater_than(data: pd.DataFrame,
                                               ref_name: str,
                                               top_count: int,
                                               output_path: str,
                                               date: str,
                                               left_offset: float) -> Optional[pd.DataFrame]:
    """
    Generate a horizontal BAR diagram that represents the maximum transaction amount (in BTC) per "reference",
    for transactions amounts greater than a given ceiling.

    Reference can be: vendor or shipping locality.

    Please note that "references" whose average transaction amount is lower than a given value are ignored.

    :param data: the input data. This is a data frame that contains 2 columns:
                 - the first column contains the "reference" names (and its name is given by the parameter "currency").
                 - the second column is the maximum transaction amount for the vendor, in BTC
                   (and its columns is "btc").
    :param ref_name: the name of the column to use as reference.
    :param top_count: the number of "top" "references" to print.
    :param output_path: the path to the file used to store the graph.
    :param date: the date.
    :param left_offset: offset between the left edge of the image and the y-axis.
    :return: a data frame that contains 2 columns:
                - the first column contains the "reference" names (and its name is given by the parameter "currency").
                - the second column contains the maximum transaction per "reference" (which name is given within the first
                  column), in BTC. The name of this column is "btc".
             or None if the ceiling value is too high.
    """
    # sub_data = data[data["btc"] > ceiling]
    sub_data = data.nlargest(top_count, "btc")
    sub_data = sub_data.sort_values(by="btc", axis=0, inplace=False)

    if len(sub_data) == 0:
        return None

    reference = "vendor" if ref_name == "vendor_name" else "shipping locality"
    title = "{} - Maximum amount per transactions in BTC per {}".format(date, reference)
    hbar(sub_data,
         "btc",
         ref_name,
         "Maximum amount per transactions in BTC",
         reference,
         output_path,
         title,
         left_offset)
    return sub_data


def draw_transactions_sum_amounts_greater_than(data: pd.DataFrame,
                                               ref_name: str,
                                               top_count: int,
                                               output_path: str,
                                               date: str,
                                               left_offset: float) -> Optional[pd.DataFrame]:
    """
    Generate a horizontal BAR diagram that represents the total amount of transaction (in BTC) per "reference",
    for total transactions amounts greater than a given ceiling.

    Reference can be: vendor or shipping locality.

    Please note that "references" whose average transaction amount is lower than a given value are ignored.

    :param data: the input data. This is a data frame that contains 2 columns:
                 - the first column contains the "reference" names (and its name is given by the parameter "currency").
                 - the second column is the total amount of transactions for the vendor, in BTC
                   (and its columns is "btc").
    :param ref_name: the name of the column to use as reference.
    :param top_count: the number of "top" "references" to print.
    :param output_path: the path to the file used to store the graph.
    :param date: the date.
    :param left_offset: offset between the left edge of the image and the y-axis.
    :return: a data frame that contains 2 columns:
                - the first column contains the "reference" names (and its name is given by the parameter "currency").
                - the second column contains the total amount of transactions per "reference" (which name is given
                  within the first column), in BTC. The name of this column is "btc".
            or None if the ceiling value is too high.
    """
    # sub_data = data[data["btc"] > top_count]
    sub_data = data.nlargest(top_count, "btc")
    sub_data = sub_data.sort_values(by="btc", axis=0, inplace=False)

    if len(sub_data) == 0:
        return None

    reference = "vendor" if ref_name == "vendor_name" else "shipping locality"
    title = "{} - Total amount of transaction in BTC per {}".format(date, reference)
    hbar(sub_data,
         "btc",
         ref_name,
         "Total amount of transaction in BTC",
         reference,
         output_path,
         title,
         left_offset)
    return sub_data


def draw_transactions_total_amounts(transactions: OrderedDict[str, pd.DataFrame],
                                    currency_name: str,
                                    output_path: str,
                                    title: str,
                                    left_offset: float) -> pd.DataFrame:
    """
    Draw a vertical BAR graph that represents the variation of the total amount of transaction in BTC of USD
    (depending on the currency of reference) over time.

    The currency of reference can be: "btc" or "usd".

    :param transactions: an ordered dictionary which keys are the dates and the values are data frames that
                         contain the data loaded from the CSV file ("01-june2014.csv"...).
    :param currency_name: the name of the column that represents the transaction amount.
                          The value of this parameter should be "btc" or "usd".
    :param output_path: the path to the file used to store the graph.
    :param title: the title of the graph.
    :param left_offset: offset between the left edge of the image and the y-axis.
    :return: a data frame that contains 2 columns:
             - a column named "date".
             - a column named "total".
    """

    df = pd.DataFrame()
    df['date'] = transactions.keys()
    df['total'] = [d[currency_name].sum() for d in transactions.values()]

    # df looks something like:
    #
    #         date      total
    #    0    january   1000
    #    1    february  2000
    #    ...  ...       ...

    vbar(df,
         abscissa="date",
         ordinate="total",
         output_path=output_path,
         title=title,
         left_offset=left_offset)
    return df


def draw_transactions_total_counts(transactions: OrderedDict[str, pd.DataFrame],
                                   output_path: str,
                                   title: str,
                                   left_offset: float) -> pd.DataFrame:
    """
    Draw a vertical BAR graph that represents the variation of the total number of transaction over time.

    :param transactions: an ordered dictionary which keys are the dates and the values are data frames that
                         contain the data loaded from the CSV file ("01-june2014.csv"...).
    :param output_path: the path to the file used to store the graph.
    :param title: the title of the graph.
    :param left_offset: offset between the left edge of the image and the y-axis.
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
         output_path=output_path,
         title=title,
         left_offset=left_offset)
    return df


def draw_whole_period_transaction_amounts_per_vendor(data: OrderedDict[str, pd.DataFrame],
                                                     currency: str,
                                                     output_path: str,
                                                     left_offset: float,
                                                     floor: Optional[float] = None,
                                                     ceiling: Optional[float] = None) -> pd.DataFrame:
    """
    Generate a graph that represents the repartition of transaction amounts (in a given currency) per vendor per month,
    in the form of a series of boxplots. Each boxplot shows the repartition of transaction amounts (in the given
    currency) for a given month.

    The currency can be: "btc" or "usd".

    :param data: the input data. This is an ordered dictionary which keys are the dates and the values the associated
                 dataframes. Please note that the dataframes must contain a column named "ref_name" (see next
                 parameter).
                 { month1 => dataframe1,
                   month2 => dataframe2,
                   ... }
                 Each value "dataframe<N>" must contain the columns "vendor_name" and "$currency" ("btc" or "usd).

    :param currency: the name of the column that contains the transactions amounts (can be "btc" or "usd").
    :param output_path: the path to the file used to store the graph.
    :param left_offset: offset between the left edge of the image and the y-axis.
    :param floor: le lowest value for y-axis.
    :param ceiling: the maximum amount to keep for the representation.
                    If you do not set this value the graph is just not readable.
    :return: a Dataframes that contains 2 columns:
             - the first columns contains the names of the months.
             - the second columns contains the data associated with the months.
               pd.DataFrame({currency: [...],
                             'month': [...]})

             Assuming that the "reference" is "btc", we return a dataframe that looks
             something like:

                          btc     month
                   0        0       jan      # Total amount of transactions for one specific vendor name
                   1        1       jan      # Total amount of transactions for another specific vendor name
                   2        2       jan      # ...
                   ...
                   n        0       feb
                   n+1     11       feb
                   n+2     22       feb
                   ...
    """

    dataframe = pd.DataFrame([], columns=[currency, 'month'])
    currency = currency.lower()
    if currency not in ('btc', 'usd'):
        raise Exception('Unexpected value for parameter "{}"!'.format(currency))

    month: str
    values: pd.DataFrame
    # We are building the dataframe that will be returned (see docstring).
    idx = 0
    for month, values in data.items():
        vendors = values['vendor_name'].unique()
        vendor: str
        for vendor in vendors:
            df_vendor: pd.DataFrame = values.query('vendor_name == "{}"'.format(vendor))
            total = df_vendor[currency].sum(axis=0, skipna=True)
            dataframe.loc[idx] = [total, month]
            idx += 1

    # I have to perform this conversion otherwise Seaborn crashes with the error:
    # "ValueError: object arrays are not supported"
    # I've lost too much time on this problem. Please let me know if you can explain the behavior!
    new_df = pd.DataFrame(dataframe.to_dict())
    multiple_boxplot(new_df,
                     'month',
                     currency,
                     'Date',
                     currency,
                     output_path,
                     "Total amount of transactions in {} per vendor".format(currency.upper()),
                     left_offset,
                     floor,
                     ceiling)
    return new_df


def draw_whole_period_transactions_counts_per_vendor(data: OrderedDict[str, pd.DataFrame],
                                                     output_path: str,
                                                     left_offset: float,
                                                     floor: Optional[float] = None,
                                                     ceiling: Optional[float] = None) -> pd.DataFrame:
    """
    Generate a graph that represents the repartition of transaction counts per vendors per month, in the form
    of a series of boxplots. Each boxplot shows the repartition of transaction counts per vendor for a given
    month.

    :param data: the input data. This is an ordered dictionary which keys are the dates and the values the associated
                 dataframes.
                 { month1 => dataframe1,
                   month2 => dataframe2,
                   ... }
                 Each value "dataframe<N>" must contain the column "vendor_name".
    :param output_path: the path to the file used to store the graph.
    :param left_offset: offset between the left edge of the image and the y-axis.
    :param floor: le lowest value for y-axis.
    :param ceiling: the maximum amount to keep for the representation.
                    If you do not set this value the graph is just not readable.
    :return: a Dataframes that contains 2 columns:
             - the first columns (maned "month") contains the names of the months.
             - the second columns (named "count") contains the data associated with the months (ie: the number
               of transactions per month).
               pd.DataFrame({'month': [...],
                             'count': [...]})

             We return a dataframe that looks something like:

                        count     month
                   0        1       jan     # Total count of transactions for one specific vendor name
                   1        1       jan     # Total count of transactions for another specific vendor name
                   2        2       jan     # ...
                   ...
                   n        1       feb
                   n+1     11       feb
                   n+2     22       feb
                   ...
    """
    dataframe = pd.DataFrame([], columns=['count', 'month'])
    month: str
    values: pd.DataFrame
    # We are building the dataframe that will be returned (see docstring).
    idx = 0
    for month, values in data.items():
        vendors = values['vendor_name'].unique()
        vendor: str
        for vendor in vendors:
            df_vendor: pd.DataFrame = values.query('vendor_name == "{}"'.format(vendor))
            count = len(df_vendor.index)
            dataframe.loc[idx] = [count, month]
            idx += 1

    # I have to perform this conversion otherwise Seaborn crashes with the error:
    # "ValueError: object arrays are not supported"
    # I've lost too much time on this problem. Please let me know if you can explain the behavior!
    new_df = pd.DataFrame(dataframe.to_dict())
    multiple_boxplot(new_df,
                     'month',
                     'count',
                     'Months',
                     'Total number of transactions',
                     output_path,
                     "Total number of transactions per vendor",
                     left_offset,
                     floor,
                     ceiling)
    return new_df
