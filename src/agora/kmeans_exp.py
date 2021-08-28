"""
This module implements k-means functionalities.

Test:

    From the project root folder:

    python -m agora.kmeans_exp

    Note: make sure to run "pipenv install --dev" first!
"""

from typing import Tuple
import pandas as pd
from sklearn.cluster import KMeans
from agora.stat import get_stat_per_column_value, get_count_per_column_value


def km_data_amount_count(in_data: pd.DataFrame) -> pd.DataFrame:
    """
    Create the DataFrame used to use the k-means clustering algorithm.
    This DataFrame contains 3 columns:
        - the first column is the name of the vendor.
        - the second column is the total transaction amount in BTC.
        - the third column is the total number of transactions.

    Example:

        Input:

              vendor_name  btc
            0          v1    1
            1          v1    2
            2          v1    3
            3          v2    5
            4          v2    5
            5          v3  200

        Output:

              vendor_name  count  btc
            0          v1      3    6
            1          v2      2   10
            2          v3      1  200

    :param in_data: the Agora data.
    :return: a DataFrame that contains 3 columns:
             - the first column is the name of the vendor.
             - the second column is the total transaction amount in BTC.
             - the third column is the total number of transactions.
    """
    # We create 2 DataFrames.
    #
    # First DataFrame (number of transactions per vendor):
    #
    #      vendor_name   count
    #      v1            10
    #      v2            5
    #      ...           ...
    #
    # Second DataFrame (total amount of transactions per vendor):
    #
    #      vendor_name   btc
    #      v1            200000
    #      v2            1000000000
    #      ...           ...

    vendor_counts = get_count_per_column_value(in_data, 'vendor_name')
    vendor_amount = get_stat_per_column_value(in_data, 'vendor_name', 'btc', lambda x: sum(list(x)))

    # We merge the 2 previously created DataFrames.
    #
    #      vendor_name   number_of_transactions   total_transaction_amount
    #      v1            10                       200000
    #      v2            5                        1000000000

    data = pd.merge(vendor_counts, vendor_amount, on="vendor_name")
    return data


def km_calc_amount_count(in_data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Apply the KMeans algorithm on a DataFrame that contains data from Agora.

    Example:

        Input:

              vendor_name  btc
            0          v1    1
            1          v1    2
            2          v1    3
            3          v2    5
            4          v2    5
            5          v3  200

        Output:

            The centroids:

                [[  2.5   8. ]
                 [  1.  200. ]]

            The entities grouped by centroid:

                  vendor_name  count  btc  labels
                0          v1      3    6       0
                1          v2      2   10       0
                2          v3      1  200       1

    Please look at the column "lebels" to link the entities and the centroids:
        'labels = 0' => [ 2.5    8. ]
        'labels = 1' => [ 1.   200.. ]

    :param in_data: the Agora data.
    :return: the function returns 2 values.
             - the first value contains the coordinates of the centroids.
             - the second value contains the entities grouped by centroid.
    """
    v = km_data_amount_count(in_data)
    kmeans = KMeans(n_clusters=2, n_init=3, max_iter=3000, random_state=1)
    kmeans = kmeans.fit(v[['count', 'btc']])
    v.loc[:, 'labels'] = kmeans.labels_
    centroids = kmeans.cluster_centers_
    return centroids, v


if __name__ == "__main__":

    d = pd.DataFrame({'vendor_name': ['v1', 'v1', 'v1', 'v2', 'v2', 'v3'],
                      'btc': [1, 2, 3, 5, 5, 200]})
    v = km_data_amount_count(d)
    print(d)
    print(v)

    centroids, v = km_calc_amount_count(d)
    print(centroids)
    print(v)
