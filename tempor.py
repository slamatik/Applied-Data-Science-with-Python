import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
# from xbbg import blp
import yfinance as yf

color_list = [
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
    def __init__(self, df, plot_type, sort, y_axis, source, name, name_legend, display_value):
        self.df = df
        self.plot_type = plot_type
        self.sort = sort
        self.y_axis = y_axis
        self.source = source
        self.name = name
        self.name_legend = name_legend
        self.display_value = False

        self.n_rows = len(self.df)  # number of tickers
        self.n_cols = len(self.df.columns)  # number of fields
        self.labels = df.index  # list of ticker names

        # self.size = round(1 / self.n_cols - 0.1, 2)
        self.size = round(1 / self.n_cols, 2)  # size of a single bar
        self.gap = self.size * 1  # gap between groups, might need to change it based on number of tickers

        self.x = np.zeros(self.n_rows)  # initialize empty list for bar groups position
        self.initial_location = self.x  # save initial bar location
        for i in range(self.n_rows): self.x[i] = round((self.size * self.n_cols + self.gap) * i, 2)

        self.label_position = self.x + (self.size * self.n_cols) / 2  # x label positions (middle of the bar(s))

        self.fig, self.ax = plt.subplots(figsize=(12, 8))  # initialize matplotlib figure
        plt.figtext(0.86, 0.02, f'Source: {source} Date: {datetime.today().date().strftime("%d/%m/%Y")}', ha='center',
                    fontsize=6)
        plt.title(name, loc='left')

        if display_value == 'o':
            self.display_value = True

        # Figure borders
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_visible(False)

        # Where to show y-axis
        if self.y_axis == 'r': self.ax.tick_params(labelright=True, right=True, labelleft=False, left=False)
        if self.y_axis == 'b': self.ax.tick_params(labelright=True, right=True)

        # Sort if needed
        if self.sort == 'a': self.df.sort_values(by=self.df.columns[0], axis=0, inplace=True, ascending=True)
        if self.sort == 'd': self.df.sort_values(by=self.df.columns[0], axis=0, inplace=True, ascending=False)

        # Stacked BarChart Settings
        if self.plot_type == 's':
            self.align = 'center'
            self.y_offset = np.zeros(self.n_rows)
        else:
            self.y_offset = None
            self.align = 'edge'


class HorizontalBarChart(BarChart):
    def __init__(self, df, plot_type, sort, y_axis, source, name, name_legend, display_value):
        super().__init__(df, plot_type, sort, y_axis, source, name, name_legend, display_value)

        y_locations = self.initial_location
        plt.grid(b=True, which='major', axis='x', color='grey', alpha=.5)
        for i, col in enumerate(df.columns, 1):
            self.ax.barh(y_locations, df[col], height=self.size, label=col, align=self.align, left=self.y_offset,
                         color=MPL_COLORS[i], edgecolor='white', linewidth=1)
            if plot_type == 's':
                self.y_offset += df[col]
            else:
                y_locations = self.x + self.size * i

        self.ax.legend(loc='lower left', bbox_to_anchor=(0, -0.14), ncol=5, frameon=False)
        if self.display_value:
            for container in self.ax.containers: self.ax.bar_label(container, fmt='%.1f', padding=3)
        if plot_type == 's':
            plt.yticks(self.initial_location, self.labels)
        else:
            plt.yticks(self.label_position, self.labels)
        # self.fig.savefig('charts/211021/' + name + '.png', bbox_inches='tight', transparent=True)
        plt.show()

        self.fig.savefig(rf'{name}' + '.png')


class VerticalBarChart(BarChart):
    def __init__(self, df, plot_type, sort, y_axis, source, name, name_legend, display_value):
        super().__init__(df, plot_type, sort, y_axis, source, name, name_legend, display_value)

        x_location = self.initial_location
        plt.grid(b=True, which='major', axis='y', color='grey', alpha=.5)
        for i, col in enumerate(df.columns, 1):
            self.ax.bar(x_location, df[col], width=self.size, label=col, align=self.align, bottom=self.y_offset,
                        color=MPL_COLORS[i], edgecolor='white', linewidth=1)
            if plot_type == 's':
                self.y_offset += df[col]
            else:
                x_location = self.x + self.size * i

        self.ax.legend(loc='lower left', bbox_to_anchor=(0, -0.14), ncol=5, frameon=False)
        if self.display_value:
            for container in self.ax.containers: self.ax.bar_label(container, fmt='%.1f', padding=3)
        if plot_type == 's':
            plt.xticks(self.initial_location, self.labels)
        else:
            plt.xticks(self.label_position, self.labels)
        # self.fig.savefig('charts/211021/' + name + '.png', bbox_inches='tight', transparent=True)
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
    fields = ['operatingMargins', 'revenueGrowth', 'currentRatio', 'quickRatio']

    yf_dict = {i: [] for i in tickers}
    for ticker in tickers:
        data = yf.Ticker(ticker).info
        yf_dict[ticker].append(data[fields[0]])
        yf_dict[ticker].append(data[fields[1]])
        yf_dict[ticker].append(data[fields[2]])
        yf_dict[ticker].append(data[fields[3]])

    yf_df = pd.DataFrame(yf_dict, index=fields).T
    # print(yf_df.columns)
    # return
    return yf_df


def get_data_example():
    with open('example.pkl', 'rb') as f:
        df = pickle.load(f)

    # return df.drop('current_trr_ytd', axis=1)
    return df


def get_tickers(row):
    tickers = []
    ticker_names = {}
    for i, col_name in enumerate(row.index):
        if col_name.startswith('ticker') and row[col_name] != '':
            tickers.append(row[col_name])
            ticker_names[row[col_name]] = row[i + 1]
    print(ticker_names)
    return tickers


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


def get_data(ticker, fields, override):
    """
    Downloads data using blp.bpd
    :param ticker: str/list, ticker(s) name(s)
    :param fields: str/list, field(s) name(s)
    :param override: dictionary, override values
    :return: data to plot
    """
    data = blp.bdp(tickers=ticker, flds=fields, **override)
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
        name = str(row['name'])
        fields = [i.strip() for i in row.fields.split(',')]  # if multiple entries this will be split into list
        override_value = check_override_value(row.override_value)
        name_legend = [i.strip() for i in row.name_legend.split(',')]
        tickers = get_tickers(row)
        print(tickers)
        break

        data = get_data_yf(tickers)
        # print(data)
        # data.index = ['kekw', 'asd']
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
            HorizontalBarChart(data, row.plot_type, row.sorting, row.y_axis, row.source, name, name_legend,
                               row.display_value)
        else:
            VerticalBarChart(data, row.plot_type, row.sorting, row.y_axis, row.source, name, name_legend,
                             row.display_value)
        print(idx, name, 'completed')
        break


if __name__ == '__main__':
    run()
