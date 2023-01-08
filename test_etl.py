import unittest
import pandas as pd
import pandas.testing as pd_testing
from core import *

file = 'test_data/test2_csv.txt'
skiprows = 11
separator = '\t'
location_of_allels_cols = (2,3,4,5)

class TestStrFind(unittest.TestCase):

    def test_source_file_load(self):

        test_data = pd.read_csv(file, skiprows=skiprows, sep=separator)
        pd_testing.assert_frame_equal(source_file_load(file), test_data)

    def test_get_info_about_file(self):

        test_data = file

        dict = {"separator": separator, "skiprows":skiprows, "location_of_allels_cols":location_of_allels_cols}
        file_info_getter_dict = FileInfoGetter(test_data).build_dict()
        print(file_info_getter_dict)
        self.assertDictEqual(dict, file_info_getter_dict)

if __name__ == "__main__":
    unittest.main()