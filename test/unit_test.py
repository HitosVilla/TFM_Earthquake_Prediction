def warn(*args, **kwargs):
    pass


import warnings
warnings.warn = warn

import unittest
from numpy.testing import assert_equal
import numpy as np

from models import common, supervised_models, read_data

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
        self.sismos, self.all_months = read_data.read_data_common('../data/')
        self.logger.info('Read Common Data. Done')
        self.frequency_year, self.time_series_magnitude = read_data.read_data_time_series('../data/')
        self.logger.info('Read Time Series Data. Done')
        self.features_classification, self.label_classification = read_data.read_data_classification('../data/')
        self.logger.info('Read classification Data. Done\n')
        # except Exception as err:
        #    self.logger.error("Error {}".format(err))

    def test_read_Data_common(self):
        self.logger.info('test_read_Data_common')
        assert_equal(len(self.sismos.columns), 15)
        assert_equal(len(self.all_months.columns), 1)

    def test_read_Data_time_series(self):
        self.logger.info('test_read_Data_time_series')
        assert_equal(len(self.frequency_year.columns), 4)
        assert_equal(len(self.time_series_magnitude.columns), 1)

    def test_read_Data_classification(self):
        self.logger.info('test_read_Data_classification')
        assert_equal(len(self.features_classification.columns), 10)
        assert_equal(len(self.label_classification.unique()), 2)

    def test_best_classification(self):
        class_models = {'LogisticRegression':     (LogisticRegression(),     {}),
                        'KNeighborsClassifier':   (KNeighborsClassifier(),   {'n_neighbors': np.arange(2, 10)}),
                        'DecisionTreeClassifier': (DecisionTreeClassifier(), {'min_samples_leaf': np.arange(1, 3),
                                                                              'max_depth': np.arange(1, 3)}),
                        'SVC':                    (SVC(kernel="linear"),     {'C': np.arange(1, 3)}),
                        'RandomForestClassifier': (RandomForestClassifier(), {'n_estimators': np.arange(1, 3),
                                                                              'max_depth': np.arange(1, 3),
                                                                              'min_samples_leaf': np.arange(1, 3)})}

        supervised_test = supervised_models.Supervised(self.features_classification.drop('YM', axis=1),
                                                       self.label_classification)
        supervised_test.evaluate_best_model(class_models)

    def test_plot(self):

        common.plot_time_series_with_big_earthquakes('Frequency per month/year split by magnitude', '# per month/year',
                                                     'YM', self.features_classification, 'count',
                                                     'mag_int', self.sismos)

    def tearDown(self):
        # Close objects
        pass


if __name__ == '__main__':
    unittest.main()
