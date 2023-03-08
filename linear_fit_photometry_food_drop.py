import glob
import os
import pandas as pd
import numpy as np #numpy
import scipy as scipy #scipy
import services.create_trendlines as create_trendlines
#import services.save_plot_food_drop as save_plot

#Interval for analysis around food drop
interval = 300

#go through directory and act on files based on folder names
for folder in glob.iglob(('/home/jordan/Desktop/dat_photometry_data_to_analyze/*')):
    if 'drop' in folder:
        for file in glob.iglob(folder + '/*.csv'):
            if "405ch" not in file:
                rawPhotometry = pd.read_csv(file)
                print(file[file.rfind("/"):])
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
                master_input = master[begin_input:last_row]
                
                master_trendlines = create_trendlines.calculate_trend_lines(master_input, begin_input, foodDropTime)

                #determine trendline equeation
                trendline_equation_auto = create_trendlines.determine_trendline_equation(master_trendlines, "auto")

                trendline_equation_data = create_trendlines.determine_trendline_equation(master_trendlines, "data")
                print(trendline_equation_auto)
                print(trendline_equation_data)

                
            

