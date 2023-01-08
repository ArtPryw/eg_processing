import unittest
import pandas as pd
import pandas.testing as pd_testing
from core import *


skiprows = 10
class TestStrFind(unittest.TestCase):

    def test_source_file_load(self):

        test_data = pd.read_csv('test_data/test_csv.csv', skiprows = skiprows)
        pd_testing.assert_frame_equal(source_file_load('test_data/test_csv.csv'), test_data)

    def test_get_info_about_file(self):

        test_data = 'test_data/test_csv.csv'

        dict = {"separator": ",", "skiprows":10}
        file_info_getter_dict = FileInfoGetter(test_data).build_dict()
        print(file_info_getter_dict)
        self.assertDictEqual(dict, file_info_getter_dict)

if __name__ == "__main__":
    unittest.main()