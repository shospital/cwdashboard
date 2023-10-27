import os
import pandas as pd
from datetime import datetime

DATA_PATH = "/Users/sunbak/PolarWatch/codebase/cwdashboard"
CSV_FILE = "erddap_log.csv"

def get_log(path: str) -> pd.DataFrame:

    dfile = os.path.join(path, CSV_FILE)
    
    if not os.path.isfile(dfile):
        raise FileNotFoundError(f"CW ERROR: The file {dfile} does not exist.")

    df = pd.read_csv(dfile)

    if len(df) >= 1:
        # remove row with units
        df.drop(index=0, inplace=True)
    return df

def check_column_exists(df, col_name):
    if col_name not in df.columns:
        raise ValueError(f"Column '{col_name}' does not exist in the DataFrame.")

def get_summary(df: pd.DataFrame):
    print(df.describe())    

def cleanup_df(df):

# format datetime
    try:
        check_column_exists(df, 'time')  
    except ValueError as e:
        print(e)
    else:    
        df['newtime'] = pd.to_datetime(df['time'])
        df['year'], df['month'] = df['newtime'].dt.year, df['newtime'].dt.month

    return df



def latest_timestamp(dt):
    return dt.max()


# TODO: make list of used var names and check existance
def main():
    data = get_log(DATA_PATH)
    cleaned_dat = cleanup_df(data)    
    
    print(cleaned_dat)


if __name__ == "__main__":
    main()

