import pandas as pd
import plotly.graph_objects as go

df = pd.DataFrame({'abscissa': ["a", "b", "c", "d", "e"],
                   'ordinate': [10, 20, 30, 40, 50]})
print(df['ordinate'])

fig = go.Figure(data=go.Bar(x=df.get('abscissa'), y=df.get('ordinate')))
fig.write_html('first_figure.html', auto_open=True)
