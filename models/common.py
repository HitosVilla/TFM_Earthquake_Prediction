import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import logging


def get_logger(component):
    """
    Write log
    :param component: name of the component who call this function to write log
    :return: Logger
    """

    log_formatter = logging.Formatter("%(asctime)s ["+component+"] [%(levelname)s]  %(message)s")
    logger = logging.getLogger(component)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)
    logger.setLevel('DEBUG')

    return logger


def plot(x, y, y_label, title):
    """
    Simple plot with title and y:label
    :param x: values of x axis
    :param y: values of y axis
    :param y_label: label to display at y axis
    :param title: plot title
    :return: a plot is displayed after calling this method
    """

    plt.figure(figsize=(18, 10))
    plt.subplot(211)
    plt.ylabel(y_label)
    plt.suptitle(title, fontsize=20)
    plt.plot(x, y)


def plot_time_series_prediction(n_periods, title, forecast, conf_int, mag_ym):
    """
    plot historical data and forecast of time series of maximun magnitude per month/year
    :param n_periods: number of periods of forecast to show.
    :param title: plot title
    :param forecast: predicted data
    :param conf_int: interval of confidence
    :param mag_ym: historical data of time series of maximun magnitude per month/year
    :return: a plot is displayed after calling this method
    """
    # Plot configuration
    x_years = pd.date_range(start='1/1/1970', periods=len(mag_ym.index) + n_periods, freq='MS')
    plt.figure(figsize=(18, 10))
    plt.subplot(211)
    plt.suptitle(title, fontsize=20)
    plt.xlabel("Year")
    plt.ylabel("Magnitude")

    # one line per historical data
    plt.plot(x_years[:-n_periods], mag_ym['mag'], alpha=0.75)

    # other line for forecast
    plt.plot(x_years[-n_periods:], forecast, alpha=0.75)  # Forecasts

    # Fill interval of confidence for forecast
    plt.fill_between(x_years[-n_periods:], conf_int[:, 0], conf_int[:, 1], alpha=0.1, color='b')


def plot_time_series_with_big_earthquakes(title_figure, y_label, column_x,
                                          data_frame, column_y, column_lines, data_frame_bar):
    """
    In the same figure are two plots:
            :param title_figure: figure title
            :param y_label: figure y label
            :param column_x: x values = column in sismos used to group data_frame  ('year' or YM')

        1. one line per value in column_lines
            :param data_frame: data frame to be plotted
            :param column_y: y value = column we want to analyze ('magcount' , 'count')
            :param column_lines: types of column_y ('magtype', 'mag_int')

        2. one vertical bar per big earthquake
            :param data_frame_bar: sismos dataframe

    :return: a plot is displayed after calling this method
    """

    # Values X axis
    x = data_frame[column_x].unique()

    # Create a color palette
    palette = plt.get_cmap('Set1')

    # Set plot figure size
    plt.figure(figsize=(18, 10))
    plt.subplot(211)
    plt.ylabel(y_label)
    plt.suptitle(title_figure, fontsize=20)

    for i, column_line in enumerate(data_frame[column_lines].unique()):
        # Values Y axis
        y = np.array(data_frame[data_frame[column_lines] == column_line][column_y])
        # One line per magnitude type
        plt.plot(x, y, color=palette(i), label=column_line)

    # one bar per greatest earthquakes
    x_bar_arr = data_frame_bar[column_x].unique()

    for x_bar in x_bar_arr:
        plt.axvline(x=x_bar, color="black", ls='-.', lw=1)

    plt.legend(loc='best')


def plot_regression_with_big_earthquake(title_figure, y_label, column_x,
                                        data_frame, column_y, column_lines, data_frame_bar,
                                        big_earthquake = True):
    """
    In the same figure are two plots:
            :param title_figure: figure title
            :param y_label: figure y label
            :param column_x: x values = column in sismos used to group data_frame  ('year' or YM')
            :param big_earthquake = boolean to plot one line per earthqueake bigger than 7

        1. one line per value in column_lines
            :param data_frame: data frame to be plotted
            :param column_y: y value = column we want to analyze ('magcount' , 'count')
            :param column_lines: types of column_y ('magtype', 'mag_int')

        2. one vertical bar per big earthquake
            :param data_frame_bar: sismos dataframe

    :return: a plot is displayed after calling this method
    """

    # Values X axis
    x = list(data_frame[column_x])

    # Create a color palette
    palette = plt.get_cmap('Set1')

    # Set plot figure size
    plt.figure(figsize=(18, 10))
    plt.subplot(211)
    plt.ylabel(y_label)
    plt.suptitle(title_figure, fontsize=20)

    for i, column_line in enumerate(list(data_frame[column_lines])):
        # Values Y axis
        y = np.array(data_frame[column_line])
        # One line per magnitude
        plt.plot(x, y, color=palette(i), label=column_line)

    # one bar per greatest earthquakes
    x_bar_arr = data_frame_bar[column_x].unique()

    if big_earthquake:
        for x_bar in x_bar_arr:
            plt.axvline(x=x_bar, color="black", ls='-.', lw=1)

    plt.legend(loc='best')


def plot_rolling_stadistics(data_frame):
    """
    Plot mean and standard variation rolling stadistics of data frame
    :param data_frame:
    :return: a plot is displayed after calling this method
    """
    # Determining rolling statistics
    window_size = 24
    # Mean
    rolling_mean = data_frame.rolling(window=window_size, center=True).mean()
    # Standard Variation
    rolling_std = data_frame.rolling(window=window_size, center=True).std()

    # Plotting rolling statistics
    plt.figure(figsize=(18, 5))
    plt.title('Rolling  Mean & Standard Deviation')
    orig = plt.plot(data_frame, color='blue', label='Original')
    mean = plt.plot(rolling_mean, color='red', label='Mean')
    st = plt.plot(rolling_std, color='black', label='Std')
    plt.legend(loc='best')