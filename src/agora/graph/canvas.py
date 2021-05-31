from typing import Pattern, Match
from abc import ABC, abstractmethod
import re


class Canvas(ABC):

    _TEMPLATE = """
<html>
    <head>
        <script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
    </head>
    
    <body>
        <div id='myDiv'>
        <script type="text/javascript">
            __JS__                
        </script>
    </body>
</html>"""

    _PATTERN: Pattern = re.compile('__JS__')

    @abstractmethod
    def _js(self) -> str:
        """
        Return the JavaScript code to insert into the HTML template.

        :return: the JavaScript code to insert into the HTML template.
        """

    def draw(self) -> str:
        """
        Return the HTML code that represents the graph.

        :return: the HTML code that represents the graph.
        """
        return re.sub('__JS__', self._js(), Canvas._TEMPLATE)
