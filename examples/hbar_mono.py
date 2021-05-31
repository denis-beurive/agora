import pandas as pd
from agora.graph import HBarMono


df = pd.DataFrame({'ordinate': ["a", "b", "c", "d", "e"],
                   'abscissa': [10, 20, 30, 40, 50]})

g = HBarMono(df)
print(g.draw())

