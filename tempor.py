import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from xbbg import blp

color_list = [
    (0, 0, 0),  # dummy color
    (130, 110, 70),  # Brown
    (168, 154, 126),  # other brown
    (205, 197, 181),  # ..
    (204, 47, 44),  #
    (68, 84, 106),  #
    (85, 117, 65),  #
    (131, 69, 100),  #
    (173, 185, 202),  #
    (236, 170, 168),  #
    (112, 48, 160),  #
    (128, 128, 0),  # Olive
    (0, 128, 0),  # Green
    (128, 0, 128),  # Purple
    (0, 128, 128),  # Teal
    (0, 0, 128)  # Navy
]


def convert_to_matplotlib_colors(mpl_colors=[]):
    for c in color_list:
        color = []
        for number in c:
            color.append(number / 255)
        mpl_colors.append(tuple(color))
    return mpl_colors


MPL_COLORS = convert_to_matplotlib_colors()


class BarChart:
    """
    This is a parent class for Barchart. There are calculations and some general values that can be used for both,
    vertical and horizontal barchart. "self" represent an instance of the class
    """

    def __init__(self, df, plot_type, sort, y_axis, source, name, legend_labels):
        # So most of the chart layout values are the same for both types of graph and they are calculated below
        self.n_tickers = len(df)  # number of tickers
        self.n_fields = len(df.columns)  # number of fields
        self.size = round(1 / self.n_fields, 2)  # size of a single bar
        self.gap = self.size * 1  # gap between groups, might need to change it based on number of tickers
        self.bar_group_position = np.zeros(self.n_tickers)  # initialize empty list for bar groups position
        self.initial_location = self.bar_group_position  # save initial bar location
        for i in range(self.n_tickers):  # calculates bar groups position
            self.bar_group_position[i] = round((self.size * self.n_fields + self.gap) * i, 2)

        # x label position in the middle of the group
        self.label_position = self.bar_group_position + (self.size * self.n_fields) / 2

        self.fig, self.ax = plt.subplots(figsize=(12, 8))  # initialize matplotlib figure

        # Put Source and Date at the bottom right corner
        self.t = plt.figtext(0.86, 0.02, f'Source: {source} Date: {datetime.today().date().strftime("%d/%m/%Y")}',
                             ha='center',
                             fontsize=6)
        plt.title(name, loc='left')  # set chat name

        # If legend_labels is nothing, use default field values, which are column names
        if legend_labels[0] == '':
            self.legend_labels = df.columns
        else:
            self.legend_labels = legend_labels

        # Figure borders
        self.ax.spines[['top', 'right', 'left']].set_visible(False)

        # Where to show y-axis, default l
        if y_axis == 'r' or y_axis == 'R': self.ax.tick_params(labelright=True, right=True, labelleft=False, left=False)
        if y_axis == 'b' or y_axis == 'B': self.ax.tick_params(labelright=True, right=True)

        # Sort if needed, sorts by first field values
        if sort == 'a' or sort == 'A':
            df.sort_values(by=df.columns[0], axis=0, inplace=True, ascending=True)
        elif sort == 'd' or sort == 'D':
            df.sort_values(by=df.columns[0], axis=0, inplace=True, ascending=False)
        self.labels = df.index  # Ticker names in order

        # Stacked BarChart Settings
        if plot_type == 's' or plot_type == 'S':
            self.align = 'center'
            self.y_offset = np.zeros(self.n_tickers)  # distance at which next bar should be placed if stacked plot
        else:
            self.y_offset = None
            self.align = 'edge'


class HorizontalBarChart(BarChart):
    def __init__(self, df, plot_type, sort, y_axis, source, name, legend_labels, display_value):
        super().__init__(df, plot_type, sort, y_axis, source, name, legend_labels)

        y_locations = self.initial_location
        plt.grid(b=True, which='major', axis='x', color='grey', alpha=.5)
        for i, col in enumerate(df.columns, 1):
            self.ax.barh(y_locations,
                         df[col], height=self.size, label=col, align=self.align, left=self.y_offset,
                         color=MPL_COLORS[i], edgecolor='white', linewidth=1)
            if plot_type == 's':
                self.y_offset += df[col]
            else:
                y_locations = self.bar_group_position + self.size * i

        # self.ax.legend(loc='lower left', bbox_to_anchor=(0, -0.14), ncol=5, frameon=False)
        if display_value == 'o' or display_value == 'O':
            for container in self.ax.containers: self.ax.bar_label(container, fmt='%.1f', padding=3)
        if plot_type == 's':
            plt.yticks(self.initial_location, self.labels)
        else:
            plt.yticks(self.label_position, self.labels)
        self.ax.legend(loc='lower left', bbox_to_anchor=(0, -0.14), ncol=5, frameon=False, labels=self.legend_labels)
        self.fig.savefig('charts/211021/' + name + '.png', bbox_inches='tight', transparent=True)


