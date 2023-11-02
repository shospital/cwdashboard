import os
import pandas as pd
from data_worker import DataWorker
import json

DATA_PATH = "/Users/sunbak/PolarWatch/codebase/cwdashboard"
OUT_PATH = "/Users/sunbak/PolarWatch/codebase/cwdashboard/js"
CSV_FILE = "erddap_log.csv"
JSON_FILE = "data.json"
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

def check_column_exists(cnames) -> None:
    ''' checks if the VARNAMES exist in the current csv file'''
    validvars = set(VARNAMES).issubset(set(cnames))

    if not validvars:
        raise ValueError("All required columns are not present.")

def format_data(df: pd.DataFrame) -> pd.DataFrame:

    # Format the data for the stats
    check_column_exists(df.columns)
    df['newtime'] = pd.to_datetime(df['time'])
    df['year'], df['month'] = df['newtime'].dt.year, df['newtime'].dt.month
    return df


def main():

    ds = get_logdata(DATA_PATH)
    df = format_data(ds)
    worker = DataWorker(df, datevar = 'newtime')
    tot_req = worker.get_stat(colname= 'requests', op = 'sum')
    tot_users = worker.get_stat(colname = 'unique_visitors', op = 'sum')
    top_10_req = worker.get_most_requested(year = None, n=10)
    active_ds = worker.get_active_ds()


    json_dict = {}
    stat = {
                'tot_req' : tot_req,
                'tot_users' : tot_users,
                'active_ds' : active_ds,
                'top10_reqs':
                    {
                        'labels': top_10_req['dataset_id'].tolist(),
                        'data': top_10_req['requests'].tolist()
                    }


            }
    json_dict["stats"] = stat

    outfile = os.path.join(OUT_PATH, JSON_FILE)

    with open(outfile, 'w') as file:
        json.dump(json_dict, file, indent=4)


if __name__ == "__main__":
    main()
