import os
import pandas as pd

DATA_PATH = "/Users/sunbak/PolarWatch/codebase/cwdashboard"
CSV_FILE = "erddap_log.csv"
VARNAMES = ['dataset_id', 'data_volume', 'requests', 'nc_req', 'dods_req',
       'text_req', 'metadata_req', 'graph_req', 'json_req', 'mat_req',
       'images_req', 'other_req', 'nc_size', 'dods_size', 'text_size',
       'metadata_size', 'graph_size', 'json_size', 'mat_size', 'images_size',
       'other_size', 'unique_visitors', 'time_epoch', 'time']


def get_log(path: str) -> pd.DataFrame:
    ''' returns pd.Dataframe'''

    dfile = os.path.join(path, CSV_FILE)

    if not os.path.isfile(dfile):
        raise FileNotFoundError(f"CW ERROR: The file {dfile} does not exist.")

    df = pd.read_csv(dfile)

    if len(df) >= 1:
        # remove row with units
        df.drop(index=0, inplace=True)
    return df

def check_column_exists(cnames) -> None:
    validvars = set(VARNAMES).issubset(set(cnames))

    if not validvars:
        print(cnames)
        raise ValueError("All required columns are not present.")

def cleanup_df(df: pd.DataFrame) -> pd.DataFrame:

# format
    try:
        check_column_exists(df.columns)
    except ValueError as e:
        print(e)
    else:
        df['newtime'] = pd.to_datetime(df['time'])
        df['year'], df['month'] = df['newtime'].dt.year, df['newtime'].dt.month

    return df

def latest_timestamp(dt):
    return dt.max()

def main():
    get_log(DATA_PATH)
    #cleaned_dat = cleanup_df(data)

    #print(cleaned_dat.columns)


if __name__ == "__main__":
    main()
