import numpy as np
import pandas as pd
from rich.progress import track
import logging, re, time, csv, os, sys
import argparse

def load_repo_list(filename, org="apache"):
    '''
    This function is sepicific to the repo_list_<xxxx>.csv file
    this csv has a special format:
    project: this is the full name of the project
    github_repo_name: **default is 0**. this is the link to the github repo
    notes: just the comments for mannul review
    '''
    df = pd.read_csv(filename, dtype={'github_repo_name': str})
    repo_list = []
    for index, row in df.iterrows():
        if row['github_repo_name'] == "0":
            repo_list.append(org + "/" + row['project'].lower())
        elif row['github_repo_name'] == "-1":
            pass
        else:
            repo_list.append(org + "/" + row['github_repo_name']) 
    return repo_list

def logger_setup(logger_name, log_file_name, TEST):
    '''
    This function is to setup the logger.
    logger_name: the name of the logger
    log_file_name: the name of the log file
    TEST: if it is a test, then the logger will be set to DEBUG level
    '''
    
    logging.basicConfig(filename=log_file_name,level=logging.ERROR, filemode="w", format="%(name)s:%(levelname)s - %(asctime)s:%(message)s", datefmt="%d-%m-%Y %H-%M-%S")
    
    # logger handler for different out in the file and console
    handler_console = logging.StreamHandler() # stdout to console
    handler_console.setLevel(logging.DEBUG)
    handler_file = logging.FileHandler(log_file_name) # stdout to file
    if TEST:
        handler_file.setLevel(logging.DEBUG)
    else:
        handler_file.setLevel(logging.ERROR)

    # formatter for the logs
    formatter = logging.Formatter('%(name)s:%(levelname)s - %(asctime)s:%(message)s', datefmt="%d-%m-%Y %H-%M-%S")
    handler_console.setFormatter(formatter)
    handler_file.setFormatter(formatter)

    # add the handlers to the logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler_console)
    logger.addHandler(handler_file)

    return logger

def d3_chord_diagram(df):
    pass

def data_correction(raw_df):
    ''' 
    The raw data set collected from the github API has some kind of issues.
    It will sometimes has an illegal character in the string, which will cause the
    break of the csv file. This function is to check if there is any illegal character in the string
    and try to fix it.
    
    Input: Raw Data df
    Output: Fixed Data df
    '''
    import warnings
    warnings.filterwarnings('ignore')

    fixed_df = pd.DataFrame(columns=raw_df.columns)
    buffer_row = None
    # iterate through the df
    for index, row in track(raw_df.iterrows(), description="Bot identification...", total=raw_df.shape[0]):

        if buffer_row is not None:
            # check if the row has the right number of columns
            
            if np.isnan(buffer_row['Bot']):
                data = [buffer_row.dropna().tolist(), row.dropna().tolist()]
                print(buffer_row)
                # Concatenate the rows
                concatenated_data = [x for sublist in data for x in sublist]
                # if not, then attach the row to the buffer row
                buffer_row = pd.DataFrame([concatenated_data], columns=raw_df.columns)
                # set column type
                buffer_row['Bot'] = buffer_row['Bot'].astype(float)
                # merge the new row
                fixed_df = pd.concat([fixed_df, buffer_row], ignore_index=True)
                buffer_row = None
            else:
                # if the row has the right number of columns, then append the buffer row
                fixed_df = fixed_df._append(buffer_row)
                buffer_row = row
        else:
            buffer_row = row
    
    # append the last buffer row
    if buffer_row is not None:
        fixed_df = fixed_df._append(buffer_row)

    return fixed_df

def main(file_path):
    df = pd.read_csv(file_path, low_memory=False)
    corrected_df = data_correction(df)
    corrected_df.to_csv(file_path[:-4]+"_fixed.csv", index=False)

if __name__ == "__main__":
    ## test the function ##
    
    # NeedFixFilePath = "data/results/collected_data_one_year_microsoft_May1st-3.csv"
    # df = pd.read_csv(NeedFixFilePath,low_memory=False)
    # data_correction(df).to_csv(NeedFixFilePath[:-4]+"_fixed.csv", index=False)

    parser = argparse.ArgumentParser(description="Process and correct data in a given csv file.")
    parser.add_argument("file_path", help="The path to the file to be corrected.")
    args = parser.parse_args()

    main(args.file_path)