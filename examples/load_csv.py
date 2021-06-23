from typing import Pattern, Match, List
import re
import os
import pandas as pd


# Set options for Pandas.
pd.set_option("display.max_rows", None, "display.max_columns", None)


def csv_loader(path: str) -> pd.DataFrame:
    """
    Load data from CSV file.

    This function skips the rows that contain empty vendor names.

    :param path: path to the CSV file to load.
    :return: the loaded data.
    """

    def regex_filter(vendor_name: str):
        """
        This function is used to avoid the selection of non-significant vendor names.

        :param vendor_name: a vendor name.
        :return: if the given name is significant, then the function returns the value True.
                 Otherwise, it returns the value False.
        """
        filter_pattern: Pattern = re.compile('^\\s*\\n')
        if vendor_name:
            m: Match = re.search(filter_pattern, vendor_name)
            return m is None
        else:
            return True

    data: pd.DataFrame = pd.read_csv(filepath_or_buffer=path,
                                     sep=',',
                                     quotechar='"',
                                     dialect='excel',
                                     dtype={
                                         'col1': str,
                                         'col2': str,
                                         'col3': str
                                     })
    return data.loc[data['col1'].apply(regex_filter)]


SCRIP_DIR = os.path.dirname(os.path.realpath(__file__))
"""Path to the directory that contains *this* (Python) script."""

CSV_FILE1 = os.path.join(SCRIP_DIR, "file1.csv")
CSV_FILE2 = os.path.join(SCRIP_DIR, "file2.csv")
CSV_FILE3 = os.path.join(SCRIP_DIR, "file3.csv")

dataframes: List[pd.DataFrame] = []
for path in [CSV_FILE1, CSV_FILE2, CSV_FILE3]:
    dataframes.append(csv_loader(path))

print('Number of loaded dataframes: {}\n'.format(len(dataframes)))
for dataframe in dataframes:
    print(str(dataframe) + "\n")

