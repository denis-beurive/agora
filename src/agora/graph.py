from typing import Optional
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pyperclip


AUTO_SAVE: bool = True


def set_graph_properties(abscissa_legend: Optional[str],
                         ordinate_legend: Optional[str],
                         output_path: str,
                         title: str):
    figure(figsize=(26, 16), dpi=80)
    if abscissa_legend is not None:
        plt.xlabel(abscissa_legend)
    if ordinate_legend is not None:
        plt.ylabel(ordinate_legend)
    plt.title(title)
    plt.rcParams['savefig.format'] = 'svg'
    plt.rcParams['figure.subplot.left'] = 0.5
    if AUTO_SAVE:
        print("Create file {}".format(output_path))
    else:
        directory = os.path.dirname(output_path)
        filename = os.path.basename(output_path)
        plt.rcParams['savefig.directory'] = directory
        pyperclip.copy(filename)
        print("=" * 40)
        print("Directory location: {}".format(directory))
        print("Suggested file name: {} (just paste CTR-V - should work)".format(filename))


def vbar(data: pd.DataFrame,
         abscissa: str,
         ordinate: str,
         legend: str,
         output_path: str,
         title: str) -> None:
    set_graph_properties(None,
                         None,
                         output_path,
                         title)
    sns.barplot(x=abscissa, y=ordinate, data=data, orient='v')
    if AUTO_SAVE:
        plt.savefig(output_path)
    else:
        plt.show()
    plt.close('all')


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
    set_graph_properties(abscissa_legend,
                         ordinate_legend,
                         output_path,
                         title)
    sns.barplot(x=abscissa, y=ordinate, data=data, orient='h')
    if AUTO_SAVE:
        plt.savefig(output_path)
    else:
        plt.show()
    plt.close('all')


def single_boxplot(data: pd.DataFrame,
                   abscissa: str,
                   ordinate: str,
                   abscissa_legend: Optional[str],
                   ordinate_legend: Optional[str],
                   output_path: str,
                   title: str) -> None:
    """
    Draw a boxplot graph.

    The type of graph is used to present a repartition.

    :param data: the data to plot.
    :param abscissa: the name of the column that contains the graph's abscissa.
    :param ordinate: the name of the column that contains the graph's ordinate.
    :param abscissa_legend: the legend for the abscissa axis. May be None.
    :param ordinate_legend: the legend for the ordinate axis. May be None.
    :param output_path: the path to the output file.
    :param title: the graph title.
    """
    set_graph_properties(abscissa_legend,
                         ordinate_legend,
                         output_path,
                         title)
    sns.violinplot(x=abscissa, y=ordinate, data=data)
    if AUTO_SAVE:
        plt.savefig(output_path)
    else:
        plt.show()
    plt.close('all')


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
    set_graph_properties(abscissa_legend,
                         ordinate_legend,
                         output_path,
                         title)
    sns.violinplot(x=abscissa, y=ordinate, data=data)
    if AUTO_SAVE:
        plt.savefig(output_path)
    else:
        plt.show()
    plt.close('all')