class VerticalBarChart(BarChart):
    def __init__(self, df, plot_type, sort, y_axis, source, name, legend_labels, display_value):
        super().__init__(df, plot_type, sort, y_axis, source, name, legend_labels)

        x_location = self.initial_location
        plt.grid(b=True, which='major', axis='y', color='grey', alpha=.5)
        for i, col in enumerate(df.columns, 1):
            self.ax.bar(x_location, df[col], width=self.size, label=col, align=self.align, bottom=self.y_offset,
                        color=MPL_COLORS[i], edgecolor='white', linewidth=1)
            if plot_type == 's':
                self.y_offset += df[col]
            else:
                x_location = self.bar_group_position + self.size * i

        if self.n_tickers > 13:  # if more than tickers -> rotate labels
            rotation = 90
            self.ax.legend(loc='lower left', ncol=5, bbox_to_anchor=(0, -0.4), frameon=False, labels=self.legend_labels)
            self.t.set_position((0.86, -0.15))
        else:  # less than tickers -> break them into lines
            self.labels = self.labels.str.replace(' ', '\n')  # replaces space between words wth new line character
            rotation = 0
            self.ax.legend(loc='lower left', ncol=5, bbox_to_anchor=(0, -0.18), frameon=False,
                           labels=self.legend_labels)

        # Values on the top of the bar if neeed
        if display_value == 'o' or display_value == 'O':
            for container in self.ax.containers:
                self.ax.bar_label(container, fmt='%.1f', padding=3)

        if plot_type == 's':
            plt.xticks(self.initial_location, self.labels, rotation=rotation)
        else:
            plt.xticks(self.label_position, self.labels, rotation=rotation)

        self.fig.savefig('charts/211021/' + name + '.png', bbox_inches='tight', transparent=True)


def get_excel(path='BarLoader_B.xlsx'):
    r"""
    Reads and parse excel spreadsheet
    you can specify absolute path like C:\Users\yourusername\desktop\BarLoader.xlsx
    or simply BarLoader.xlsx if excel and python file are in the same folder
    :param path: str, path to a file
    :return: DataFrame representation of excel
    """

    # Get Data from excel , dtype={'date': datetime}
    df = pd.read_excel(path, na_filter=False, engine='openpyxl',
                       # remove two lines below once you start using proper excel
                       nrows=16)
    chart_related_columns = ['plot_type', 'orientation', 'sorting', 'y_axis']

    # In casse if you pressed spacebar in a cell, replace it with nothing
    df[chart_related_columns] = df[chart_related_columns].replace(to_replace='\s+', value='', regex=True)

    # replacing empty cell values with default values for corresponding column
    df = df.replace({'plot_type': {'': 'b'},
                     'orientation': {'': 'h'},
                     'sorting': {'': None},
                     'y_axis': {'': 'l'},
                     'start_date': {pd.NaT: ''},
                     'end_date': {pd.NaT: ''},
                     })
    return df


def get_tickers(row):
    tickers = []
    ticker_names = {}
    for i, col_name in enumerate(row.index):
        if col_name.startswith('ticker') and row[col_name] != '':
            tickers.append(row[col_name])
            ticker_names[row[col_name]] = row[i + 1]
    return tickers, ticker_names


def check_override_value(value):
    """
    Checks override value, and converts it to yyyymmdd if needed, or leaves as it is
    :param value: str
    :return: datetime/str
    """
    if isinstance(value, datetime):
        return [value.strftime('%Y%m%d')]

    if isinstance(value, int):
        return [str(value)]
    value = [i.strip() for i in value.split(',')]
    results = []
    for i in value:
        try:
            results.append(pd.to_datetime(i).strftime('%Y%m%d').strip())
        except Exception as e:
            results.append(i.strip())
    return results
    if isinstance(value, int):
        return [str(value)]
    value = [i.strip() for i in value.split(',')]
    results = []
    for i in value:
        try:
            results.append(pd.to_datetime(i).strftime('%Y%m%d').strip())
        except Exception as e:
            results.append(i.strip())
    return results


def get_override(row):
    overrides = []
    fields = []
    for i, col_name in enumerate(row.index):
        cell = row[col_name]
        actual_override = {}
        if col_name.startswith('field_') and cell != '':
            cell = cell.split(',')
            for value in cell:
                fields.append(value.strip())
        if col_name.startswith('override_') and cell != '':
            cell = cell.split(',')
            for value in cell:
                k, v = value.strip().split('=')
                actual_override[k] = v
            overrides.append(actual_override)
    return fields, overrides


def get_data(ticker, fields, override, legend_labels):
    """
    Downloads data using blp.bpd
    :param ticker: str/list, ticker(s) name(s)
    :param fields: str/list, field(s) name(s)
    :param override: dictionary, override values
    :return: data to plot
    """
    data = pd.DataFrame()
    for idx, field in enumerate(fields):
        try:
            temp = blp.bdp(tickers=ticker, flds=field, **override[idx])
        except Exception:
            temp = blp.bdp(tickers=ticker, flds=field)
        data[legend_labels[idx]] = temp
    return data


def get_data_bdh(ticker, fields, start_date, end_date, override):
    """
    """
    data = blp.bdh(tickers=ticker, flds=fields, start_date=start_date, end_date=end_date, **override)
    data = data.T
    data = data.unstack()
    data = data.droplevel(0, axis=1)
    return data


def run():
    df = get_excel()
    for idx, row in df.iterrows():
        # if idx == 8:
        name = str(row['name'])
        fields, override = get_override(row)
        legend_labels = [i.strip() for i in row.legend_labels.split(',')]
        tickers, ticker_names = get_tickers(row)

        if override == []: override = [{}]

        try:
            if row.start_date != '':
                data = get_data_bdh(tickers, fields, row.start_date, row.end_date, override)
            else:
                data = get_data(tickers, fields, override, legend_labels)
        except Exception as e:
            print(f'Exception: {e}\nError on downloading data: {name}')

        data.index = data.index.map(ticker_names)

        if row.orientation.lower() == 'h':
            HorizontalBarChart(data,
                               row.plot_type,
                               row.sorting,
                               row.y_axis,
                               row.source,
                               name,
                               legend_labels,
                               row.display_value)
        else:
            VerticalBarChart(data,
                             row.plot_type,
                             row.sorting,
                             row.y_axis,
                             row.source,
                             name,
                             legend_labels,
                             row.display_value)

        print(idx, name, 'completed')
        if idx == 10: break


if __name__ == '__main__':
    run()
