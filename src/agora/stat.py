"""
This file implements functions that perform common operations on dataframes.
"""

from typing import Callable
from dataclasses import dataclass
import pandas as pd
from statistics import mean, median
from numpy import float64, percentile


@dataclass(frozen=False)
class BoxPlotData:
    """
    This class is a container for BoxPlot data.
    """
    q1: float64
    q3: float64
    iqr: float64
    lower_fence: float64
    upper_fence: float64

    def __init__(self, q1: float64, q3: float64):
        self.q1 = q1
        self.q3 = q3
        self.iqr = q3 - q1
        self.lower_fence = q1 - (1.5 * self.iqr)
        self.upper_fence = q3 + (1.5 * self.iqr)


def get_count_per_column_value(in_data: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Given a data frame "D" that contains **at least** 1 column "C", the function returns a dataframe.
    The returned dataframe contains 2 columns:
    - the first column (which name is "C") contains distinct values from the column "C".
    - the second column (which name is "count") contains the number of times a corresponding value
      from column "C" appears in "D".

    Examples:

        in_data (D):

                   c1  c2
                0   1  10
                1   2  10
                2   3  10
                3   4  40
                4   5  50

        get_count_per_column_value(D, 'c1'):

                   c1  count
                0   1      1
                1   2      1
                2   3      1
                3   4      1
                4   5      1

        get_count_per_column_value(D, 'c2'):

                   c2  count
                0  10      3
                1  40      1
                2  50      1

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
    """
    Create series by grouping values according to a given column.
    Then apply a given function to the created series.

    Example:

        in_data (in_data):

                   c1  c2
                0  10   1
                1  10   2
                2  10   3
                3  40   4
                4  50   5

        Let's consider the following hypothesis:
          - the function to apply is: "stat_function(data: list) -> Union[int, float]"
          - we execute: get_stat_per_column_value(in_data, 'c1', 'c2', stat_function)

        1. Create series by grouping values according to the column "c1":

                   c1  c2
                0  10  [1, 2, 3]
                1  40  [4]
                2  50  [5]

        2. Apply the function "stat_function" to the series:

                   c1  c2
                0  10  stat_function([1, 2, 3])
                1  40  stat_function([4])
                2  50  stat_function([5])

    :param in_data: the data frame.
    :param group_by_column_name: the name of the column upon which data are grouped.
    :param value_column_name: the name of the column upon which the series are created.
    :param function: the function to apply on the series. The function signature must be:
                     stat_function(data: list) -> Union[int, float]
    :return: a data frame that contains two columns:
             - the first column name is the value of the parameter "group_by_column_name".
             - the second column name is the value of the parameter "value_column_name".


    """
    sub_data: pd.DataFrame = in_data.filter([group_by_column_name, value_column_name], axis=1)
    return sub_data.groupby(by=group_by_column_name, as_index=False).agg(function)


def get_average_per_column_value(in_data: pd.DataFrame,
                                 group_by_column_name: str,
                                 value_column_name: str) -> pd.DataFrame:
    """
    Create series by grouping values according to a given column.
    Then calculate the average values of the created series.

    Example:

        in_data (in_data):

                   c1  c2
                0  10   1
                1  10   2
                2  10   3
                3  40   4
                4  50   5

        Let's consider the following hypothesis:
          - we execute: get_average_per_column_value(in_data, 'c1', 'c2')

        1. Create series by grouping values according to the column "c1":

                   c1  c2
                0  10  [1, 2, 3]
                1  40  [4]
                2  50  [5]

        2. Calculate the average values of the created series.

                   c1  c2
                0  10  avg([1, 2, 3])
                1  40  avg([4])
                2  50  avg([5])

    :param in_data: the data frame.
    :param group_by_column_name: the name of the column upon which data are groped.
    :param value_column_name: the name of the column upon which the series are created.
    :return: a data frame that contains two columns:
             - the first column name is the value of the parameter "group_by_column_name".
             - the second column name is the value of the parameter "value_column_name".
    """
    return get_stat_per_column_value(in_data, group_by_column_name, value_column_name, lambda x: mean(list(x)))


def get_median_per_column_value(in_data: pd.DataFrame,
                                group_by_column_name: str,
                                value_column_name: str) -> pd.DataFrame:
    """
    Create series by grouping values according to a given column.
    Then calculate the median values of the created series.

    Example:

        in_data (in_data):

                   c1  c2
                0  10   1
                1  10   2
                2  10   3
                3  40   4
                4  50   5

        Let's consider the following hypothesis:
          - we execute: get_median_per_column_value(in_data, 'c1', 'c2')

        1. Create series by grouping values according to the column "c1":

                   c1  c2
                0  10  [1, 2, 3]
                1  40  [4]
                2  50  [5]

        2. Calculate the median values of the created series.

                   c1  c2
                0  10  median([1, 2, 3])
                1  40  median([4])
                2  50  median([5])

    :param in_data: the data frame.
    :param group_by_column_name: the name of the column upon which data are groped.
    :param value_column_name: the name of the column upon which the series are created.
    :return: a data frame that contains two columns:
             - the first column name is the value of the parameter "group_by_column_name".
             - the second column name is the value of the parameter "value_column_name".
    """
    return get_stat_per_column_value(in_data, group_by_column_name, value_column_name, lambda x: median(list(x)))


def get_max_per_column_value(in_data: pd.DataFrame,
                             group_by_column_name: str,
                             value_column_name: str) -> pd.DataFrame:
    """
    Create series by grouping values according to a given column.
    Then keep the maximum values from the created series.

    Example:

        in_data (in_data):

                   c1  c2
                0  10   1
                1  10   2
                2  10   3
                3  40   4
                4  50   5

        Let's consider the following hypothesis:
          - we execute: get_max_per_column_value(in_data, 'c1', 'c2', stat_function)

        1. Create series by grouping values according to the column "c1":

                   c1  c2
                0  10  [1, 2, 3]
                1  40  [4]
                2  50  [5]

        2. Calculate the max values of the created series.

                   c1  c2
                0  10  max([1, 2, 3])
                1  40  max([4])
                2  50  max([5])

    :param in_data: the data frame.
    :param group_by_column_name: the name of the column upon which data are groped.
    :param value_column_name: the name of the column upon which the series are created.
    :return: a data frame that contains two columns:
             - the first column name is the value of the parameter "group_by_column_name".
             - the second column name is the value of the parameter "value_column_name".
    """
    return get_stat_per_column_value(in_data, group_by_column_name, value_column_name, lambda x: max(list(x)))


def get_sum_per_column_value(in_data: pd.DataFrame,
                             group_by_column_name: str,
                             value_column_name: str) -> pd.DataFrame:
    """
    Create series by grouping values according to a given column.
    Then calculates the sums from the created series.

    Example:

        in_data (in_data):

                   c1  c2
                0  10   1
                1  10   2
                2  10   3
                3  40   4
                4  50   5

        Let's consider the following hypothesis:
          - we execute: get_max_per_column_value(in_data, 'c1', 'c2', stat_function)

        1. Create series by grouping values according to the column "c1":

                   c1  c2
                0  10  [1, 2, 3]
                1  40  [4]
                2  50  [5]

        2. Calculate the sum from the created series.

                   c1  c2
                0  10  sum([1, 2, 3])
                1  40  sum([4])
                2  50  sum([5])

    :param in_data: the data frame.
    :param group_by_column_name: the name of the column upon which data are groped.
    :param value_column_name: the name of the column upon which the series are created.
    :return: a data frame that contains two columns:
             - the first column name is the value of the parameter "group_by_column_name".
             - the second column name is the value of the parameter "value_column_name".
    """
    return get_stat_per_column_value(in_data, group_by_column_name, value_column_name, lambda x: sum(list(x)))


def calculate_boxplot_data(in_data: pd.DataFrame, column_name: str) -> BoxPlotData:
    """
    Calculate boxplot data from values extracted from a data frame column (identified by its name).

    :param in_data: the data frame.
    :param column_name: the name of the column.
    :return: data about the boxplot.
    """
    sub_data: pd.Series = in_data[column_name]
    q3, q1 = percentile(sub_data, [75, 25])
    return BoxPlotData(q1, q3)


if __name__ == "__main__":

    # Example for "get_count_per_column_value()"

    df = pd.DataFrame({'c1': [1, 2, 3, 4, 5],
                       'c2': [10, 10, 10, 40, 50]})
    print(df)
    res = get_count_per_column_value(df, 'c1')
    print(res)
    res = get_count_per_column_value(df, 'c2')
    print(res)

    # Example for "get_stat_per_column_value()"

    def stat_function(data: list) -> int:
        return sum(data)

    df = pd.DataFrame({'c1': [10, 10, 10, 40, 50],
                       'c2': [1, 2, 3, 4, 5]})
    res = get_stat_per_column_value(df, 'c1', 'c2', stat_function)
    print(df)
    print(res)

    # Example for "get_max_per_column_value"

    df = pd.DataFrame({'c1': [10, 10, 10, 40, 50],
                       'c2': [1, 2, 3, 4, 5]})

    res = get_max_per_column_value(df, 'c1', 'c2')
    print(df)
    print(res)

    # Example for "get_sum_per_column_value"

    df = pd.DataFrame({'c1': [10, 10, 10, 40, 50],
                       'c2': [1, 2, 3, 4, 5]})

    res = get_sum_per_column_value(df, 'c1', 'c2')
    print(df)
    print(res)

    df = pd.DataFrame({'c1': [10, 10, 10, 40, 50],
                       'c2': [1, 2, 3, 4, 5]})

    res = calculate_boxplot_data(df, 'c1')


