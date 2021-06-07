import pandas as pd
import plotly.graph_objects as go

STACKED = True

df = pd.DataFrame({'abscissa': ["a", "b", "c", "d", "e"],
                   'Y': [10, 20, 30, 40, 50],
                   'Z': [11, 12, 13, 14, 15],
                   'T': [12, 13, 14, 15, 16]})

fig = go.Figure(go.Bar(x=df.get('abscissa'), y=df.get('Y'), name='Montreal'))
fig.add_trace(go.Bar(x=df.get('abscissa'), y=df.get('Z'), name='Ottawa'))
fig.add_trace(go.Bar(x=df.get('abscissa'), y=df.get('T'), name='Paris'))

if STACKED:
    fig.update_layout(barmode='stack')
fig.update_xaxes(categoryorder='category ascending')
fig.show()
