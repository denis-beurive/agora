from typing import Optional
import pandas as pd
import os
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import pyperclip


def set_graph_properties(abscissa_legend: Optional[str],
                         ordinate_legend: str,
                         output_path: str,
                         title: str):
    if abscissa_legend is not None:
        plt.xlabel(abscissa_legend)
    plt.ylabel(ordinate_legend)
    plt.title(title)
    directory = os.path.dirname(output_path)
    filename = os.path.basename(output_path)
    plt.rcParams['savefig.format'] = 'svg'
    plt.rcParams['savefig.directory'] = directory
    print("=" * 40)
    pyperclip.copy(filename)
    print("Directory location: {}".format(directory))
    print("Suggested file name: {} (just paste CTR-V - shout work)".format(filename))


def vbar(data: pd.DataFrame,
         abscissa: str,
         ordinate: str,
         legend: str,
         output_path: str,
         title: str) -> None:
    fig = go.Figure(go.Bar(x=data.get(abscissa), y=data.get(ordinate), name=legend, orientation='v'))
    fig.update_layout(title_text=title)
    fig.write_html(output_path, auto_open=False)


def hbar(data: pd.DataFrame,
         abscissa: str,
         ordinate: str,
         abscissa_legend: Optional[str],
         ordinate_legend: str,
         output_path: str,
         title: str) -> None:
    """
    Draw an horizontal HBAR.

    :param data: a dataframe that contains the data used to generate the graph. Please note that this dataframe must
                 contains at least 2 columns which names are given by the parameters "abscissa" and "ordinate".
    :param abscissa: the name of the column (within the dataframe "data") that contains the values to be printed on the
                     X-axis.
    :param ordinate: the name of the column (within the dataframe "data") that contains the values to be printed on the
                     Y-axis.
    :param abscissa_legend: the legend for the abscissa axis. May be None.
    :param ordinate_legend: the legend for the ordinate axis.
    :param output_path: the path to the output file.
    :param title: the graph title.
    """
    sns.barplot(x=abscissa, y=ordinate, data=data, orient='h')
    set_graph_properties(abscissa_legend,
                         ordinate_legend,
                         output_path,
                         title)
    plt.show()


def single_boxplot(data: pd.DataFrame,
                   abscissa: str,
                   ordinate: str,
                   abscissa_legend: Optional[str],
                   ordinate_legend: str,
                   output_path: str,
                   title: str) -> None:
    """
    Draw a boxplot graph.

    The type of graph is used to present a repartition.

    :param data: the data to plot.
    :param abscissa: the name of the column that contains the graph's abscissa.
    :param ordinate: the name of the column that contains the graph's ordinate.
    :param abscissa_legend: the legend for the abscissa axis.  May be None.
    :param ordinate_legend: the legend for the ordinate axis.
    :param output_path: the path to the output file.
    :param title: the graph title.
    """
    sns.violinplot(x=abscissa, y=ordinate, data=data)
    set_graph_properties(abscissa_legend,
                         ordinate_legend,
                         output_path,
                         title)
    plt.show()


def multiple_boxplot(data: pd.DataFrame,
                     abscissa: str,
                     ordinate: str,
                     abscissa_legend: Optional[str],
                     ordinate_legend: str,
                     output_path: str,
                     title: str):
    """
    Draw a series of violin boxplots.

    :param data: a dataframe that contains the data used to generate the graph. Please note that this dataframe must
                contains at least 2 columns which names are given by the parameters "abscissa" and "ordinate".
    :param abscissa: the name of the column (within the dataframe "data") that contains the values to be printed on the
                     X-axis.
    :param ordinate: the name of the column (within the dataframe "data") that contains the values to be printed on the
                     Y-axis.
    :param abscissa_legend: the legend for the abscissa axis. May be None.
    :param ordinate_legend: the legend for the ordinate axis.
    :param output_path: the path to the output file.
    :param title: the graph title.
    """
    sns.violinplot(x=abscissa, y=ordinate, data=data)
    set_graph_properties(abscissa_legend,
                         ordinate_legend,
                         output_path,
                         title)
    plt.show()
