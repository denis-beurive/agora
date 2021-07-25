from typing import List
from random import randrange
import pandas as pd
import plotly.express as px


def generate_abscissa() -> List[str]:
    result: List[str] = []
    for x in range(200):
        result.append(chr(65 + randrange(25)))
    result.sort()
    return result


def generate_ordinate() -> List[int]:
    result: List[int] = []
    for x in range(200):
        result.append(randrange(100))
    return result


df = pd.DataFrame({'abscissa': generate_abscissa(),
                   'ordinate': generate_ordinate()})

print(df)

fig = px.box(df, x="abscissa", y="ordinate")
fig.show()

