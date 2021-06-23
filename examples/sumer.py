import pandas as pd
from typing import OrderedDict
import collections as co


def draw_transactions_total_amounts(transactions: OrderedDict[str, pd.DataFrame], ref_name: str):
    df = pd.DataFrame()

    df['date'] = transactions.keys()
    df['total'] = [d[ref_name].sum() for d in transactions.values()]

    # for label, dataframe in transactions.items():
    #     series: pd.Series = dataframe[ref_name]
    #     df[label] = [series.sum()]

    return df


df1 = pd.DataFrame({
    "c1": [0, 1, 2],
    "c2": [0, 1, 2]
})

df2 = pd.DataFrame({
    "c1": [0, 10, 20],
    "c2": [0, 100, 200]
})

print(df1)
print(df2)


data = co.OrderedDict()
data['jan'] = df1
data['feb'] = df2

res = draw_transactions_total_amounts(data, 'c1')
print(res)

