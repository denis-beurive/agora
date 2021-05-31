import pandas as pd
from agora.graph import HBarMulti


df = pd.DataFrame({'ordinate': ["a", "b", "c", "d", "e"],
                   'Y': [10, 20, 30, 40, 50],
                   'Z': [11, 12, 13, 14, 15]})

params = [
    {'color': 'rgba(55,128,191,0.6)', 'width': 1},
    {'color': 'rgba(255,153,51,0.6)', 'width': 1}
]

g = HBarMulti(df, params)
print(g.draw())
