import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
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

scatter_colors = [
    (1, 1, 1),
    (51 / 255, 25 / 255, 0),
    (51 / 255, 25 / 255, 0)
]

TICK_SIZE = 13  # x or y axis tick label size
TICKER_NAME_SIZE = 12
TEXT_FONT = 9
# List of all fonts available : ['Candara', 'Garamond', 'Adobe Fan Heiti Std', 'Ink Free', 'Dubai', 'Bell MT', 'Gill Sans MT Ext Condensed Bold', 'Microsoft Tai Le', 'Lucida Bright', 'Adobe Gothic Std', 'Malgun Gothic', 'Lucida Fax', 'Garamond', 'IGES 1001', 'Lucida Sans Typewriter', 'Solid Edge ANSI', 'Gadugi', 'Gigi', 'SWGreks', 'Tempus Sans ITC', 'Franklin Gothic Medium', 'Dubai', 'Blackadder ITC', 'SWMap', 'Comic Sans MS', 'Rockwell Extra Bold', 'SERomanc', 'Franklin Gothic Medium', 'Palatino Linotype', 'Franklin Gothic Demi', 'Courier New', 'Constantia', 'Lucida Sans Unicode', 'Segoe UI', 'Courier New', 'Freestyle Script', 'Yu Gothic', 'Vladimir Script', 'SWIsop1', 'Perpetua', 'Verdana', 'SWRomnc', 'Solid Edge ANSI', 'Segoe UI', 'Onyx', 'Bodoni MT', 'Solid Edge ISO2 Symbols', 'Solid Edge ISO Unicode', 'Gadugi', 'Trebuchet MS', 'Lucida Sans', 'Lucida Bright', 'Adobe Arabic', 'Tw Cen MT', 'Tw Cen MT Condensed', 'Helvetica-Narrow', 'Gill Sans MT', 'Forte', 'SWItalc', 'Engravers MT', 'Segoe UI', 'Bodoni MT', 'Snap ITC', 'Gill Sans Ultra Bold Condensed', 'Lucida Console', 'Script MT Bold', 'Garamond', 'Consolas', 'Tw Cen MT Condensed', 'Forte', 'Broadway', 'Times New Roman', 'Tw Cen MT', 'Baskerville Old Face', 'SWMono', 'Felix Titling', 'Segoe Script', 'Leelawadee UI', 'Consolas', 'SETxt', 'Perpetua', 'Wingdings 3', 'Leelawadee', 'Brush Script MT', 'Lucida Sans', 'Symbol', 'PDM', 'Californian FB', 'Bookman Old Style', 'Microsoft JhengHei', 'Tempus Sans ITC', 'SWMono', 'Californian FB', 'Microsoft YaHei', 'Georgia', 'Bookshelf Symbol 7', 'Niagara Solid', 'Solid Edge ANSI2 Symbols', 'Lucida Calligraphy', 'Showcard Gothic', 'Cambria', 'Microsoft New Tai Lue', 'Eras Bold ITC', 'Cooper Black', 'Tahoma', 'Corbel', 'Bodoni MT', 'Trebuchet MS', 'Lucida Sans Typewriter', 'Old English Text MT', 'Solid Edge ANSI Unicode', 'Trebuchet MS', 'Pristina', 'Calibri', 'High Tower Text', 'Yu Gothic', 'Yu Gothic', 'Lucida Fax', 'Century Gothic', 'Book Antiqua', 'Freestyle Script', 'Nirmala UI', 'Onyx', 'Verdana', 'Franklin Gothic Heavy', 'Gill Sans MT', 'SESimplex', 'Goudy Old Style', 'SWIsop2', 'Niagara Engraved', 'Courier New', 'Segoe UI', 'Candara', 'Castellar', 'Brush Script MT', 'Segoe Print', 'Copperplate Gothic Light', 'Blackadder ITC', 'Minion Pro', 'Berlin Sans FB', 'Segoe UI Symbol', 'Bodoni MT', 'Corbel', 'Segoe UI Historic', 'Microsoft JhengHei', 'Maiandra GD', 'Gill Sans MT', 'Goudy Old Style', 'Viner Hand ITC', 'Cambria', 'Microsoft YaHei', 'Playbill', 'Constantia', 'Perpetua', 'Lucida Sans Typewriter', 'SWIsot3', 'Arial', 'Microsoft Himalaya', 'Microsoft Himalaya', 'Consolas', 'Gabriola', 'Arial', 'Lucida Fax', 'SWIsot1', 'Tahoma', 'Microsoft YaHei', 'Solid Edge ISO3 Symbols', 'Times New Roman', 'Edwardian Script ITC', 'Solid Edge ANSI', 'SIEMENS_GOST Type A', 'SWGothi', 'Bell MT', 'SWGrekc', 'Calibri', 'Adobe Myungjo Std', 'Rockwell', 'Tahoma', 'SWGreks', 'Microsoft YaHei', 'Solid Edge ANSI', 'Showcard Gothic', 'Calibri', 'SWSimp', 'Bodoni MT', 'Californian FB', 'High Tower Text', 'Rockwell', 'Trebuchet MS', 'Century', 'Verdana', 'Solid Edge ANSI GDT Symbols', 'Calibri', 'Agency FB', 'Microsoft PhagsPa', 'Consolas', 'Dubai', 'Sitka Small', 'Verdana', 'Bodoni MT', 'Bodoni MT', 'Leelawadee UI', 'Bodoni MT', 'Microsoft JhengHei', 'MS Outlook', 'Calibri', 'Microsoft Uighur', 'Solid Edge ISO CE', 'Gill Sans MT', 'Arial', 'Myanmar Text', 'Lucida Fax', 'Segoe UI', 'Arial', 'Franklin Gothic Book', 'Solid Edge GOST1 Symbols', 'Agency FB', '3ds', 'HoloLens MDL2 Assets', 'Palatino Linotype', 'Cambria', 'SWItal', 'Times New Roman', 'Solid Edge ISO3 Symbols', 'Lucida Fax', 'Microsoft JhengHei', 'Sylfaen', 'Bookman Old Style', 'MingLiU-ExtB', 'Vivaldi', 'Calisto MT', 'Calisto MT', 'Adobe Arabic', 'Lucida Sans Typewriter', 'Kunstler Script', 'Eras Light ITC', 'Microsoft Sans Serif', 'Book Antiqua', 'Adobe Hebrew', 'OCR A Extended', 'Century Schoolbook', 'Wingdings', 'Segoe UI', 'Jokerman', 'Arial', 'Lucida Sans Unicode', 'Century Schoolbook', 'Bodoni MT', 'Eras Light ITC', 'Candara', 'MingLiU-ExtB', 'Palatino Linotype', 'Californian FB', 'Corbel', '3DS Fonticon', 'Eras Demi ITC', 'Franklin Gothic Medium', 'Arial', 'SWMusic', 'Ink Free', 'Gill Sans MT', 'Cambria', 'Courier New', 'IGES 1001', 'Segoe Print', 'Gill Sans Ultra Bold', 'Algerian', 'Wide Latin', 'SWItalt', 'Comic Sans MS', 'Jokerman', 'Constantia', 'SWRomnc', 'Segoe UI', 'Leelawadee', 'Juice ITC', 'Leelawadee', 'Segoe UI', 'Curlz MT', 'Rockwell Condensed', 'Candara', 'Californian FB', 'Courier New', 'Bookman Old Style', 'Rockwell', 'Lucida Bright', 'Microsoft JhengHei', 'Poor Richard', 'Britannic Bold', 'Bodoni MT', 'Lucida Sans', 'Gigi', 'Franklin Gothic Medium Cond', 'Rockwell Condensed', 'Bell MT', 'SWComp', 'Rockwell', 'Solid Edge ANSI Unicode', 'Tw Cen MT', 'SWIsot2', 'Webdings', 'Bodoni MT', 'Rockwell', 'SWItalc', 'Wingdings 2', 'Franklin Gothic Book', 'Tw Cen MT Condensed', 'Arial', 'Century Schoolbook', 'Microsoft Tai Le', 'Nirmala UI', 'Leelawadee UI', 'Elephant', 'PDM', 'Franklin Gothic Book', 'Candara', 'Myriad Pro', 'Magneto', 'SolidWorks GDT', 'Candara', 'SimSun', 'Solid Edge ANSI3 Symbols', '3DS Fonticon', 'Constantia', 'SEGDT', 'Ebrima', 'SimSun-ExtB', 'OLF SimpleSansOC', 'Juice ITC', 'SWRomnd', 'Microsoft Uighur', 'Book Antiqua', 'Matura MT Script Capitals', 'Corbel', 'Gill Sans MT', 'Bodoni MT', 'Engravers MT', 'Century Gothic', 'Impact', 'Franklin Gothic Demi Cond', 'Adobe Thai', 'Maiandra GD', 'Gill Sans MT Condensed', 'Lucida Handwriting', 'Microsoft New Tai Lue', 'Solid Edge ISO2 Symbols', 'Solid Edge ISO', 'Comic Sans MS', 'Perpetua', 'Segoe UI', 'Dubai', 'Corbel', 'Book Antiqua', 'Bell MT', 'SWGothg', 'Solid Edge ANSI', 'Agency FB', 'Comic Sans MS', 'Segoe UI Symbol', 'Tw Cen MT', 'Sitka Small', 'Solid Edge ISO Unicode', 'Courier New', 'Chiller', 'SEMonotxt', 'Tw Cen MT', 'TeamViewer15', 'MS Reference Sans Serif', 'Franklin Gothic Demi', 'Bodoni MT', 'Arial', 'Tahoma', 'Segoe UI', 'Solid Edge ISO GDT Symbols', 'Georgia', 'Georgia', 'Rockwell Extra Bold', 'Rage Italic', 'Segoe Script', 'Malgun Gothic', 'Arial', 'Sitka Small', 'Calibri', 'Bradley Hand ITC', 'Impact', 'SWGrekc', 'Malgun Gothic', 'Lucida Bright', 'Solid Edge ISO Unicode', 'Elephant', 'Leelawadee UI', 'Ebrima', 'Microsoft Yi Baiti', 'Goudy Old Style', 'Courier New', 'Palace Script MT', 'Sitka Small', 'Solid Edge GOST1 Symbols', 'Segoe UI', 'Monotype Corsiva', 'Calibri', 'Consolas', 'Tw Cen MT Condensed', 'Times New Roman', 'Courier Std', 'Lucida Sans Typewriter', 'MV Boli', 'SWLink', 'Century Schoolbook', 'Solid Edge ANSI Unicode', 'Script MT Bold', 'Tw Cen MT', 'Bodoni MT', 'Mongolian Baiti', 'Calibri', 'Perpetua Titling MT', 'SWIsop1', 'Calisto MT', 'SERomanc', 'Javanese Text', 'Eras Demi ITC', 'Franklin Gothic Heavy', 'Bodoni MT', 'Centaur', 'MS Reference Specialty', 'Lucida Sans', 'SWScrps', 'Tw Cen MT Condensed Extra Bold', 'Arial', 'Solid Edge ISO', 'Snap ITC', 'Century Gothic', 'Century Schoolbook', 'Solid Edge ISO Unicode', 'Papyrus', 'Solid Edge ISO Unicode', 'Segoe UI', 'Goudy Stout', 'Adobe Ming Std', 'Corbel', 'Solid Edge ISO1 Symbols', 'Verdana', 'MS Outlook', 'Verdana', 'Myanmar Text', 'Microsoft Uighur', 'SWIsot2', 'Bodoni MT', 'Parchment', 'Bradley Hand ITC', 'HYSWLongFangSong', 'High Tower Text', 'Bodoni MT', 'Wingdings 3', 'SESimplex', 'IGES 1002', 'SWTxt', 'SIEMENS_GOST Type A', 'Malgun Gothic', 'Trebuchet MS', 'Solid Edge Stencil', 'Helvetica-Narrow', 'Nirmala UI', 'Solid Edge ANSI Unicode', 'Calibri', 'Sitka Small', 'Nirmala UI', 'Arial Rounded MT Bold', 'Microsoft Sans Serif', 'Adobe Thai', 'Yu Gothic', 'Ebrima', 'Imprint MT Shadow', 'Comic Sans MS', 'Goudy Old Style', 'SWMeteo', 'Microsoft Uighur', 'Gloucester MT Extra Condensed', 'Perpetua', 'Adobe Hebrew', 'SWMath', 'Monotype Corsiva', 'Solid Edge ANSI Unicode', 'Bodoni MT', 'Mistral', 'Harrington', 'Courier New', 'SWItalt', 'Georgia', 'Times New Roman', 'Franklin Gothic Heavy', 'Bookman Old Style', 'Nirmala UI', 'Solid Edge ISO', 'Gill Sans MT Ext Condensed Bold', 'Segoe UI', 'Algerian', 'SWRomns', 'Palatino Linotype', 'Magneto', 'SWGothg', 'Gill Sans Ultra Bold Condensed', 'Microsoft PhagsPa', 'Dubai', 'Bernard MT Condensed', 'Myanmar Text', 'Comic Sans MS', 'Berlin Sans FB Demi', 'Modern No. 20', 'Adobe Pi Std', 'Rockwell Condensed', 'Solid Edge ISO Unicode', 'Arial', 'Cambria', 'SolidWorks GDT', 'Solid Edge ISO', 'SWIsot3', 'Californian FB', 'SWGothe', 'Segoe UI', 'IGES 1002', 'SWIsop3', 'SWRomnt', 'French Script MT', 'IGES 1003', 'SWGothi', 'Segoe UI', 'Bookshelf Symbol 7', 'Rockwell', 'Arial', 'Gadugi', 'Dubai', 'Segoe Script', 'SERomans', 'Microsoft New Tai Lue', 'Adobe Hebrew', 'Britannic Bold', 'Playbill', 'Gloucester MT Extra Condensed', 'Stencil', 'Solid Edge ANSI', 'Franklin Gothic Book', 'Bodoni MT', 'Courier Std', 'Calisto MT', 'Haettenschweiler', 'Gill Sans MT Condensed', 'Constantia', 'Garamond', 'Goudy Old Style', 'Bernard MT Condensed', 'Lucida Sans', 'Javanese Text', 'Papyrus', 'Imprint MT Shadow', 'Palatino Linotype', 'MS Gothic', 'Solid Edge ISO Unicode', 'Informal Roman', 'Webdings', 'Sitka Small', 'Microsoft Tai Le', 'Footlight MT Light', 'Ravie', 'Book Antiqua', 'Trebuchet MS', 'Myriad CAD', 'Leelawadee UI', 'Calibri', 'Agency FB', 'Candara', 'SWSimp', 'Lucida Sans Typewriter', 'Dubai', 'Adobe Thai', 'Yu Gothic', 'SWIsop3', 'Franklin Gothic Demi Cond', 'Comic Sans MS', 'Franklin Gothic Medium Cond', 'Cooper Black', 'Century Schoolbook', 'Microsoft Tai Le', 'SEMonotxt', 'Haettenschweiler', 'Adobe Song Std', 'Century Schoolbook', 'SWGDT', 'Adobe Arabic', 'Candara', 'Solid Edge ANSI Unicode', 'SWItal', 'Franklin Gothic Medium', 'Leelawadee', 'Perpetua', 'SERomans', 'Viner Hand ITC', 'Segoe UI', 'Chiller', 'Felix Titling', 'Candara', 'SWTxt', 'Symbol', 'Lucida Sans Typewriter', 'Footlight MT Light', 'HYSWLongFangSong', 'TeamViewer15', 'SWIsot1', 'Solid Edge ANSI1 Symbols', 'Malgun Gothic', 'Bodoni MT', 'SWMap', 'Harrington', 'Corbel', 'Helvetica-Narrow', 'Perpetua Titling MT', 'Solid Edge ANSI3 Symbols', 'Informal Roman', 'Solid Edge ANSI', 'Calisto MT', 'Courier Std', 'Niagara Solid', 'Bell MT', 'Niagara Engraved', 'Microsoft New Tai Lue', 'SWGDT', 'Solid Edge ANSI1 Symbols', 'Segoe MDL2 Assets', 'Lucida Sans', 'SERomand', 'Corbel', 'Lucida Handwriting', 'Leelawadee UI', 'Segoe UI', 'Book Antiqua', 'Cambria', 'Georgia', 'Lucida Fax', 'Arial', 'Solid Edge ISO1 Symbols', 'Lucida Sans Typewriter', 'Stencil', 'Old English Text MT', 'Vladimir Script', 'Pristina', 'Bahnschrift', 'Solid Edge ISO CE', 'Microsoft Yi Baiti', 'Verdana', 'Tw Cen MT Condensed Extra Bold', 'Wingdings', 'SWRomnd', 'Gadugi', 'Lucida Calligraphy', 'Candara', 'Palatino Linotype', 'Copperplate Gothic Bold', 'OLF SimpleSansOC', 'Corbel', 'Baskerville Old Face', 'Solid Edge ANSI', 'Lucida Sans', 'Wide Latin', 'SWMusic', 'web-PDM', 'Segoe UI', 'Segoe UI', 'Helvetica-Narrow', 'Solid Edge ISO GDT Symbols', 'Segoe UI', 'Copperplate Gothic Light', 'Castellar', 'Solid Edge ANSI Unicode', 'Century Gothic', 'Sitka Small', 'Solid Edge ISO', 'Franklin Gothic Heavy', 'MS Reference Specialty', 'Arial', 'Segoe Print', 'Harlow Solid Italic', 'Bookman Old Style', 'Calibri', 'Segoe UI Historic', 'SWScrpc', 'Wingdings 2', 'High Tower Text', 'Century Schoolbook', 'Solid Edge ANSI2 Symbols', 'Kozuka Mincho Pr6N', 'Berlin Sans FB', 'SimSun', 'Bell MT', 'Perpetua', 'Franklin Gothic Demi', 'Mongolian Baiti', 'Segoe Script', 'Garamond', 'Berlin Sans FB Demi', 'Corbel', 'Georgia', 'SWAstro', 'Segoe UI', 'Harlow Solid Italic', 'Book Antiqua', 'HoloLens MDL2 Assets', 'Palatino Linotype', 'Georgia', 'Segoe UI', 'Helvetica-Narrow', 'Goudy Old Style', 'Perpetua Titling MT', 'Trebuchet MS', 'SEGDT', 'Trebuchet MS', 'SWComp', 'SWScrps', 'Century Gothic', 'Constantia', 'Lucida Bright', 'SWGothe', 'Calisto MT', 'Consolas', 'SETxt', 'SWRomnt', 'Rockwell Condensed', 'Bodoni MT', 'Candara', 'Bookman Old Style', 'Cambria', 'Constantia', 'Rage Italic', 'Tw Cen MT', 'Berlin Sans FB', 'Curlz MT', 'Century Gothic', 'Elephant', 'Adobe Arabic', 'Solid Edge Stencil', 'Myanmar Text', 'Franklin Gothic Demi', 'Kristen ITC', 'Bauhaus 93', 'Solid Edge ANSI GDT Symbols', 'Cambria', 'Adobe Heiti Std', 'Calisto MT', 'Arial', 'Eras Medium ITC', 'Helvetica-Narrow', 'SWMeteo', 'Yu Gothic', 'Solid Edge ISO', 'Century Gothic', 'Century Gothic', 'Candara', 'Kozuka Gothic Pr6N', 'Gill Sans MT', 'Lucida Console', 'Poor Richard', 'Arial Rounded MT Bold', 'SWRomns', 'Times New Roman', 'Segoe UI Emoji', 'Berlin Sans FB', 'Lucida Fax', 'Constantia', 'Gill Sans Ultra Bold', 'Perpetua', 'Sylfaen', 'SWMath', 'Times New Roman', 'Courier Std', 'Bodoni MT', 'Bookman Old Style', 'Corbel', 'Georgia', 'Segoe MDL2 Assets', 'SERomand', 'Palatino Linotype', 'Adobe Hebrew', 'Verdana', 'Gill Sans MT', 'IGES 1003', 'Centaur', 'French Script MT', 'Microsoft YaHei', 'Colonna MT', 'Marlett', 'Vivaldi', 'SWIsop2', 'Nirmala UI', 'MS Reference Sans Serif', 'Century', 'Segoe UI', 'Dubai', 'Helvetica-Narrow', 'Malgun Gothic', 'Bauhaus 93', 'Colonna MT', 'Adobe Thai', 'MS Gothic', 'MT Extra', 'Segoe Print', 'Segoe UI Emoji', 'Lucida Bright', 'Kunstler Script', 'Calisto MT', 'Lucida Bright', 'Ravie', 'Helvetica-Narrow', 'Microsoft PhagsPa', 'SWAstro', 'Broadway', 'Solid Edge ISO', 'MV Boli', 'Eras Medium ITC', 'Kristen ITC', 'Lucida Sans', 'Segoe UI', 'Microsoft PhagsPa', 'Arial', 'Matura MT Script Capitals', 'Bookman Old Style', 'Tw Cen MT', 'Solid Edge ANSI Unicode', 'Mistral', 'MT Extra', 'Yu Gothic', 'SWScrpc', 'Lucida Bright', 'Perpetua Titling MT', 'Elephant', 'Arial', 'Comic Sans MS', 'OCR A Extended', 'SWLink', 'Arial', 'Lucida Fax', 'Microsoft JhengHei', 'Gabriola', 'Parchment', 'Consolas', 'Palace Script MT', 'Garamond', 'Edwardian Script ITC', 'SimSun-ExtB', 'Corbel', 'Rockwell', 'Ebrima', 'Goudy Stout', 'Modern No. 20', 'Bahnschrift', 'Copperplate Gothic Bold', 'Solid Edge ISO', 'Times New Roman', 'Yu Gothic', 'Eras Bold ITC', 'Rockwell', 'Sitka Small', 'Microsoft YaHei', 'Calibri', 'Consolas', 'Solid Edge ISO Unicode', 'Book Antiqua', 'web-PDM']
mpl.rcParams['font.family'] = 'Calibri'


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

    def __init__(self, df, plot_type, y_axis, source, name, legend_labels):
        # So most of the chart layout values are the same for both types of graph and they are calculated below
        self.name = name  # Chart name
        self.labels = df.index  # Ticker names
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
        self.t = self.ax.text(0.9, 0.01, f'Source: {source} Date: {datetime.today().date().strftime("%d.%m.%Y")}',
                              ha='right',
                              fontsize=TEXT_FONT)
        plt.title(name, loc='left')  # set chat name

        # If legend_labels is nothing, use default field values, which are column names
        if legend_labels[0] == '':
            self.legend_labels = df.columns
        else:
            self.legend_labels = legend_labels

        # Figure borders
        self.ax.spines[['top', 'right', 'left']].set_visible(False)

        # Where to show y-axis, default l
        if y_axis == 'r': self.ax.tick_params(labelright=True, right=True, labelleft=False, left=False)
        if y_axis == 'b': self.ax.tick_params(labelright=True, right=True)

        # Stacked BarChart Settings
        if plot_type == 's':
            self.align = 'center'
            self.y_offset = np.zeros(self.n_tickers)  # distance at which next bar should be placed if stacked plot
        else:
            self.y_offset = None
            self.align = 'edge'

        self.default_settings = {'align': self.align, 'edgecolor': 'white', 'linewidth': 1}

        list_of_labels = self.ax.get_xticklabels(which='major')
        render = self.fig.canvas.get_renderer()
        self.legend_y_pos = 0
        for l in list_of_labels:
            bbox = l.get_window_extent(render)
            bbox = self.ax.transData.inverted().transform(bbox)
            self.legend_y_pos = min(self.legend_y_pos, bbox[0][1])

        _, self.right = self.ax.get_xlim()

    def plot_scatter(self, data, date_range):
        names = ['min', 'max', 'avg']
        markersize = [16, 16, 12]
        transparency = [1, 1, .5]

        all_bars = []
        for i in range(1, self.n_fields + 1):
            for y in self.bar_group_position:
                all_bars.append(y + self.size * (i - 0.5))
        all_bars = sorted(all_bars)
        scatter_points = []

        if isinstance(self, HorizontalBarChart):
            markers = ['|', '|', 'D']
            for idx, df in enumerate(data):
                tmp_df = df.stack().reset_index()
                scatter_points.append(self.ax.scatter(tmp_df[0], all_bars, zorder=2,
                                                      color=scatter_colors[idx],
                                                      marker=markers[idx],
                                                      alpha=transparency[idx],
                                                      label=names[idx],
                                                      s=markersize[idx]))
        else:
            markers = ['_', '_', 'D']
            for idx, df in enumerate(data):
                tmp_df = df.stack().reset_index()
                scatter_points.append(self.ax.scatter(all_bars, tmp_df[0], zorder=2,
                                                      color=scatter_colors[idx],
                                                      marker=markers[idx],
                                                      alpha=transparency[idx],
                                                      label=names[idx],
                                                      s=markersize[idx]))

        self.date_range_text = self.ax.text(self.right, self.legend_y_pos - 0.6,
                                            f'Date Range {date_range[0].strftime("%d.%m.%Y")} - {date_range[1].strftime("%d.%m.%Y")}',
                                            ha='right', fontsize=TEXT_FONT)
        self.ax.legend(scatter_points, names, loc=1, frameon=False)
        self.ax.add_artist(self.main_legend)

    def plot_bar_value(self, display_value):
        """
        plots bar values
        :param display_value: string
        :return:
        """
        if display_value.lower() == 'o':
            for container in self.ax.containers:
                self.ax.bar_label(container, fmt='%.1f', padding=3)

    def save_plot(self, path='charts/211021/'):
        self.fig.savefig(path + self.name + '.png', bbox_inches='tight', transparent=True)
        plt.close(self.fig)


