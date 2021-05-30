import pandas as pd


df = pd.DataFrame({'X': [1, 2, 3, 4, 5],
                   'Y': [1, 2, 3, 4, 5],
                   'Z': [3, 4, 5, 6, 3]})
print("DataFrame:")
print(df)

#   DataFrame:
#      X  Y  Z
#   0  1  1  3
#   1  2  2  4
#   2  3  3  5
#   3  4  4  6
#   4  5  5  3

sums = df.sum(axis=1)
print("Row-wise sum:")
print(sums)

#       sum(X+Y+Z)
#   0       5
#   1       8
#   2       11
#   3       14
#   4       13
