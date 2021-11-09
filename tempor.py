import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
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

TICK_SIZE = 13  # x or y axis tick label size
TICKER_NAME_SIZE = 12
# List of all fonts available : ['Candara', 'Garamond', 'Adobe Fan Heiti Std', 'Ink Free', 'Dubai', 'Bell MT', 'Gill Sans MT Ext Condensed Bold', 'Microsoft Tai Le', 'Lucida Bright', 'Adobe Gothic Std', 'Malgun Gothic', 'Lucida Fax', 'Garamond', 'IGES 1001', 'Lucida Sans Typewriter', 'Solid Edge ANSI', 'Gadugi', 'Gigi', 'SWGreks', 'Tempus Sans ITC', 'Franklin Gothic Medium', 'Dubai', 'Blackadder ITC', 'SWMap', 'Comic Sans MS', 'Rockwell Extra Bold', 'SERomanc', 'Franklin Gothic Medium', 'Palatino Linotype', 'Franklin Gothic Demi', 'Courier New', 'Constantia', 'Lucida Sans Unicode', 'Segoe UI', 'Courier New', 'Freestyle Script', 'Yu Gothic', 'Vladimir Script', 'SWIsop1', 'Perpetua', 'Verdana', 'SWRomnc', 'Solid Edge ANSI', 'Segoe UI', 'Onyx', 'Bodoni MT', 'Solid Edge ISO2 Symbols', 'Solid Edge ISO Unicode', 'Gadugi', 'Trebuchet MS', 'Lucida Sans', 'Lucida Bright', 'Adobe Arabic', 'Tw Cen MT', 'Tw Cen MT Condensed', 'Helvetica-Narrow', 'Gill Sans MT', 'Forte', 'SWItalc', 'Engravers MT', 'Segoe UI', 'Bodoni MT', 'Snap ITC', 'Gill Sans Ultra Bold Condensed', 'Lucida Console', 'Script MT Bold', 'Garamond', 'Consolas', 'Tw Cen MT Condensed', 'Forte', 'Broadway', 'Times New Roman', 'Tw Cen MT', 'Baskerville Old Face', 'SWMono', 'Felix Titling', 'Segoe Script', 'Leelawadee UI', 'Consolas', 'SETxt', 'Perpetua', 'Wingdings 3', 'Leelawadee', 'Brush Script MT', 'Lucida Sans', 'Symbol', 'PDM', 'Californian FB', 'Bookman Old Style', 'Microsoft JhengHei', 'Tempus Sans ITC', 'SWMono', 'Californian FB', 'Microsoft YaHei', 'Georgia', 'Bookshelf Symbol 7', 'Niagara Solid', 'Solid Edge ANSI2 Symbols', 'Lucida Calligraphy', 'Showcard Gothic', 'Cambria', 'Microsoft New Tai Lue', 'Eras Bold ITC', 'Cooper Black', 'Tahoma', 'Corbel', 'Bodoni MT', 'Trebuchet MS', 'Lucida Sans Typewriter', 'Old English Text MT', 'Solid Edge ANSI Unicode', 'Trebuchet MS', 'Pristina', 'Calibri', 'High Tower Text', 'Yu Gothic', 'Yu Gothic', 'Lucida Fax', 'Century Gothic', 'Book Antiqua', 'Freestyle Script', 'Nirmala UI', 'Onyx', 'Verdana', 'Franklin Gothic Heavy', 'Gill Sans MT', 'SESimplex', 'Goudy Old Style', 'SWIsop2', 'Niagara Engraved', 'Courier New', 'Segoe UI', 'Candara', 'Castellar', 'Brush Script MT', 'Segoe Print', 'Copperplate Gothic Light', 'Blackadder ITC', 'Minion Pro', 'Berlin Sans FB', 'Segoe UI Symbol', 'Bodoni MT', 'Corbel', 'Segoe UI Historic', 'Microsoft JhengHei', 'Maiandra GD', 'Gill Sans MT', 'Goudy Old Style', 'Viner Hand ITC', 'Cambria', 'Microsoft YaHei', 'Playbill', 'Constantia', 'Perpetua', 'Lucida Sans Typewriter', 'SWIsot3', 'Arial', 'Microsoft Himalaya', 'Microsoft Himalaya', 'Consolas', 'Gabriola', 'Arial', 'Lucida Fax', 'SWIsot1', 'Tahoma', 'Microsoft YaHei', 'Solid Edge ISO3 Symbols', 'Times New Roman', 'Edwardian Script ITC', 'Solid Edge ANSI', 'SIEMENS_GOST Type A', 'SWGothi', 'Bell MT', 'SWGrekc', 'Calibri', 'Adobe Myungjo Std', 'Rockwell', 'Tahoma', 'SWGreks', 'Microsoft YaHei', 'Solid Edge ANSI', 'Showcard Gothic', 'Calibri', 'SWSimp', 'Bodoni MT', 'Californian FB', 'High Tower Text', 'Rockwell', 'Trebuchet MS', 'Century', 'Verdana', 'Solid Edge ANSI GDT Symbols', 'Calibri', 'Agency FB', 'Microsoft PhagsPa', 'Consolas', 'Dubai', 'Sitka Small', 'Verdana', 'Bodoni MT', 'Bodoni MT', 'Leelawadee UI', 'Bodoni MT', 'Microsoft JhengHei', 'MS Outlook', 'Calibri', 'Microsoft Uighur', 'Solid Edge ISO CE', 'Gill Sans MT', 'Arial', 'Myanmar Text', 'Lucida Fax', 'Segoe UI', 'Arial', 'Franklin Gothic Book', 'Solid Edge GOST1 Symbols', 'Agency FB', '3ds', 'HoloLens MDL2 Assets', 'Palatino Linotype', 'Cambria', 'SWItal', 'Times New Roman', 'Solid Edge ISO3 Symbols', 'Lucida Fax', 'Microsoft JhengHei', 'Sylfaen', 'Bookman Old Style', 'MingLiU-ExtB', 'Vivaldi', 'Calisto MT', 'Calisto MT', 'Adobe Arabic', 'Lucida Sans Typewriter', 'Kunstler Script', 'Eras Light ITC', 'Microsoft Sans Serif', 'Book Antiqua', 'Adobe Hebrew', 'OCR A Extended', 'Century Schoolbook', 'Wingdings', 'Segoe UI', 'Jokerman', 'Arial', 'Lucida Sans Unicode', 'Century Schoolbook', 'Bodoni MT', 'Eras Light ITC', 'Candara', 'MingLiU-ExtB', 'Palatino Linotype', 'Californian FB', 'Corbel', '3DS Fonticon', 'Eras Demi ITC', 'Franklin Gothic Medium', 'Arial', 'SWMusic', 'Ink Free', 'Gill Sans MT', 'Cambria', 'Courier New', 'IGES 1001', 'Segoe Print', 'Gill Sans Ultra Bold', 'Algerian', 'Wide Latin', 'SWItalt', 'Comic Sans MS', 'Jokerman', 'Constantia', 'SWRomnc', 'Segoe UI', 'Leelawadee', 'Juice ITC', 'Leelawadee', 'Segoe UI', 'Curlz MT', 'Rockwell Condensed', 'Candara', 'Californian FB', 'Courier New', 'Bookman Old Style', 'Rockwell', 'Lucida Bright', 'Microsoft JhengHei', 'Poor Richard', 'Britannic Bold', 'Bodoni MT', 'Lucida Sans', 'Gigi', 'Franklin Gothic Medium Cond', 'Rockwell Condensed', 'Bell MT', 'SWComp', 'Rockwell', 'Solid Edge ANSI Unicode', 'Tw Cen MT', 'SWIsot2', 'Webdings', 'Bodoni MT', 'Rockwell', 'SWItalc', 'Wingdings 2', 'Franklin Gothic Book', 'Tw Cen MT Condensed', 'Arial', 'Century Schoolbook', 'Microsoft Tai Le', 'Nirmala UI', 'Leelawadee UI', 'Elephant', 'PDM', 'Franklin Gothic Book', 'Candara', 'Myriad Pro', 'Magneto', 'SolidWorks GDT', 'Candara', 'SimSun', 'Solid Edge ANSI3 Symbols', '3DS Fonticon', 'Constantia', 'SEGDT', 'Ebrima', 'SimSun-ExtB', 'OLF SimpleSansOC', 'Juice ITC', 'SWRomnd', 'Microsoft Uighur', 'Book Antiqua', 'Matura MT Script Capitals', 'Corbel', 'Gill Sans MT', 'Bodoni MT', 'Engravers MT', 'Century Gothic', 'Impact', 'Franklin Gothic Demi Cond', 'Adobe Thai', 'Maiandra GD', 'Gill Sans MT Condensed', 'Lucida Handwriting', 'Microsoft New Tai Lue', 'Solid Edge ISO2 Symbols', 'Solid Edge ISO', 'Comic Sans MS', 'Perpetua', 'Segoe UI', 'Dubai', 'Corbel', 'Book Antiqua', 'Bell MT', 'SWGothg', 'Solid Edge ANSI', 'Agency FB', 'Comic Sans MS', 'Segoe UI Symbol', 'Tw Cen MT', 'Sitka Small', 'Solid Edge ISO Unicode', 'Courier New', 'Chiller', 'SEMonotxt', 'Tw Cen MT', 'TeamViewer15', 'MS Reference Sans Serif', 'Franklin Gothic Demi', 'Bodoni MT', 'Arial', 'Tahoma', 'Segoe UI', 'Solid Edge ISO GDT Symbols', 'Georgia', 'Georgia', 'Rockwell Extra Bold', 'Rage Italic', 'Segoe Script', 'Malgun Gothic', 'Arial', 'Sitka Small', 'Calibri', 'Bradley Hand ITC', 'Impact', 'SWGrekc', 'Malgun Gothic', 'Lucida Bright', 'Solid Edge ISO Unicode', 'Elephant', 'Leelawadee UI', 'Ebrima', 'Microsoft Yi Baiti', 'Goudy Old Style', 'Courier New', 'Palace Script MT', 'Sitka Small', 'Solid Edge GOST1 Symbols', 'Segoe UI', 'Monotype Corsiva', 'Calibri', 'Consolas', 'Tw Cen MT Condensed', 'Times New Roman', 'Courier Std', 'Lucida Sans Typewriter', 'MV Boli', 'SWLink', 'Century Schoolbook', 'Solid Edge ANSI Unicode', 'Script MT Bold', 'Tw Cen MT', 'Bodoni MT', 'Mongolian Baiti', 'Calibri', 'Perpetua Titling MT', 'SWIsop1', 'Calisto MT', 'SERomanc', 'Javanese Text', 'Eras Demi ITC', 'Franklin Gothic Heavy', 'Bodoni MT', 'Centaur', 'MS Reference Specialty', 'Lucida Sans', 'SWScrps', 'Tw Cen MT Condensed Extra Bold', 'Arial', 'Solid Edge ISO', 'Snap ITC', 'Century Gothic', 'Century Schoolbook', 'Solid Edge ISO Unicode', 'Papyrus', 'Solid Edge ISO Unicode', 'Segoe UI', 'Goudy Stout', 'Adobe Ming Std', 'Corbel', 'Solid Edge ISO1 Symbols', 'Verdana', 'MS Outlook', 'Verdana', 'Myanmar Text', 'Microsoft Uighur', 'SWIsot2', 'Bodoni MT', 'Parchment', 'Bradley Hand ITC', 'HYSWLongFangSong', 'High Tower Text', 'Bodoni MT', 'Wingdings 3', 'SESimplex', 'IGES 1002', 'SWTxt', 'SIEMENS_GOST Type A', 'Malgun Gothic', 'Trebuchet MS', 'Solid Edge Stencil', 'Helvetica-Narrow', 'Nirmala UI', 'Solid Edge ANSI Unicode', 'Calibri', 'Sitka Small', 'Nirmala UI', 'Arial Rounded MT Bold', 'Microsoft Sans Serif', 'Adobe Thai', 'Yu Gothic', 'Ebrima', 'Imprint MT Shadow', 'Comic Sans MS', 'Goudy Old Style', 'SWMeteo', 'Microsoft Uighur', 'Gloucester MT Extra Condensed', 'Perpetua', 'Adobe Hebrew', 'SWMath', 'Monotype Corsiva', 'Solid Edge ANSI Unicode', 'Bodoni MT', 'Mistral', 'Harrington', 'Courier New', 'SWItalt', 'Georgia', 'Times New Roman', 'Franklin Gothic Heavy', 'Bookman Old Style', 'Nirmala UI', 'Solid Edge ISO', 'Gill Sans MT Ext Condensed Bold', 'Segoe UI', 'Algerian', 'SWRomns', 'Palatino Linotype', 'Magneto', 'SWGothg', 'Gill Sans Ultra Bold Condensed', 'Microsoft PhagsPa', 'Dubai', 'Bernard MT Condensed', 'Myanmar Text', 'Comic Sans MS', 'Berlin Sans FB Demi', 'Modern No. 20', 'Adobe Pi Std', 'Rockwell Condensed', 'Solid Edge ISO Unicode', 'Arial', 'Cambria', 'SolidWorks GDT', 'Solid Edge ISO', 'SWIsot3', 'Californian FB', 'SWGothe', 'Segoe UI', 'IGES 1002', 'SWIsop3', 'SWRomnt', 'French Script MT', 'IGES 1003', 'SWGothi', 'Segoe UI', 'Bookshelf Symbol 7', 'Rockwell', 'Arial', 'Gadugi', 'Dubai', 'Segoe Script', 'SERomans', 'Microsoft New Tai Lue', 'Adobe Hebrew', 'Britannic Bold', 'Playbill', 'Gloucester MT Extra Condensed', 'Stencil', 'Solid Edge ANSI', 'Franklin Gothic Book', 'Bodoni MT', 'Courier Std', 'Calisto MT', 'Haettenschweiler', 'Gill Sans MT Condensed', 'Constantia', 'Garamond', 'Goudy Old Style', 'Bernard MT Condensed', 'Lucida Sans', 'Javanese Text', 'Papyrus', 'Imprint MT Shadow', 'Palatino Linotype', 'MS Gothic', 'Solid Edge ISO Unicode', 'Informal Roman', 'Webdings', 'Sitka Small', 'Microsoft Tai Le', 'Footlight MT Light', 'Ravie', 'Book Antiqua', 'Trebuchet MS', 'Myriad CAD', 'Leelawadee UI', 'Calibri', 'Agency FB', 'Candara', 'SWSimp', 'Lucida Sans Typewriter', 'Dubai', 'Adobe Thai', 'Yu Gothic', 'SWIsop3', 'Franklin Gothic Demi Cond', 'Comic Sans MS', 'Franklin Gothic Medium Cond', 'Cooper Black', 'Century Schoolbook', 'Microsoft Tai Le', 'SEMonotxt', 'Haettenschweiler', 'Adobe Song Std', 'Century Schoolbook', 'SWGDT', 'Adobe Arabic', 'Candara', 'Solid Edge ANSI Unicode', 'SWItal', 'Franklin Gothic Medium', 'Leelawadee', 'Perpetua', 'SERomans', 'Viner Hand ITC', 'Segoe UI', 'Chiller', 'Felix Titling', 'Candara', 'SWTxt', 'Symbol', 'Lucida Sans Typewriter', 'Footlight MT Light', 'HYSWLongFangSong', 'TeamViewer15', 'SWIsot1', 'Solid Edge ANSI1 Symbols', 'Malgun Gothic', 'Bodoni MT', 'SWMap', 'Harrington', 'Corbel', 'Helvetica-Narrow', 'Perpetua Titling MT', 'Solid Edge ANSI3 Symbols', 'Informal Roman', 'Solid Edge ANSI', 'Calisto MT', 'Courier Std', 'Niagara Solid', 'Bell MT', 'Niagara Engraved', 'Microsoft New Tai Lue', 'SWGDT', 'Solid Edge ANSI1 Symbols', 'Segoe MDL2 Assets', 'Lucida Sans', 'SERomand', 'Corbel', 'Lucida Handwriting', 'Leelawadee UI', 'Segoe UI', 'Book Antiqua', 'Cambria', 'Georgia', 'Lucida Fax', 'Arial', 'Solid Edge ISO1 Symbols', 'Lucida Sans Typewriter', 'Stencil', 'Old English Text MT', 'Vladimir Script', 'Pristina', 'Bahnschrift', 'Solid Edge ISO CE', 'Microsoft Yi Baiti', 'Verdana', 'Tw Cen MT Condensed Extra Bold', 'Wingdings', 'SWRomnd', 'Gadugi', 'Lucida Calligraphy', 'Candara', 'Palatino Linotype', 'Copperplate Gothic Bold', 'OLF SimpleSansOC', 'Corbel', 'Baskerville Old Face', 'Solid Edge ANSI', 'Lucida Sans', 'Wide Latin', 'SWMusic', 'web-PDM', 'Segoe UI', 'Segoe UI', 'Helvetica-Narrow', 'Solid Edge ISO GDT Symbols', 'Segoe UI', 'Copperplate Gothic Light', 'Castellar', 'Solid Edge ANSI Unicode', 'Century Gothic', 'Sitka Small', 'Solid Edge ISO', 'Franklin Gothic Heavy', 'MS Reference Specialty', 'Arial', 'Segoe Print', 'Harlow Solid Italic', 'Bookman Old Style', 'Calibri', 'Segoe UI Historic', 'SWScrpc', 'Wingdings 2', 'High Tower Text', 'Century Schoolbook', 'Solid Edge ANSI2 Symbols', 'Kozuka Mincho Pr6N', 'Berlin Sans FB', 'SimSun', 'Bell MT', 'Perpetua', 'Franklin Gothic Demi', 'Mongolian Baiti', 'Segoe Script', 'Garamond', 'Berlin Sans FB Demi', 'Corbel', 'Georgia', 'SWAstro', 'Segoe UI', 'Harlow Solid Italic', 'Book Antiqua', 'HoloLens MDL2 Assets', 'Palatino Linotype', 'Georgia', 'Segoe UI', 'Helvetica-Narrow', 'Goudy Old Style', 'Perpetua Titling MT', 'Trebuchet MS', 'SEGDT', 'Trebuchet MS', 'SWComp', 'SWScrps', 'Century Gothic', 'Constantia', 'Lucida Bright', 'SWGothe', 'Calisto MT', 'Consolas', 'SETxt', 'SWRomnt', 'Rockwell Condensed', 'Bodoni MT', 'Candara', 'Bookman Old Style', 'Cambria', 'Constantia', 'Rage Italic', 'Tw Cen MT', 'Berlin Sans FB', 'Curlz MT', 'Century Gothic', 'Elephant', 'Adobe Arabic', 'Solid Edge Stencil', 'Myanmar Text', 'Franklin Gothic Demi', 'Kristen ITC', 'Bauhaus 93', 'Solid Edge ANSI GDT Symbols', 'Cambria', 'Adobe Heiti Std', 'Calisto MT', 'Arial', 'Eras Medium ITC', 'Helvetica-Narrow', 'SWMeteo', 'Yu Gothic', 'Solid Edge ISO', 'Century Gothic', 'Century Gothic', 'Candara', 'Kozuka Gothic Pr6N', 'Gill Sans MT', 'Lucida Console', 'Poor Richard', 'Arial Rounded MT Bold', 'SWRomns', 'Times New Roman', 'Segoe UI Emoji', 'Berlin Sans FB', 'Lucida Fax', 'Constantia', 'Gill Sans Ultra Bold', 'Perpetua', 'Sylfaen', 'SWMath', 'Times New Roman', 'Courier Std', 'Bodoni MT', 'Bookman Old Style', 'Corbel', 'Georgia', 'Segoe MDL2 Assets', 'SERomand', 'Palatino Linotype', 'Adobe Hebrew', 'Verdana', 'Gill Sans MT', 'IGES 1003', 'Centaur', 'French Script MT', 'Microsoft YaHei', 'Colonna MT', 'Marlett', 'Vivaldi', 'SWIsop2', 'Nirmala UI', 'MS Reference Sans Serif', 'Century', 'Segoe UI', 'Dubai', 'Helvetica-Narrow', 'Malgun Gothic', 'Bauhaus 93', 'Colonna MT', 'Adobe Thai', 'MS Gothic', 'MT Extra', 'Segoe Print', 'Segoe UI Emoji', 'Lucida Bright', 'Kunstler Script', 'Calisto MT', 'Lucida Bright', 'Ravie', 'Helvetica-Narrow', 'Microsoft PhagsPa', 'SWAstro', 'Broadway', 'Solid Edge ISO', 'MV Boli', 'Eras Medium ITC', 'Kristen ITC', 'Lucida Sans', 'Segoe UI', 'Microsoft PhagsPa', 'Arial', 'Matura MT Script Capitals', 'Bookman Old Style', 'Tw Cen MT', 'Solid Edge ANSI Unicode', 'Mistral', 'MT Extra', 'Yu Gothic', 'SWScrpc', 'Lucida Bright', 'Perpetua Titling MT', 'Elephant', 'Arial', 'Comic Sans MS', 'OCR A Extended', 'SWLink', 'Arial', 'Lucida Fax', 'Microsoft JhengHei', 'Gabriola', 'Parchment', 'Consolas', 'Palace Script MT', 'Garamond', 'Edwardian Script ITC', 'SimSun-ExtB', 'Corbel', 'Rockwell', 'Ebrima', 'Goudy Stout', 'Modern No. 20', 'Bahnschrift', 'Copperplate Gothic Bold', 'Solid Edge ISO', 'Times New Roman', 'Yu Gothic', 'Eras Bold ITC', 'Rockwell', 'Sitka Small', 'Microsoft YaHei', 'Calibri', 'Consolas', 'Solid Edge ISO Unicode', 'Book Antiqua', 'web-PDM']
matplotlib.rcParams['font.family'] = 'Calibri'


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
        self.t = plt.figtext(0.81, 0.01, f'Source: {source} Date: {datetime.today().date().strftime("%d/%m/%Y")}',
                             ha='center',
                             fontsize=7)
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

    def plot_scatter(self, data):
        min_data = data[0]
        max_data = data[1]
        average_data = data[2]

        # print(min_data)

        for col in min_data.columns:
            # self.ax.scatter(min_data.index, min_data[col])
            self.ax.scatter(min_data[col], min_data.index)
        self.fig.savefig('charts/211021/' + 'test' + '.png', bbox_inches='tight', transparent=True)


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
            plt.yticks(self.initial_location, self.labels, fontsize=TICKER_NAME_SIZE)
        else:
            plt.yticks(self.label_position, self.labels, fontsize=TICKER_NAME_SIZE)
        self.ax.legend(loc='lower left', bbox_to_anchor=(0, -0.14), ncol=5, frameon=False, labels=self.legend_labels)

        plt.axvline(0, color='black', linewidth=0.5)
        plt.xticks(fontsize=TICK_SIZE)
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

        if self.n_tickers > 15:  # if more than tickers -> rotate labels
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
            plt.xticks(self.initial_location, self.labels, rotation=rotation, fontsize=TICKER_NAME_SIZE)
        else:
            plt.xticks(self.label_position, self.labels, rotation=rotation, fontsize=TICKER_NAME_SIZE)

        plt.axhline(0, color='black', linewidth=0.5)

        plt.yticks(fontsize=TICK_SIZE)
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
                       nrows=23)
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
                     'start_date_scatter': {pd.NaT: ''},
                     'end_date_scatter': {pd.NaT: ''}
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
            override_cell = row[i + 1]
            if override_cell == '':
                overrides.append({})
            else:
                override_cell = override_cell.split(',')
                for value in override_cell:
                    k, v = value.strip().split('=')
                    actual_override[k] = v
                overrides.append(actual_override)
    # =============================================================================
    #         if col_name.startswith('override_') and cell != '':
    #             cell = cell.split(',')
    #             for value in cell:
    #                 k, v = value.strip().split('=')
    #                 actual_override[k] = v
    #             overrides.append(actual_override)
    # =============================================================================
    return fields, overrides


