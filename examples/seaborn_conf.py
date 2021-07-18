from typing import Optional
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


def set_graph_properties(abscissa_legend: Optional[str],
                         ordinate_legend: Optional[str],
                         title: str,
                         left_shift: float):
    """
    Set the image properties.

    :param abscissa_legend: the message that describes the X-axis (optional).
    :param ordinate_legend: the message that describes the Y-axis (optional).
    :param title: image title.
    :param left_shift: left shift.
    """
    figure(figsize=(26, 16), dpi=80)
    if abscissa_legend is not None:
        plt.xlabel(abscissa_legend)
    if ordinate_legend is not None:
        plt.ylabel(ordinate_legend)
    plt.title(title)
    plt.rcParams['savefig.format'] = "svg"
    plt.rcParams['figure.subplot.left'] = left_shift
    plt.close('all')


data = pd.DataFrame({
    'abscissa': [0, 1, 2, 3],
    'ordinate': [0, 10, 20, 30]
})


set_graph_properties(None,
                     None,
                     'title',
                     0.1)

sns.barplot(x='abscissa', y='ordinate', data=data, orient='v')
plt.savefig('/tmp/test')

