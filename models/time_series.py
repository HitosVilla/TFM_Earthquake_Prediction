import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from models import common
# from statsmodels.tsa.arima_model import ARIMA


class TimeSeries(object):
    """ Base class to evaluate a models """

    def __init__(self, frequency_year, time_series_magnitude):
        # Create logger
        self.logger = common.get_logger('TiSe')

        # Initialize self variables for data
        self.frequency_year = frequency_year
        self.time_series_magnitude = time_series_magnitude

    def decomposition(self):

        to_decompose = self.time_series_magnitude

        decomposition = seasonal_decompose(to_decompose)
        trend = decomposition.trend.fillna(0)
        seasonal = decomposition.seasonal.fillna(0)
        residual = decomposition.resid.fillna(0)

        plt.figure(figsize=(18, 7))
        plt.subplot(411)
        plt.plot(to_decompose, label='Original')
        plt.legend(loc='best')
        plt.subplot(412)
        plt.plot(trend, label='Trend')
        plt.legend(loc='best')
        plt.subplot(413)
        plt.plot(seasonal, label='Seasonality')
        plt.legend(loc='best')
        plt.subplot(414)
        plt.plot(residual, label='Residual')
        plt.legend(loc='best')

        return True

    def dickey_fuller_test(self):

        text = 'Dickey-Fuller Test: Magnitude per year \n\n'

        result = adfuller(self.time_series_magnitude['mag'].dropna(), autolag='AIC')

        labels = ['ADF test statistic', 'p-value', '# lags used', '# observations']
        out = pd.Series(result[0:4], index=labels)

        for key, val in result[4].items():
            out[f'critical value ({key})'] = val

        text = text + out.to_string()  # .to_string() removes the line "dtype: float64"

        if result[1] <= 0.05:
            text = text + '\n\nStrong evidence against the null hypothesis'
            text = text + '\nReject the null hypothesis'
            text = text + '\nData has no unit root and is stationary'
        else:
            text = text + '\n\nWeak evidence against the null hypothesis'
            text = text + '\nFail to reject the null hypothesis'
            text = text + '\nData has a unit root and is non-stationary'

        return text

    def arima(self):

        '''plot_acf(self.time_serie)
        plot_pacf(self.time_serie)
        model = ARIMA(history, order=(5, 1, 0))
        model_fit = model.fit()
        output = model_fit.forecast()
        yhat = output[0]'''
        pass