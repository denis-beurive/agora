from typing import List, Dict, NewType, Optional, Union
from enum import Enum
from pprint import pprint
from collections import OrderedDict
import os


class SetLabels(Enum):
    SHORT = 'short',
    LONG = 'long',
    PATH = 'path'


class TitleLabels(Enum):
    TITLE = 'title',
    SET = 'set',
    LEVEL = 'level'


SetName = NewType('SetName', str)
SetDesc = NewType('SetDesc', List[Dict[SetLabels, Optional[str]]])
TitleDesc = NewType('TitleDesc', Dict[TitleLabels, Union[int, str]])


class Report:

    def __init__(self, in_path: str):
        self.output_path: str = in_path
        self._lines: List[Dict[TitleLabels, Optional[Union[str, SetName, int]]]] = []
        self._sets: OrderedDict[SetName, SetDesc] = OrderedDict()

    def add_title1(self, in_title: str,
                   in_set_name: Optional[SetName] = None) -> None:
        self._lines.append({
            TitleLabels.TITLE: in_title,
            TitleLabels.SET: in_set_name,
            TitleLabels.LEVEL: 1
        })
        if in_set_name not in self._sets:
            self._sets[SetName(in_set_name)] = SetDesc([])

    def add_title2(self, in_title: str,
                   in_set_name: Optional[SetName]) -> None:
        self._lines.append({
            TitleLabels.TITLE: in_title,
            TitleLabels.SET: in_set_name,
            TitleLabels.LEVEL: 2
        })
        if in_set_name not in self._sets:
            self._sets[SetName(in_set_name)] = SetDesc([])

    def add_document_to_set(self,
                            in_set: str,
                            in_short_description: str,
                            in_long_description: Optional[str],
                            in_path: str) -> None:
        if in_set not in self._sets:
            self._sets[SetName(in_set)] = SetDesc([])
        self._sets[SetName(in_set)].append({
            SetLabels.SHORT: in_short_description,
            SetLabels.LONG: in_long_description,
            SetLabels.PATH: in_path
        })

    def dump(self, root_path: str) -> None:
        with open(self.output_path, "w") as fd:
            for line in self._lines:
                fd.write("{} {}\n\n".format("#" * line[TitleLabels.LEVEL],
                                            line[TitleLabels.TITLE]))
                if self._sets[line[TitleLabels.SET]] is None:
                    continue
                for doc in self._sets[line[TitleLabels.SET]]:
                    path = doc[SetLabels.PATH]
                    prefix = os.path.commonprefix([path, root_path])
                    rel_path = path[len(prefix)+1:]
                    fd.write("* {}: [click here]({})\n".format(doc[SetLabels.SHORT],
                                                               rel_path))
                fd.write("\n")
