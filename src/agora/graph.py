import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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
