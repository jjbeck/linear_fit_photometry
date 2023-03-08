def calculate_df(master_calculations):
    #calculate delta f/f (dff) and create dff column in master_calculations
    master_calculations['dff']= ((master_calculations['data_final'] - master_calculations['auto_final'])/master_calculations['auto_final'])*100
    return master_calculations