import pandas as pd


def data_top_btc_dumper(count: pd.DataFrame,
                        average: pd.DataFrame,
                        maximum: pd.DataFrame,
                        total_sum: pd.DataFrame,
                        reference: str,
                        top_length: int = 10) -> str:
    """
    Generate a Markdown representation that shows:
    - the top "references" considering the total number of transactions.
    - the top "references" considering the maximum transactions (in BTC).
    - the top "references" considering the average transactions (in BTC).

    Note: the value of the parameter "reference" can be "vendor_name" or "ship_from".

    :param count: data frame that contains the number of transactions per "reference".
                  Expected columns: "reference" ("vendor_name" or "ship_from") and "count".
    :param average: data frame that contains the average transactions per "reference".
                    Expected columns: "reference" ("vendor_name" or "ship_from") and "btc".
    :param maximum: data frame that contains the maximum transactions per "reference".
                    Expected columns: "reference" ("vendor_name" or "ship_from") and "btc".
    :param total_sum: data frame that contains the total amount of transaction per "reference".
                      Expected columns: "reference" ("vendor_name" or "ship_from") and "btc".
    :param reference: the reference. It can be: "vendor_name" or "ship_from".
    :param top_length: the number of top "references".
    :return: a string that represents a Markdown table.
    """
    top_count = count.nlargest(top_length, "count")
    top_count.reset_index(drop=True, inplace=True)
    top_average = average.nlargest(top_length, "btc")
    top_average.reset_index(drop=True, inplace=True)
    top_maximum = maximum.nlargest(top_length, "btc")
    top_maximum.reset_index(drop=True, inplace=True)
    top_sum = total_sum.nlargest(top_length, "btc")
    top_sum.reset_index(drop=True, inplace=True)

    tops = pd.DataFrame({
        'top count': top_count[reference],
        'count': top_count['count'],
        'top average (BTC)': top_average[reference],
        'average': top_average['btc'],
        'top maximum (BTC)': top_maximum[reference],
        'maximum': top_average['btc'],
        'top total (BTC)': top_sum[reference],
        'total': top_sum['btc']
    })
    return tops.to_markdown(index="never")


def data_total_dumper(data: pd.DataFrame) -> str:
    """
    Generate a Markdown representation that shows for each month the total amount of transactions.

    :param data: the dataframe. It must contains (at least) 2 columns:
                 - a column named "date".
                 - a column names "total".
    :return: a string that represents a Markdown table.
    """
    gd = pd.DataFrame({
        'date': data['date'],
        'total': data['total']
    })
    return gd.to_markdown(index="never")


def km_count_amount_dumper(data: pd.DataFrame) -> str:
    gd = pd.DataFrame({
        'vendor_name': data['vendor_name'],
        'count': data['count'],
        'btc': data['btc']
    })
    return gd.to_markdown(index="never")


if __name__ == "__main__":

    # Example for "get_count_per_column_value()"

    df = pd.DataFrame({'c1': [1, 2, 3, 4, 5],
                       'c2': [10, 10, 10, 40, 50]})
    top_count = df.nlargest(3, "c1")
    print(top_count)

