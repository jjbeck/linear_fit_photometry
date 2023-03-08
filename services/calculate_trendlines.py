import pandas as pd
import numpy as np

def create_master_calculations(master_calculations):
    #reset master_calculations row index 
    master_calculations = master_calculations.reset_index(drop = True)
    #create x_master_calculations (ranging from 1 to # rows in master_calculations) pandas DataFrame
    x_range_master_calculations = master_calculations.axes[0] - (master_calculations.axes[0][0] - 1)
    x_master_calculations = pd.DataFrame({'x': x_range_master_calculations})
    #add x_master_calculations to master_calculations 
    master_calculations = pd.concat([x_master_calculations, master_calculations], axis = 1, join = 'inner') 

    return x_range_master_calculations, x_master_calculations, master_calculations

def create_auto_trendline(x_range_master_calculations, master_calculations, a, b, data):
    #create auto_trendline_y pandas DataFrame 
    data_list = []

    if data == "data":
        for x in x_range_master_calculations:
            y = a*x + b 
            data_list.append(y)
        data_array = np.array(data_list)
        data_trendline_y = pd.DataFrame({'auto_trendline_y': data_array})
        #add auto_trendline_y to master_calculations
        master_calculations = pd.concat([master_calculations, data_trendline_y], axis = 1, join = 'inner')
    else:
        for x in x_range_master_calculations:
            y = a*x + b 
            data_list.append(y)
        data_array = np.array(data_list)
        data_trendline_y = pd.DataFrame({'data_trendline_y': data_array})
        #add auto_trendline_y to master_calculations
        master_calculations = pd.concat([master_calculations, data_trendline_y], axis = 1, join = 'inner')
    
    return master_calculations

def subtract_trendlines(master_calculations, d):
    #subtract auto_trendline_y from auto to create auto_fit column in master_calculations
    master_calculations['auto_fit'] = master_calculations['auto'] - master_calculations['auto_trendline_y']
    #subtract gcamp_trendline_y from gcamp to create gcamp_fit column in master_calculations
    master_calculations['data_fit'] = master_calculations['data'] - master_calculations['data_trendline_y']

    #add gcamp_trendline y-intercept to auto_fit to create auto_fit column in master_calculations
    master_calculations['auto_final'] = d + master_calculations['auto_fit']
    #add gcamp_trendline y-intercept to gcamp_fit to create gcamp_fit column in master_calculations
    master_calculations['data_final'] = d + master_calculations['data_fit']

    return master_calculations