def get_data(ticker, fields, override, legend_labels):
    """
    Downloads data using blp.bpd
    :param ticker: str/list, ticker(s) name(s)
    :param fields: str/list, field(s) name(s)
    :param override: dictionary, override values
    :return: data to plot
    """
    # print(override)
    # print(fields, override[0], legend_labels)
    data = pd.DataFrame()
    for idx, field in enumerate(fields):
        # print(idx, field)
        try:
            temp = blp.bdp(tickers=ticker, flds=field, **override[idx])
        except Exception as e:
            temp = blp.bdp(tickers=ticker, flds=field)
        # print(temp)
        data[legend_labels[idx]] = temp
    return data


def get_data_bdh(ticker, fields, start_date, end_date, override, legend_labels, full_data=False):
    data = pd.DataFrame()
    if not full_data:
        for idx, field in enumerate(fields):
            try:
                temp = blp.bdh(tickers=ticker, flds=field, start_date=start_date, end_date=end_date, **override[idx])
            except Exception as e:
                temp = blp.bdh(tickers=ticker, flds=field, start_date=start_date, end_date=end_date)
            temp = temp.T.unstack()[start_date]

            data[legend_labels[idx]] = temp
        return data
    else:
        min_data = pd.DataFrame()
        max_data = pd.DataFrame()
        average_data = pd.DataFrame()
        for idx, field in enumerate(fields):
            try:
                temp = blp.bdh(tickers=ticker, flds=field, start_date=start_date, end_date=end_date, **override[idx])
            except Exception as e:
                temp = blp.bdh(tickers=ticker, flds=field, start_date=start_date, end_date=end_date)
            min_data[legend_labels[idx]] = temp[ticker].min().unstack()
            max_data[legend_labels[idx]] = temp[ticker].max().unstack()
            average_data[legend_labels[idx]] = temp[ticker].mean().unstack()
        return min_data, max_data, average_data


