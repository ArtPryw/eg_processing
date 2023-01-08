import pandas as pd
import csv
from collections import Counter
from errors import *

class FileInfoGetter():

    def __init__(self, file_path):
        self.file_path = file_path

    def __check_separator(self):
        sniffer = csv.Sniffer()
        with open(self.file_path, 'r') as f:
            found_separators = []
            counter = 0
            while counter != 15:
                line = f.readline()
                try:
                    dialect = sniffer.sniff(line)
                    found_separators.extend(dialect.delimiter)
                except:
                    pass
                counter +=1
        counter = Counter(found_separators)
        separator = counter.most_common()
        separator = separator[0][0]

        return separator

    def __check_skiprow(self):
        separator = self.__check_separator()
        skiprows = 0
        with open(self.file_path, 'r') as f:
            while True:
                line = f.readline().split(separator)
                splitted_line = list(filter(lambda x: len(x.strip()) == 1, line))
                if len(splitted_line) >= 2:
                    break
                else:
                    if skiprows > 10:
                        break
                    else:
                        skiprows += 1
            return skiprows

    def build_dict(self):

        separator = self.__check_separator()
        skiprows = self.__check_skiprow()
        dict = {"separator": separator, "skiprows": skiprows}
        return dict

def source_file_load(file):
    source_file = pd.read_csv(file, skiprows = 10)

    return source_file