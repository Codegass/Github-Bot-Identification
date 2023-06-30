from numpy import int32
import pandas as pd
import logging, re, time

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

if __name__ == "__main__":
    ## test the function ##
    repo_list = load_repo_list("data/repo_list_apache.csv")
    print(repo_list)