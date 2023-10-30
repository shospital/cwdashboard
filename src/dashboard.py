import os
import pandas as pd
from data_worker import DataWorker

DATA_PATH = "/Users/sunbak/PolarWatch/codebase/cwdashboard"
CSV_FILE = "erddap_log.csv"
VARNAMES = ['dataset_id', 'data_volume', 'requests', 'nc_req', 'dods_req',
       'text_req', 'metadata_req', 'graph_req', 'json_req', 'mat_req',
       'images_req', 'other_req', 'nc_size', 'dods_size', 'text_size',
       'metadata_size', 'graph_size', 'json_size', 'mat_size', 'images_size',
       'other_size', 'unique_visitors', 'time_epoch', 'time']


def get_logdata(path: str) -> pd.DataFrame:
    ''' returns pd.Dataframe'''

    dfile = os.path.join(path, CSV_FILE)

    if not os.path.isfile(dfile):
        raise FileNotFoundError(f"CW ERROR: The file {dfile} does not exist.")

    df = pd.read_csv(dfile)

    if len(df) >= 1:
        # remove row with units
        df.drop(index=0, inplace=True)
    return df

def _check_column_exists(cnames) -> None:
    validvars = set(VARNAMES).issubset(set(cnames))

    if not validvars:
        print(cnames)
        raise ValueError("All required columns are not present.")

def format_data(df: pd.DataFrame) -> pd.DataFrame:

    # Check all columns required for analysis
    try:
        _check_column_exists(df.columns)
    except ValueError as e:
        print(e)
    else:
        df['newtime'] = pd.to_datetime(df['time'])
        df['year'], df['month'] = df['newtime'].dt.year, df['newtime'].dt.month

    return df

def latest_timestamp(dt):
    return dt.max()

def main():
    df = get_logdata(DATA_PATH)
    worker = DataWorker(df)
    worker.get_latest_date('newtime')


# latest_date = analyzer.get_latest_date('date')
# mean_value = analyzer.mean_of_column('values')
# summary_stats = analyzer.summary_statistics('values')

# print("Latest Date:", latest_date)
# print("Mean of values:", mean_value)
# print("Summary Statistics:\n", summary_stats)


if __name__ == "__main__":
    main()




# TODO
# COUNT Total # of Request
# COUNT  Total Unique “Known” Users
# COUNT Total Active Datasets
# BAR GRAPH Top 10 most requested datasets (most requests)
# TABLE Top 10 most requested datasets with link to metadata (most request)
# PIE GRAPH Total requests by formats
# PIE GRAPH total request by volume
