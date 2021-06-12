from typing import Any
import pandas as pd
import numpy


def classname(obj: Any) -> str:
    cls = type(obj)
    module = cls.__module__
    name = cls.__qualname__
    if module is not None and module != "__builtin__":
        name = module + "." + name
    return name


df = pd.DataFrame({'a': [1, 2, 3, 4, 50],
                   'b': [1, 2, 3, 4, 5],
                   'c': [3, 4, 5, 6, 3]})
print(df)

series: pd.Series = df['a']
print(series)  # -> [1, 2, 3, 4, 50]

value: numpy.int64 = df['a'][0]
print(value)
