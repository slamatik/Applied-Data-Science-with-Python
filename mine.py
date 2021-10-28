import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
# from xbbg import blp
import yfinance as yf

color_list = [
    (0, 0, 0),  # Dummy color
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
        self.ax.text(0.86, 0.02, f'Source: {source} Date: {datetime.today().date().strftime("%d/%m/%Y")}', ha='center',
                    fontsize=6)
        plt.title(name, loc='left')  # set chart name

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
        if sort == 'a' or sort == 'A': df.sort_values(by=df.columns[0], axis=0, inplace=True, ascending=True)
        elif sort == 'd' or sort == 'D': df.sort_values(by=df.columns[0], axis=0, inplace=True, ascending=False)
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
                         df[col], height=self.size, label=col, align=self.align, left=self.y_offset, color=MPL_COLORS[i], edgecolor='white', linewidth=1)
            if plot_type == 's':
                self.y_offset += df[col]
            else:
                y_locations = self.bar_group_position + self.size * i

        self.ax.legend(loc='lower left', bbox_to_anchor=(0, -0.14), ncol=5, frameon=False)
        if display_value == 'o' or display_value == 'O':
            for container in self.ax.containers: self.ax.bar_label(container, fmt='%.1f', padding=3)
        if plot_type == 's':
            plt.yticks(self.initial_location, self.labels)
        else:
            plt.yticks(self.label_position, self.labels)
        # self.fig.savefig('charts/211021/' + name + '.png', bbox_inches='tight', transparent=True)
        plt.show()

        # self.fig.savefig(rf'{name}' + '.png')


class VerticalBarChart(BarChart):
    def __init__(self, df, plot_type, sort, y_axis, source, name, legend_labels, display_value):
        super().__init__(df, plot_type, sort, y_axis, source, name, legend_labels)

        if self.n_tickers > 1: # if more than tickers -> rotate labels
            rotation = 90
        else: # less than tickers -> break them into lines
            self.labels = self.labels.str.replace(' ', '\n') # replaces space between words wth new line character
            rotation = 0

        if plot_type == 's': self.label_position = self.initial_location
        plt.xticks(self.label_position, self.labels, rotation=rotation)

        x_location = self.initial_location
        plt.grid(b=True, which='major', axis='y', color='grey', alpha=.5)
        for i, col in enumerate(df.columns, 1):
            self.ax.bar(x_location, df[col], width=self.size, label=col, align=self.align, bottom=self.y_offset,
                        color=MPL_COLORS[i], edgecolor='white', linewidth=1)
            if plot_type == 's':
                self.y_offset += df[col]
            else:
                x_location = self.bar_group_position + self.size * i

        list_of_labels = self.ax.get_xticklabels(which='major')
        render = self.fig.canvas.get_renderer()

        legend_y_pos = 0
        for l in list_of_labels:
            bbox = l.get_window_extent(render)
            bbox = self.ax.transData.inverted().transform(bbox)
            legend_y_pos = min(legend_y_pos, bbox[0][1])

        # Sets legend up
        self.ax.legend(loc='lower left', bbox_to_anchor=(0, legend_y_pos - 0.025), ncol=5, frameon=False)

        # Values on the top of the bar if neeed
        if display_value == 'o' or display_value == 'O':
            [self.ax.bar_label(container, fmt='%.1f', padding=3) for container in self.ax.containers]

        # plt.tight_layout()
        self.fig.savefig(name + '.png', bbox_inches='tight', transparent=True)
        plt.show()


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


def get_data_yf(tickers):
    # fields = ['operatingMargins', 'revenueGrowth', 'currentRatio', 'quickRatio', 'longName']
    fields = ['operatingMargins', 'revenueGrowth', 'currentRatio', 'quickRatio']

    yf_dict = {i: [] for i in tickers}
    for ticker in tickers:
        data = yf.Ticker(ticker).info
        yf_dict[ticker].append(data[fields[0]])
        yf_dict[ticker].append(data[fields[1]])
        yf_dict[ticker].append(data[fields[2]])
        yf_dict[ticker].append(data[fields[3]])
        # yf_dict[ticker].append(data[fields[4]])

    yf_df = pd.DataFrame(yf_dict, index=fields).T
    # yf_df.longName = yf_df.longName.str.replace(' ', '\n')
    # yf_df.set_index('longName', drop=True, inplace=True)
    # print(yf_df.columns)
    # return
    return yf_df


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


def run():
    df = get_excel()
    for idx, row in df.iterrows():
        name = str(row['name'])
        fields = [i.strip() for i in row.fields.split(',')]  # if multiple entries this will be split into list
        override_value = check_override_value(row.override_value)
        legend_labels = [i.strip() for i in row.name_legend.split(',')]
        tickers, ticker_names = get_tickers(row)

        data = get_data_yf(tickers)
        data.index = data.index.map(ticker_names)
        # print(data)
        # if row.override == '' or row.override_value == ['']:
        #     override = {}
        # else:
        #     override_fields = [i.strip() for i in row.override.split(', ')]
        #     override = dict(zip(override_fields, override_value))
        #
        # try:
        #     if row.start_date != '':
        #         data = get_data_bdh(tickers, fields, row.start_date, row.end_date, override)
        #     else:
        #         data = get_data(tickers, fields, override)
        # except Exception as e:
        #     print(f'Exception: {e}\nError on downloading data: {name}')

        if row.orientation.lower() == 'h':
            HorizontalBarChart(data, row.plot_type, row.sorting, row.y_axis, row.source, name, legend_labels,
                               row.display_value)
        else:
            VerticalBarChart(data, row.plot_type, row.sorting, row.y_axis, row.source, name, legend_labels,
                             row.display_value)
        print(idx, name, 'completed')
        break


if __name__ == '__main__':
    run()
