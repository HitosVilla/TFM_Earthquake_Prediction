import unittest
from numpy.testing import assert_equal
import numpy as np
import pandas as pd

from models import supervised_models, time_series

class UnitTests(unittest.TestCase):

    def setUp(self):
        # Set up required configuration

        # Create logger
        #self.logger = logger_tools.get_logger(self.config, name)

        # Initialize Recommender
        #self.time_series = time_series.TimeSeries()
        pass

    # TEST READ DATA
    def test_read_data_ok(self):
        file_time_series = pd.read_csv('../data/1979_5.csv', parse_dates=True)

        # Create date column
        file_time_series['date'] = [d.date() for d in file_time_series['time']]

        # Validate there is no null values
        assert_equal(file_time_series.isnull().values.any(), True)

        # Create Time Series with maximum magnitude per day
        time_series = pd.DataFrame(file_time_series[(file_time_series['mag'] > 5)], columns=['date', 'mag']).groupby(['date']).max()

        # Recreate index
        time_series.reset_index(inplace=True)
        time_series.set_index(time_series['date'], inplace=True)
        del time_series["date"]
        time_series.sort_index(inplace=True)

        # Fill missing days with magnitude zero
        time_series = time_series.asfreq(freq='D', fill_value=0)

        # Validate number of days
        assert_equal(time_series.count(),14593)




    def tearDown(self):
        # Close database connection
        pass


if __name__ == '__main__':
    unittest.main()
