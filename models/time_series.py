from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
# from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
# from statsmodels.tsa.arima_model import ARIMA


class TimeSeries(object):
    """ Base class to evaluate a models """

    def __init__(self, time_serie):

        self.time_serie = time_serie

    def adfuller(self):

        fuller = adfuller(self.time_serie, autolag='AIC')

        test_statistic = fuller[0]
        p_value = fuller[1]
        lag = fuller[2]
        num_observations = fuller[3]

        critical_value = {}
        for key, value in fuller[4].items():
            critical_value[key] = value

        return test_statistic, p_value, lag, num_observations, critical_value

    def decomposition(self):
        self.time_serie = self.time_serie.set_index('Month')
        decomposition = seasonal_decompose(self.time_serie)
        trend = decomposition.trend
        seasonal = decomposition.seasonal
        residual = decomposition.resid

        return trend, seasonal, residual

    def arima(self):

        '''plot_acf(self.time_serie)
        plot_pacf(self.time_serie)
        model = ARIMA(history, order=(5, 1, 0))
        model_fit = model.fit()
        output = model_fit.forecast()
        yhat = output[0]'''
        pass