class HorizontalBarChart(BarChart):
    def __init__(self, df, plot_type, y_axis, source, name, legend_labels):
        super().__init__(df, plot_type, y_axis, source, name, legend_labels)

        self.scatter_location = []

        y_locations = self.initial_location
        plt.grid(b=True, which='major', axis='x', color='grey', alpha=.5)
        for i, col in enumerate(df.columns, 1):
            self.scatter_location.append(y_locations)
            self.ax.barh(y_locations, df[col], height=self.size, label=col, left=self.y_offset, color=MPL_COLORS[i],
                         **self.default_settings)
            if plot_type == 's':
                self.y_offset += df[col]
            else:
                y_locations = self.bar_group_position + self.size * i

        # self.ax.legend(loc='lower left', bbox_to_anchor=(0, -0.14), ncol=5, frameon=False)
        if plot_type == 's':
            plt.yticks(self.initial_location, self.labels, fontsize=TICKER_NAME_SIZE)
        else:
            plt.yticks(self.label_position, self.labels, fontsize=TICKER_NAME_SIZE)
        self.main_legend = self.ax.legend(loc='lower left', bbox_to_anchor=(0, -0.14), ncol=5, frameon=False,
                                          labels=self.legend_labels)

        plt.axvline(0, color='black', linewidth=0.5)
        plt.xticks(fontsize=TICK_SIZE)


