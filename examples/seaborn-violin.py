from typing import Any
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def classname(obj: Any) -> str:
    cls = type(obj)
    module = cls.__module__
    name = cls.__qualname__
    if module is not None and module != "__builtin__":
        name = module + "." + name
    return name


# Set options for Pandas.
pd.set_option("display.max_rows", None, "display.max_columns", None)

data = pd.DataFrame({
    'column1': [0, 1, 2, 3],
    'column2': [0, 10, 20, 30],
    'column3': [0, 100, 200, 300]
})

print(data)
sns.violinplot(x='column1', y='column2', data=data)
plt.xlabel("name of the X label")
plt.ylabel("name of the Y label")
plt.title("the title")
plt.rcParams['savefig.format'] = 'svg'
plt.rcParams['savefig.directory'] = '/tmp'
plt.show()
