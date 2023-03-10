import glob
import os
import pandas as pd
import numpy as np #numpy
import scipy as scipy #scipy
from pathlib import Path
import matplotlib.lines as mlines #matplotlib
import matplotlib.pyplot as plt #matplotlib
plt.style.use('ggplot') #emulate ggplot from R
import services.create_trendlines as create_trendlines
import services.calculate_trendlines as calculate_trendlines
import services.calculate_data_change as calculate_data_change
#import services.save_plot_food_drop as save_plot

#Interval for analysis around food drop
interval = 300

#go through directory and act on files based on folder names
with pd.ExcelWriter('dat_photometry_food_drop_zscore.xlsx', mode='w') as writer:
    for folder in glob.iglob(('/home/jordan/Desktop/dat_photometry_data_to_analyze/*')):
        if 'drop' in folder:
            for file in glob.iglob(folder + '/*.csv'):
                if "405ch" not in file:
                    rawPhotometry = pd.read_csv(file)
                    autoFluorescence = pd.read_csv(file[:-4] + "_405ch.csv")

                    #make auto and npy column headings lowercase
                    autoFluorescence.columns = autoFluorescence.columns.str.lower()
                    rawPhotometry.columns = rawPhotometry.columns.str.lower()

                    #combine time column and auto, npy,  d0 columns to create master pandas DataFrame
                    master = pd.concat([autoFluorescence['time'], autoFluorescence['d0'], rawPhotometry['d0']], axis=1, keys = ['time', "auto" , "data", 'shock'])
                    
                    #create food/object drop onset
                    foodDropTime = int(file[file.rfind('_')+1:-4])
                    #create begin_input 
                    begin_input = foodDropTime - interval #IMPORTANT - can change number to any number of rows before drop onset

                    #create last_row
                    last_row = foodDropTime + interval

                    #create master_input pandas DataFrame
                    master_input = master[(master['time']>= foodDropTime-interval) & (master['time']<= foodDropTime+interval)]
                
                    master_trendlines = create_trendlines.calculate_trend_lines(master_input, begin_input, foodDropTime)
                    
                    #determine trendline equeation
                    trendline_equation_auto, a, b = create_trendlines.determine_trendline_equation(master_trendlines, "auto")
                    trendline_equation_data, c, d = create_trendlines.determine_trendline_equation(master_trendlines, "data")

                    """
                    #create auto scatter plot with auto linear trendline
                    plt.scatter(master_trendlines.x, master_trendlines.auto, color = 'blue', s = 20)
                    auto_trendline_values = np.polyval([a,b], master_trendlines.x)
                    plt.plot(master_trendlines.x, auto_trendline_values, linewidth = 3, color = 'red')
                    #plt.title(auto_linear_trendline_equation, fontsize = 10, y = 0.9)
                    plt.xlabel('x')
                    plt.ylabel('autofluorescence')
                    plt.show()
                    

                    #create npy scatter plot with npy linear trendline
                    plt.scatter(master_trendlines.x, master_trendlines.data, color = 'blue', s = 10)
                    npy_trendline_values = np.polyval([c,d], master_trendlines.x)
                    plt.plot(master_trendlines.x, npy_trendline_values, linewidth = 3, color = 'red')
                    #plt.title(npy_linear_trendline_equation, fontsize = 10, y = 0.9)
                    plt.xlabel('x')
                    plt.ylabel('npy')
                    plt.show()
                    """
                    
                    #perform master calculations
                    x_range_master_calculations, x_master_calculations, master_calculations = calculate_trendlines.create_master_calculations(master_input)

                    
                    #perform auto trendline
                    master_calculations = calculate_trendlines.create_auto_trendline(x_range_master_calculations, master_calculations, a,b, "auto")
                    master_calculations = calculate_trendlines.create_auto_trendline(x_range_master_calculations, master_calculations, a,d, "data")

                    #subtract trendlines
                    master_calculations = calculate_trendlines.subtract_trendlines(master_calculations, d)
                
                    #calculate zscore
                    master_calculations = calculate_data_change.calculate_ind_z_score_food_drop(master_calculations, foodDropTime, interval, file[file.rfind('/')+1:])
                    
                    if "food" in file[file.rfind('/')+1:]:
                        master_calculations.to_excel(writer, sheet_name="food", columns=[file[file.rfind('/')+1:]], index=False)

                    elif "object" in file[file.rfind('/')+1:]:
                        master_calculations.to_excel(writer, sheet_name="object", columns=[file[file.rfind('/')+1:]], index=False)
                        

                    




                


                    
                

