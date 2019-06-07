import matplotlib.pyplot as plt
import numpy as np
import logging


def get_logger(component):
    """
    Write log
    :param component:
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
    # Set plot figure size
    plt.figure(figsize=(18, 10))
    plt.subplot(211)
    plt.ylabel(y_label)
    plt.suptitle(title, fontsize=20)
    plt.plot(x, y)


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

    :return: Nothing to return, a figure is drawn
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
    x_bar_arr = data_frame_bar[data_frame_bar['mag'] >= 7][column_x].unique()

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

    :return: Nothing to return, a figure is drawn
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
    x_bar_arr = data_frame_bar[data_frame_bar['mag'] >= 7][column_x].unique()

    if big_earthquake:
        for x_bar in x_bar_arr:
            plt.axvline(x=x_bar, color="black", ls='-.', lw=1)

    plt.legend(loc='best')


def plot_rolling_stadistics(data_frame):
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