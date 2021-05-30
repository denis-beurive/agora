

# pandas.Series

    import pandas as pd

    vendor_name: pd.Series = data.get('vendor_name')
    c: pd.Series = vendor_name.value_counts()
    c.plot(kind='bar')

# Saving plots

    import pandas as pd

    vendor_name: pd.Series = data.get('vendor_name')
    c: pd.Series = vendor_name.value_counts()
    g = c.plot(kind='bar')
    g.get_figure().savefig('output.png')