class VerticalBarChart(BarChart):
    def __init__(self, df, plot_type, y_axis, source, name, legend_labels):
        super().__init__(df, plot_type, y_axis, source, name, legend_labels)

        x_location = self.initial_location
        plt.grid(b=True, which='major', axis='y', color='grey', alpha=.5)
        plt.axhline(0, color='black', linewidth=0.5)

        for i, col in enumerate(df.columns, 1):
            self.ax.bar(x_location, df[col], width=self.size, label=col, bottom=self.y_offset,
                        color=MPL_COLORS[i], **self.default_settings)
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

        if plot_type == 's':
            plt.xticks(self.initial_location, self.labels, rotation=rotation, fontsize=TICKER_NAME_SIZE)
        else:
            plt.xticks(self.label_position, self.labels, rotation=rotation, fontsize=TICKER_NAME_SIZE)

        self.main_legend = self.ax.legend(loc='lower left', bbox_to_anchor=(0, -0.2), ncol=5, frameon=False,
                                          labels=self.legend_labels)

        self.t.set_position((self.right, self.legend_y_pos - 0.4))
        # self.date_range_text.set_position((self.right, self.legend_y_pos - 0.6))
        plt.yticks(fontsize=TICK_SIZE)


def get_excel(path='BarLoader_B.xlsx'):
    r"""
    Reads and parse excel spreadsheet
    you can specify absolute path like C:\Users\yourusername\desktop\BarLoader.xlsx
    or simply BarLoader.xlsx if excel and python file are in the same folder
    :param path: str, path to a file
    :return: DataFrame representation of excel
    """

    # Get Data from excel , dtype={'date': datetime}
    df = pd.read_excel(path, nrows=23)  # remove nrows once we finish
    chart_related_columns = ['plot_type', 'orientation', 'sorting', 'y_axis']

    # In casse if you pressed spacebar in a cell, replace it with nothing
    df[chart_related_columns] = df[chart_related_columns].replace(to_replace='\s+', value='', regex=True)
    # replacing empty cell values with default values for corresponding column
    df = df.replace({pd.NA: '', pd.NaT: '', np.NaN: ''})
    df = df.replace({'plot_type': {'': 'b'},
                     'orientation': {'': 'h'},
                     'sorting': {'': 'no'},
                     'y_axis': {'': 'l'},
                     'display_value': {'': 'x'}})
    return df


