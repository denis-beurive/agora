from typing import Tuple, List, Dict, Any, Union
import json
import pandas as pd
import re
from numpy import ndarray
from .canvas import Canvas
from .canvas_exception import CanvasException
from .types import AbscissaName, AbscissaValue, OrdinateName, OrdinateValue, ColorName, ParamName, WidthValue


class HBarMulti(Canvas):

    _TEMPLATE = """
    __TRACES__; 
    var data = __DATA__; 
    var layout = __LAYOUT__; 
    
    Plotly.newPlot('myDiv', data, layout);
    """

    def __init__(self,
                 in_data: pd.DataFrame,
                 params: List[Dict[ParamName, Union[int, List[ColorName]]]]):
        """
        Create a new Horizontal Multi Bar graph.

        :param in_data: data to plot. Structure:
        {'ordinate': ["a", "b", "c", "d", "e"],
               'x1': [10, 20, 30, 40, 50],
               'x2': [11, 12, 13, 14, 15]}
        :param params: parameters. This is a list of dictionaries which keys are:
        - "colors"
        - "width"
        """
        items: List[Tuple] = list(in_data.items())
        if len(items) < 2:
            raise CanvasException("Unexpected DataFrame: incorrect dimension ({})".format(len(items)))
        if (len(items) - 1) != len(params):
            raise CanvasException("Unexpected number of parameters ({}, expected {})".format(len(params),
                                                                                             len(items)-1))

        self._params = params
        self._ordinate: OrdinateName = items[0][0]
        v: ndarray = items[0][1].values
        self._ordinate_values: List[OrdinateValue] = v.tolist()

        self._abscissa: Dict[AbscissaName, List[AbscissaValue]] = {}
        for item in items[1:]:
            name: OrdinateName = item[0]
            v: ndarray = item[1].values
            self._abscissa[AbscissaName(name)] = v.tolist()

    @property
    def ordinate(self) -> OrdinateName:
        return self._ordinate

    @property
    def ordinate_values(self) -> List[AbscissaValue]:
        return self._ordinate_values

    @property
    def abscissa(self) -> Dict[AbscissaName, List[AbscissaValue]]:
        return self._abscissa

    @property
    def params(self) -> List[Dict[ParamName, Union[WidthValue, List[ColorName]]]]:
        return self._params

    def _js(self) -> str:
        variables: List[Dict[str, Any]] = []
        n: int = 0
        for name, graph in self._abscissa.items():
            v = {
                'x': graph,
                'y': self.ordinate_values,
                'name': name,
                'orientation': 'h',
                'marker': {
                    'color': self._params[n][ParamName('color')],
                    'width': self._params[n][ParamName('width')]
                },
                'type': 'bar'
            }
            n += 1
            variables.append(v)
        n: int = 0
        text: List[str] = []
        for variable in variables:
            text.append('var trace{} = {}'.format(n, json.dumps(variable)))
            n += 1
        traces = '; '.join(text)
        data = '[' + ', '.join(["trace{}".format(n) for n in range(len(variables))]) + ']'
        layout = json.dumps({
            'title': 'Colored Bar Chart',
            'barmode': 'stack'
        })
        js = re.sub('__TRACES__', traces, HBarMulti._TEMPLATE)
        js = re.sub('__DATA__', data, js)
        js = re.sub('__LAYOUT__', layout, js)
        return js
