import pandas as pd
import plotly.express as px

df = pd.DataFrame({'population': [50, 25, 25],
                   'country': ['France', 'England', 'Italy']})


fig = px.pie(df, values='population', names='country', title='Population')
fig.show()

