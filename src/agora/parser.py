from typing import Iterable
import csv
from .record import Record


class Parser:

    def __init__(self, in_input_path: str):
        self._path: str = in_input_path

    def run(self) -> Iterable[Record]:
        with open(self._path, 'r') as fd:
            reader = csv.reader(fd, delimiter=',', quotechar='"', dialect='excel')
            header_passed: bool = False
            for line in reader:
                if not header_passed:
                    header_passed = True
                    continue
                yield Record(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8])