def get_date(your_input):
    """
    Calculates date days/months/years ago
    :param your_input: str
    :return: new date 'YYYY-MM-DD'
    """
    if type(your_input) == str and your_input[-1] in ['d', 'm', 'y', 'D', 'M', 'Y']:
        today = date.today()
        if your_input.lower() == 'ytd':
            return date(today.year, 1, 1)
        number = int(your_input[:-1])
        if your_input[-1] == 'd':
            result = today - relativedelta(days=number)
        if your_input[-1] == 'm':
            result = today - relativedelta(months=number)
        if your_input[-1] == 'y':
            result = today - relativedelta(years=number)
        return result
    else:
        return pd.to_datetime(your_input).date()


def get_tickers(row):
    """
    Loops over columns if columns name starts with ticker and cell has value in it, add that value to the list, and add
    value from next cell (ticker name) to the dictionary
    :param row: DataFrame row
    :return: list of ticers, dictionary {ticker: ticker_name}
    """
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
    """
    loops over columns, if column name starts with field, it will take field(s) from that cell, and override value
    from next column
    :param row: DataFrame row
    :return: list of strings [fields], list of dictionaries {override: override_value}
    """
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
    # if overrides == []: overrides = [{}]
    return fields, overrides


def get_data(ticker, fields, override, legend_labels, sort):
    """
    Downloads data using blp.bpd
    :param legend_labels: list[string], your name for fields
    :param ticker: str/list, ticker(s) name(s)
    :param fields: str/list, field(s) name(s)
    :param override: dictionary, override values
    :param sort: string, sort value if needed
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

    if sort == 'a':
        data.sort_values(by=data.columns[0], axis=0, inplace=True, ascending=True)
    if sort == 'd':
        data.sort_values(by=data.columns[0], axis=0, inplace=True, ascending=False)

    return data


def get_data_bdh(ticker, fields, start_date, end_date, override, legend_labels, sort):
    """
    Downloads data using blp.bph
    :param ticker: str/list, ticker(s) name(s)
    :param fields: str/list, field(s) name(s)
    :param start_date: datetime
    :param end_date: datetime
    :param override: dictionary (override_value: override_value)
    :param legend_labels: list[string], your name for fields
    :param sort: string, sort value if needed
    :return: data to plot
    """
    data = pd.DataFrame()
    min_max_avg = [pd.DataFrame(), pd.DataFrame(), pd.DataFrame()]
    final = []
    for idx, field in enumerate(fields):
        try:
            temp = blp.bdh(tickers=ticker, flds=field, start_date=start_date, end_date=end_date, **override[idx])
        except Exception as e:
            temp = blp.bdh(tickers=ticker, flds=field, start_date=start_date, end_date=end_date)
        data[legend_labels[idx]] = temp.iloc[-1].unstack()
        min_max_avg[0][legend_labels[idx]] = temp[ticker].min().unstack()
        min_max_avg[1][legend_labels[idx]] = temp[ticker].max().unstack()
        min_max_avg[2][legend_labels[idx]] = temp[ticker].mean().unstack()

    if sort == 'a':
        data.sort_values(by=data.columns[0], axis=0, inplace=True, ascending=True)
    if sort == 'd':
        data.sort_values(by=data.columns[0], axis=0, inplace=True, ascending=False)

    # print(min_max_avg[0])
    for df in min_max_avg:
        final.append(df.reindex(data.index))
    return data, final


def run():
    df = get_excel()
    for idx, row in df.iterrows():
        # if idx == 1:   #Select single row from Excel Input
        name = str(row['name'])
        fields, override = get_override(row)
        legend_labels = [i.strip() for i in row.legend_labels.split(',')]
        tickers, ticker_names = get_tickers(row)
        # if start_date provided, converts it to datetimem
        start_date = get_date(row.start_date) if row.start_date != '' else ''

        try:
            # if we have start date, use bdh
            if start_date != '':
                # if no end_date, set it to today
                if row.end_date == '':
                    end_date = date.today()
                # if there is end_date, convert it to datetime
                else:
                    end_date = get_date(row.end_date)
                data, scatter_data = get_data_bdh(tickers, fields, start_date, end_date, override, legend_labels,
                                                  row.sorting.lower())
                date_range = (start_date, end_date)
            # if we dont have start_date, use bdp
            else:
                data = get_data(tickers, fields, override, legend_labels, row.sorting.lower())
                scatter_data = None
                date_range = None
        except Exception as e:
            print(f'Exception: {e}\nError on downloading data: {name}')

        data.index = data.index.map(ticker_names)

        args = {'df': data, 'plot_type': row.plot_type.lower(),
                'y_axis': row.y_axis.lower(), 'source': row.source,
                'name': str(row['name']), 'legend_labels': legend_labels}

        if row.orientation.lower() == 'h':
            plot = HorizontalBarChart(**args)
        else:
            plot = VerticalBarChart(**args)
        if scatter_data: plot.plot_scatter(scatter_data, date_range)
        plot.plot_bar_value(row.display_value)

        print(idx, name, 'completed')
        plot.save_plot()


if __name__ == '__main__':
    run()
