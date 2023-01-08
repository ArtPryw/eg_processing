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
        if separator == '	':
            separator = '\t'
        print(f"Separator = {separator}")
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
            print(f"Skiprows = {skiprows}")
            return skiprows

    def __location_of_allels_cols(self):
        separator = self.__check_separator()
        skiprows = self.__check_skiprow()

        df = pd.read_csv(self.file_path, skiprows=skiprows, nrows=10, sep=separator)
        translated_allels = ['B']
        not_translated_allels = ['A', 'C', 'T', 'G']

        translated_alleles_col_postion_list = []
        not_translated_alleles_col_postion_list = []
        for i in range(len(df.columns)):
            col_to_list = df.iloc[:, i].tolist()
            if any(element in translated_allels for element in col_to_list):
                translated_alleles_col_postion_list.append(i)
        if len(translated_alleles_col_postion_list) == 0:
            for i in range(len(df.columns)):
                col_to_list = df.iloc[:, i].tolist()
                if any(element in not_translated_allels for element in col_to_list):
                    not_translated_alleles_col_postion_list.append(i)
            result = not_translated_alleles_col_postion_list
        else:
            result = translated_alleles_col_postion_list

        return tuple(result)



    def build_dict(self):

        separator = self.__check_separator()
        skiprows = self.__check_skiprow()
        location_of_allels_cols = self.__location_of_allels_cols()
        dict = {"separator": separator, "skiprows": skiprows, "location_of_allels_cols": location_of_allels_cols}
        return dict

def source_file_load(file):

    info_getter = FileInfoGetter(file)
    df_information = info_getter.build_dict()

    source_file = pd.read_csv(file, skiprows=df_information['skiprows'], sep=df_information['separator'])

    return source_file