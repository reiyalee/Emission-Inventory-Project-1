# -*- coding: utf-8 -*-
"""
Created on Thu Jul 07 15:17:36 2016

@author: Yiting
"""

"""
This program is to reformat csv data, which would be used in ArcGIS
Main task:
(1) convert blank to -99999
(2) rename csv file
(3) make sure every csv file has TAZ
"""

import os

def ReformatCSV(path, county_name):
    """ Reformat CSV: convert blank in to -99999
        AND: reformat excel if it contain several spreadsheets, then save to csv
    INPUT: 
    path - csv path folder
    county_name - path folder name

    OUTPUT:
    revised csv file
    
    INSIDE FUNCTION:
    GetYear
    """
    import pandas
    import numpy
    import glob
    #--------------------------------------------------------------------------
    # file extension used to search .xls or .csv
    ext1='.csv'
    ext2='.xls'
    ext3='.xlsx'
    # parse all files in path
    for root, dirs_list, files_list in os.walk(path):
        for file_name in files_list:
            # (1) csv file process
            if os.path.splitext(file_name)[-1] == ext1: 
                file_name_path = os.path.join(root, file_name)
                print file_name_path
                
                # parse csv files in path folder
                for CSVfiles in glob.glob("*.csv"):
                    print CSVfiles
                    if len(CSVfiles) == 0:
                        break
                        print county_name + 'do not have csv data'
                    else:
                        print 'WOW'
                        # get year
                        year = GetYear(CSVfiles)
            
                        try:
                            # because ArcGIS will recognize Null
                            df = pandas.read_csv(CSVfiles)
                            # find TAZ column, convert it to 'TAZ'
                            df = df.rename(columns={df.columns[0]:u'TAZ'})
                            
                            # replace nan by -99999
                            df2 = df.replace('nan', -99999)   
                            #df3 = df2.replace(';TAZ' , 'TAZ')
                            
                            # output revised file
                            csv_name = county_name + "_" + year + '.csv'
                            
                            df2.to_csv(os.path.join(path, csv_name))
                            
                            print county_name + year + ' refomat csv success'
                            del year, csv_name
                            
                        except:
                            print county_name + year + " Reformat csv failed"
                            
            # (2) if data is .xls or .xlsx it will contain several spreadsheet
            else:
                if os.path.splitext(file_name)[-1] == ext3 \
                or os.path.splitext(file_name)[-1] == ext2:
                    file_name_path = os.path.join(root, file_name)
                    print file_name
                    print file_name_path
    #--------------------------------------------------------------------------
    # parse excel file, because it will have several spreadsheet
    #for XLSfiles in glob.glob('?.xls'):
        
    
                
def GetYear(file_name):
    """ get year number from file_name string and convert to format: 20xx
    note: make sure file_name is STRING
    (1) extract all number from file name
    (2) one number? => this is year 
    (3) several number? => find the first 2 or 4-digit number as year
    """
    import re
    # extract number from file name
    YearNum = re.findall("\d+", file_name)
    # if YearNum only has one result, it is year number
    if len(YearNum) == 1:
        if len(YearNum[0]) == 2:
            year = '20' + YearNum[0]
        else:
            year = YearNum[0]
    # if YearNum has several results, find the first 2 or 4-digit number
    else:
        for YN in YearNum:
            # first 2-digit number, and than exit parse number in YearNum
            if len(YN) == 2:
                year = '20' + YN
                break
            elif len(YN) == 4:
                year = YN
                break                    
            else:
                pass
            
    # return value year is string                    
    return(year)    
    
# test excuate
path = r'f:/old_emission_inventory\Spatial_Contract\SE_data\fresno'
os.chdir(path)
county_name = "fresno"

ReformatCSV(path, county_name)
