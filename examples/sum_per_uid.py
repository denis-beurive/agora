from typing import Tuple
import pandas as pd
from numpy import ndarray


df = pd.DataFrame({'X': [1, 1, 3, 3, 5],
                   'Y': [1, 2, 3, 4, 5],
                   'Z': [3, 4, 5, 6, 3]})
print("DataFrame:")
print(df)

#      X  Y  Z
#   0  1  1  3
#   1  1  2  4
#   2  3  3  5
#   3  3  4  6
#   4  5  5  3

print(df.groupby('X').sum())

#   X sum(Y) sum(Z)
#   1   3      7
#   3   7      11
#   5   5      3

# ---------------------------------------------------------------------------
# We extract a "slice" of the data frame (the columns "X" and "Y").
# ---------------------------------------------------------------------------

result: pd.DataFrame = df[['X', 'Y']].groupby('X').sum()
print(result)

#   X sum(Y)
#   1   3
#   3   7
#   5   5

print(result.to_json())
item: Tuple
for item in result.items():
    name: str = item[0]
    series: pd.Series = item[1]

# ---------------------------------------------------------------------------
# We use a user-provided aggregator.
# ---------------------------------------------------------------------------


def aggregator(s: pd.Series) -> float:
    """
    Aggregates a series.

    The parameter "s" contains the following data:
        - the name of the column. It can be "Y" or "Z".
        - the values within the column.

    Please note that this aggregator does the perform the same action whether the column is "X" or "Y".

    :param s: the series to aggregate.
    :return: the aggregation.
    """

    def action(in_column_name: str, in_values: ndarray) -> float:
        total = 0
        if in_column_name == 'Y':
            for x in in_values:
                total += x
        if in_column_name == 'Z':
            for x in in_values:
                total += 2*x
        return total

    column_name: str = str(s.name)  # "Y" or "Z"
    return action(column_name, s.values)


result: pd.DataFrame = df.groupby('X').agg(func=aggregator)
print(result)

#   X  sum(Y) sum(2*Z)
#   1    3       14
#   3    7       22
#   5    5       6

print(result.to_json())

