from typing import List
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt


def hbar(data: pd.DataFrame,
         abscissa: str,
         ordinate: str,
         legend: str,
         output_path: str,
         title: str) -> None:
    """
    Draw an horizontal HBAR.

    :param data: the data to plot.
    :param abscissa: the name of the column that contains the graph's abscissa.
    :param ordinate: the name of the column that contains the graph's ordinate.
    :param legend: the legend of the graph.
    :param output_path: the path to the HTML output file.
    :param title: the graph title.
    """
    fig = go.Figure(go.Bar(x=data.get(abscissa), y=data.get(ordinate), name=legend, orientation='h'))
    fig.update_layout(title_text=title)
    fig.write_html(output_path, auto_open=False)


def vbar(data: pd.DataFrame,
         abscissa: str,
         ordinate: str,
         legend: str,
         output_path: str,
         title: str) -> None:
    fig = go.Figure(go.Bar(x=data.get(abscissa), y=data.get(ordinate), name=legend, orientation='v'))
    fig.update_layout(title_text=title)
    fig.write_html(output_path, auto_open=False)


def single_boxplot(data: pd.DataFrame, abscissa: str, ordinate: str, output_path: str, title: str) -> None:
    """
    Draw a boxplot graph.

    The type of graph is used to present a repartition.

    :param data: the data to plot.
    :param abscissa: the name of the column that contains the graph's abscissa.
    :param ordinate: the name of the column that contains the graph's ordinate.
    :param output_path: the path to the HTML output file.
    :param title: the graph title.
    """
    fig = px.box(data, x=abscissa, y=ordinate, title=title)
    fig.write_html(output_path, auto_open=False)


def multiple_boxplot(data: List[pd.DataFrame],
                     abscissa: List[str],
                     ordinate: str,
                     output_path: str,
                     title: str) -> None:
    """
    Draw a multiple boxplot graph.

    The type of graph is used to present series of repartition.

    :param data: the list of data to plot.
    :param abscissa: the names of the months.
    :param ordinate: the name of the axis that represents the graph's ordinate.
    :param output_path: the path to the HTML output file.
    :param title: the graph title.
    """
    fig = go.Figure(go.Box(y=data[0], name='{}'.format(abscissa[0][3:-4])))

    for i in range(1, len(abscissa)):
        fig.add_trace(go.Box(y=data[i], name='{}'.format(abscissa[i][3:-4])))

    fig.update_layout(title=title,
                      yaxis_title=ordinate)
    fig.write_html(output_path, auto_open=False)


def multiple_boxplot_seaborn(data: pd.DataFrame, abscissa: str, ordinate: str):
    """
    Draw a series of violin boxplots.

    :param data: a dataframe that contains the data used to generate the graph. Please note that this dataframe must
                contains at least 2 columns which names are given by the parameters "abscissa" and "ordinate".
    :param abscissa: the name of the column (within the dataframe "data") that contains the values to be printed on the
                     X-axis.
    :param ordinate: the name of the column (within the dataframe "data") that contains the values to be printed on the
                     Y-axis.
    """
    sns.violinplot(x=abscissa, y=ordinate, data=data)
    plt.show()