def run():
    df = get_excel()
    for idx, row in df.iterrows():
        # if idx == 8:   #Select single row from Excel Input
        name = str(row['name'])
        fields, override = get_override(row)
        legend_labels = [i.strip() for i in row.legend_labels.split(',')]
        tickers, ticker_names = get_tickers(row)
        start_date = pd.to_datetime(row.start_date).date() if row.start_date != '' else ''
        end_date = pd.to_datetime(row.end_date).date() if row.end_date != '' else ''
        start_date_scatter = pd.to_datetime(row.start_date_scatter).date() if row.start_date_scatter != '' else ''
        end_date_scatter = pd.to_datetime(row.end_date_scatter).date() if row.end_date_scatter != '' else ''

        if override == []: override = [{}]

        try:
            if start_date != '':
                data = get_data_bdh(tickers, fields, start_date, end_date, override, legend_labels)
            else:
                data = get_data(tickers, fields, override, legend_labels)
        except Exception as e:
            print(f'Exception: {e}\nError on downloading data: {name}')

        # =============================================================================
        #             try:
        #                 if start_date_scatter != '':
        #                     scatter_data = get_data_bdh(tickers, fields, start_date_scatter, end_date_scatter, override, legend_labels, True)
        #                     #print(scatter_data)
        #             except Exception as e:
        #                 print(f'Exception: {e}\nError on downloading scatter data: {name}')
        # =============================================================================

        data.index = data.index.map(ticker_names)

        if row.orientation.lower() == 'h':
            plot = HorizontalBarChart(data,
                                      row.plot_type,
                                      row.sorting,
                                      row.y_axis,
                                      row.source,
                                      name,
                                      legend_labels,
                                      row.display_value)
        else:
            plot = VerticalBarChart(data,
                                    row.plot_type,
                                    row.sorting,
                                    row.y_axis,
                                    row.source,
                                    name,
                                    legend_labels,
                                    row.display_value)
        # =============================================================================
        #             if scatter_data:
        #                 plot.plot_scatter(scatter_data)
        # =============================================================================
        print(idx, name, 'completed')

    # ♣ if idx==0: break


if __name__ == '__main__':
    run()
