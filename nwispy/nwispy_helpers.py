# -*- coding: utf-8 -*-
"""
:Module: helpers.py

:Author: Jeremiah Lant
 
:Email: jlant@usgs.gov

:Purpose: 
Helper functions for the various modules. 

"""
import os
import numpy as np
import datetime
import re

def get_filepaths(directory, file_ext = None):
    """    
    Return a list of full file paths from a directory including its subdirectories.
        
    *Parameters:*
        directory : string path 
      
    *Return:*
        file_paths : list of full file paths from a directory
        
    """     
    file_paths = []  

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath) 

    # if user wants on certain file extentions then only include those paths by removing unwanted paths
    if file_ext:
        for f in file_paths:
            if not f.endswith(file_ext):
                file_paths.remove(f)

    return file_paths

# Run the above function and store its results in a variable.   
full_file_paths = get_filepaths("/Users/johnny/Desktop/TEST")



def get_current_date_time():
    """    
    Return current date and time in a format that can be used as a file name.
    
    Example:
        str(datetiem.datetime.today()) = "2014-03-14 16:46:14.079000"
    
        date_time = "2014-03-14_16.46.14"
        
    *Parameters:*
        none
      
    *Return:*
        date_time : string of date and time
        
    """  
    pattern = "([0-9]{4}-[0-9]{1,2}-[0-9]{1,2})\s([0-9]{1,2}):([0-9]{1,2}):([0-9].+)"    
    
    today_str = str(datetime.datetime.today())
    
    match = re.search(pattern, today_str)

    year_month_day = match.group(1)
    hour = match.group(2)    
    minute = match.group(3)
    second = match.group(4)

    hour_minute_second = ".".join([hour, minute, second])

    date_time = "_".join([year_month_day, hour_minute_second])

    return date_time

def get_filedir_filename(path):
    """    
    Get file directory and name from a file path.
    
    *Parameters:*
        path: string path name
      
    *Return:*
        filedir : string file directory path
        filename : string file name
        
    """ 
    filedir, filename = os.path.split(path)
    
    # filedir is an empty string when file f is in current directory 
    if not filedir: 
        filedir = os.getcwd()

    return filedir, filename

def make_directory(path, directory_name):
    """    
    Make an output directory.
    
    *Parameters:*
        path: string path name
        directory_name : string directory name
      
    *Return:*
        directory_path : string path to directory 
        
    """    
    directory_path = '/'.join([path, directory_name])  
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)         
    
    return directory_path

def is_float(value):
    """   
    Determine if string value can be converted to a float. Return True if
    value can be converted to a float and False otherwise.
    
    *Parameters*:
        value: string
        
    *Return*:
        boolean
        
    """
    
    try:
        float(value)
        return True
        
    except ValueError:
        return False

def subset_data(dates, data, start_date, end_date):
    """   
    Subset the *dates* and *data* arrays to match the range of the *start_date*
    and *end_date*. If *start_date* and *end_date* are not within the range of dates
    specified in *dates*, then the *start_date* and *end_date* are set to the
    first and last dates in the array *dates*.
            
    *Parameters:*  
        dates :  array of dates as datetime objects 
        
        data : array of data
        
        start_date : datetime object
        
        end_date : datetime object
    
    *Return:*
        data : dictionary holding arrays of date and data subset

    """ 
    if len(dates) != len(data):
        raise ValueError("Lengths of dates and data are not equal!")
        
    else:
        # if start_date or end_date are not within dates, set them to the 
        # first and last elements in dates
        if start_date < dates[0] or start_date > dates[-1]:
            start_date = dates[0]  
        
        if end_date > dates[-1] or end_date < dates[0]:
            end_date = dates[-1] 
            
        # find start and ending indices; have to convert idx from array to int to slice
        start_idx = int(np.where(dates == start_date)[0])
        end_idx = int(np.where(dates == end_date)[0])
        
        # subset variable and date range; 
        date_subset = dates[start_idx:end_idx + 1] 
        data_subset = data[start_idx:end_idx + 1] 
        
        # put data into a dictionary
        data = {
            'dates': date_subset, 
            'data': data_subset
        }    
        
        return data

def find_start_end_dates(model_dates, observed_dates):
    """  
    Find start and end dates between two different sized arrays of datetime
    objects.

    *Parameters:*  
        model_dates : array of datetime objects
        
        observed_dates : array of datetime objects
    
    *Return:*
        overlap_dates : array of datetime objects

    """ 
    # pick later of two dates for start date; pick earlier of two dates for end date
    if observed_dates[0] > model_dates[0]: 
        start_date = observed_dates[0]         
    else:
        start_date = model_dates[0]
    
    if observed_dates[-1] >  model_dates[-1]: 
        end_date = model_dates[-1]        
    else:
        end_date = observed_dates[-1]
                
    return start_date, end_date

        
    
    