def warn(*args, **kwargs):
    pass


import warnings
warnings.warn = warn

import unittest
from numpy.testing import assert_equal
import numpy as np

from models import common, read_data, supervised_models, time_series

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


class UnitTests(unittest.TestCase):

    def setUp(self):
        self.file_name = '../data/1979_200kmSantiago.csv'
        # Create logger
        self.logger = common.get_logger('Test')
        self.logger.info('******** Initialize unit test ********')

        # Load earthquake data
        # try:
        self.sismos, self.all_months = read_data.read_data_common('../data/earthquake.csv')
        self.logger.info('Read Common Data. Done')

        # Read Time Series
        self.frequency_year, self.time_series_magnitude = read_data.read_data_time_series('../data/earthquake.csv')
        self.logger.info('Read Time Series Data. Done')
        self.time_series_object = time_series.TimeSeries(self.frequency_year, self.time_series_magnitude)

        # Read Classification
        self.features_classification, self.label_classification = \
            read_data.read_data_classification('../data/earthquake.csv', '../data/Temperature.csv')
        self.logger.info('Read classification Data. Done\n')

        self.supervised_test = supervised_models.Supervised(self.features_classification.drop('YM', axis=1),
                                                            self.label_classification)
        # except Exception as err:
        #    self.logger.error("Error {}".format(err))

    def test_read_Data_common(self):

        assert_equal(len(self.sismos.columns), 14)
        assert_equal(len(self.all_months.columns), 1)
        self.logger.info('test_read_Data_common. Done\n')

    def test_read_Data_time_series(self):

        assert_equal(len(self.frequency_year.columns), 4)
        assert_equal(len(self.time_series_magnitude.columns), 1)
        self.logger.info('test_read_Data_time_series. Done\n')

    def test_read_Data_classification(self):

        assert_equal(len(self.features_classification.columns), 10)
        assert_equal(len(self.label_classification.unique()), 2)
        self.logger.info('test_read_Data_classification. Done\n')

    def test_decomposition(self):

        test_decomposition = self.time_series_object.decomposition()
        self.logger.info('test_decomposition. Done\n')
        assert_equal(test_decomposition, True)

    def test_dickey_fuller_test(self):

        test_dickey_fuller = self.time_series_object.dickey_fuller_test()
        self.logger.info('test_decomposition. Done\n')
        assert_equal(test_dickey_fuller, True)

    def test_best_classification(self):
        class_models = {'LogisticRegression':     (LogisticRegression(),     {}),
                        'KNeighborsClassifier':   (KNeighborsClassifier(),   {'n_neighbors': np.arange(2, 10)}),
                        'DecisionTreeClassifier': (DecisionTreeClassifier(), {'min_samples_leaf': np.arange(1, 3),
                                                                              'max_depth': np.arange(1, 3)}),
                        'SVC':                    (SVC(kernel="linear"),     {'C': np.arange(1, 3)}),
                        'RandomForestClassifier': (RandomForestClassifier(), {'n_estimators': np.arange(1, 3),
                                                                              'max_depth': np.arange(1, 3),
                                                                              'min_samples_leaf': np.arange(1, 3)})}
        self.supervised_test.evaluate_best_model(class_models)

    def test_plot_data_frames(self):

        data_frames_colors = [[self.time_series_magnitude, 'green'],[self.time_series_magnitude, 'blue']]
        common.plot_data_frames(data_frames_colors, 'test', 'test')


    def test_plot_regression_with_big_earthquake(self):

        common.plot_regression_with_big_earthquake('Frequency per month/year split by magnitude', '# per month/year',
                                                   'YM', self.features_classification, '', ['6', '7', '8'],
                                                   self.sismos, False)
        self.logger.info('plot_regression_with_big_earthquake. Done\n')

    def test_plot_rolling_statistics(self):

        common.plot_rolling_stadistics(self.time_series_magnitude)
        self.logger.info('test_plot_rolling_statistics. Done\n')

    def tearDown(self):
        # Close objects
        pass


if __name__ == '__main__':
    unittest.main()
