import pandas as pd
from pylab import *


def calculate_trend_lines(master_input, begin_input, drop_onset):
    #create master_trendlines pandas DataFrame
    master_trendlines = master_input.loc[begin_input:drop_onset - 1]
    #reset master_trendlines row index 
    master_trendlines = master_trendlines.reset_index(drop = True)
    #create x_master_trendlines (ranging from 1 to # rows in master_trendlines) pandas DataFrame
    x_range_master_trendlines = master_trendlines.axes[0] - (master_trendlines.axes[0][0] - 1)
    x_master_trendlines = pd.DataFrame({'x': x_range_master_trendlines})
    #add x_master_trendlines to master_trendlines 
    master_trendlines = pd.concat([x_master_trendlines, master_trendlines], axis=1, join='inner') 
    return master_trendlines

def determine_trendline_equation(master_trendlines, data):
    if data == "auto":
        (a, b) = polyfit(master_trendlines.x, master_trendlines.auto, 1)
    else:
        (a, b) = polyfit(master_trendlines.x, master_trendlines.data, 1)
    return 'y = ' + str(round(a, 5)) + 'x + ' + str(round(b, 5))