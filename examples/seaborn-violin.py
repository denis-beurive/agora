from typing import List
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Set options for Pandas.
pd.set_option("display.max_rows", None, "display.max_columns", None)

data = pd.DataFrame({
    'column1': [0, 1, 2, 3],
    'column2': [0, 10, 20, 30],
    'column3': [0, 100, 200, 300]
})

print(data)

sns.violinplot(x='column1', y='column2', data=data)
plt.show()


