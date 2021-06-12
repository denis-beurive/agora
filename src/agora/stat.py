from typing import Callable, Any
import pandas as pd
from statistics import mean, median


def get_count_per_column_value(in_data: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Given a data frame "D" and a column name "C" (that appears in "D"), returns a data frame
    that contains two columns:
    - the first column contains distinct values from the column "C".
    - the second column contains the number of times a corresponding value from column "C" appears in "D".

    :param in_data: the data frame.
    :param column_name: the name of the column.
    :return: a data frame that contains two columns, as described earlier.
    """
    sub_data: pd.DataFrame = in_data.filter(items=[column_name], axis=1)
    sub_data['count'] = 0
    return sub_data.groupby(by=column_name, as_index=False).agg(lambda x: len(list(x)))  # x: numpy.ndarray


def get_stat_per_column_value(in_data: pd.DataFrame,
                              group_by_column_name: str,
                              value_column_name: str,
                              function: Callable) -> pd.DataFrame:
    sub_data: pd.DataFrame = in_data.filter([group_by_column_name, value_column_name], axis=1)
    return sub_data.groupby(by=group_by_column_name, as_index=False).agg(function)


def get_average_per_column_value(in_data: pd.DataFrame,
                                 group_by_column_name: str,
                                 value_column_name: str) -> pd.DataFrame:
    return get_stat_per_column_value(in_data, group_by_column_name, value_column_name, lambda x: mean(list(x)))


def get_median_per_column_value(in_data: pd.DataFrame,
                                group_by_column_name: str,
                                value_column_name: str) -> pd.DataFrame:
    return get_stat_per_column_value(in_data, group_by_column_name, value_column_name, lambda x: median(list(x)))
