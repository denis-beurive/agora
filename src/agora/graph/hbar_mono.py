from typing import Tuple, List, Any
import pandas as pd
import json
import re
from numpy import ndarray
from .canvas import Canvas
from .canvas_exception import CanvasException


class HBarMono(Canvas):

    _TEMPLATE = """
    var data=__DATA__; Plotly.newPlot('myDiv', data);
    """

    def __init__(self, in_data: pd.DataFrame):
        items: List[Tuple] = list(in_data.items())
        if len(items) != 2:
            raise CanvasException("Unexpected DataFrame: incorrect dimension ({})".format(len(items)))

        self._ordinate: str = items[0][0]
        v: ndarray = items[0][1].values
        self._ordinate_values: List[Any] = v.tolist()

        self._abscissa: str = items[1][0]
        v: ndarray = items[1][1].values
        self._abscissa_values: List[Any] = v.tolist()

    @property
    def abscissa(self) -> str:
        return self._abscissa

    @property
    def ordinate(self) -> str:
        return self._ordinate

    @property
    def abscissa_values(self) -> List[Any]:
        return self._abscissa_values

    @property
    def ordinate_values(self) -> List[Any]:
        return self._ordinate_values

    def _js(self) -> str:
        data = [{
            'type': 'bar',
            'x': self._abscissa_values,
            'y': self._ordinate_values,
            'orientation': 'h'
        }]
        return re.sub('__DATA__', json.dumps(data), HBarMono._TEMPLATE)
