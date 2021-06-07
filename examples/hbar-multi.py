import pandas as pd
import plotly.graph_objects as go

STACKED = True

df = pd.DataFrame({'ordinate': ["a", "b", "c", "d", "e"],
                   'A': [10, 20, 30, 40, 50],
                   'B': [11, 21, 31, 41, 51]})
print(df['ordinate'])

fig = go.Figure(data=go.Bar(x=df.get('A'), y=df.get('ordinate'), orientation='h'))
fig = go.Figure(go.Bar(x=df.get('A'), y=df.get('ordinate'), name='Montreal', orientation='h'))
fig.add_trace(go.Bar(x=df.get('B'), y=df.get('ordinate'), name='Ottawa', orientation='h'))

if STACKED:
    fig.update_layout(barmode='stack')
fig.write_html('first_figure.html', auto_open=True)
