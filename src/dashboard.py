import os
import pandas as pd
from utils.summarizer import Summarizer
import json

DATA_PATH = "/Users/sunbak/PolarWatch/codebase/cwdashboard"
INFO_PATH = "/Users/sunbak/PolarWatch/codebase/cwdashboard"

OUT_PATH = "/Users/sunbak/PolarWatch/codebase/cwdashboard/js"
CSV_FILE = "erddap_log.csv"
INFO_FILE = "wcn_log_crosswalk.csv"

JSON_FILE = "data.json"
VARNAMES = ['dataset_id', 'data_volume', 'requests', 'nc_req', 'dods_req',
       'text_req', 'metadata_req', 'graph_req', 'json_req', 'mat_req',
       'images_req', 'other_req', 'nc_size', 'dods_size', 'text_size',
       'metadata_size', 'graph_size', 'json_size', 'mat_size', 'images_size',
       'other_size', 'unique_visitors', 'time_epoch', 'time']



def get_file_types(content: str, varnames: list)-> list:

    ''' returns file types from _req or _size column names'''
    ''' input content: either _req or _size '''
    ''' input varnames: list of varnames'''
    ftypes = [ft.split(content)[0] for ft in varnames]
    return ftypes


def get_logdata(path: str, filename: str) -> pd.DataFrame:
    ''' returns pd.Dataframe'''

    dfile = os.path.join(path, filename)

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

def check_clean_data(df: pd.DataFrame) -> pd.DataFrame:

    # Format the data for the stats
    check_column_exists(df.columns)
    df['newtime'] = pd.to_datetime(df['time'])
    df['year'], df['month'] = df['newtime'].dt.year, df['newtime'].dt.month
    return df

def main():

    # Get logdata (csv)
    ds = get_logdata(DATA_PATH, CSV_FILE)

    # Get data info
    ds_info = get_logdata(INFO_PATH, INFO_FILE)

    # Merge data
    merged_ds = ds.merge(ds_info, how='inner', on='dataset_id')

    # merged_ds.to_csv('test.csv', index=False)

    # Check all colnames to be used for Summarizer()
    df = check_clean_data(merged_ds)


    worker = Summarizer(df, datevar = 'newtime')
    tot_req = worker.get_stat(colname= 'requests', op = 'sum')
    tot_users = worker.get_stat(colname = 'unique_visitors', op = 'sum')
    top_10_req = worker.get_most_requested(year = None, n=10)
    active_ds = worker.get_active_ds()

    #get_req_by_format
    file_by_req = worker.get_req_by_format('req')
    file_by_size = worker.get_req_by_format('size')


    # Group: Ocean Color Stat
    oc_df = df[df['group_title'].isin(['NOAA Ocean Color', 'NASA Ocean Color'])]
    ocolor = Summarizer(oc_df, datevar = 'newtime')
    oc_tot_req = ocolor.get_stat(colname= 'requests', op = 'sum')
    oc_tot_users = ocolor.get_stat(colname = 'unique_visitors', op = 'sum')
    oc_top_10_req = ocolor.get_most_requested(year = None, n=10)
    oc_active_ds = ocolor.get_active_ds()

    oc_file_by_req = ocolor.get_req_by_format('req')
    oc_file_by_size = ocolor.get_req_by_format('size')



    json_dict = {}
    stat = {
                'tot_req' : tot_req,
                'tot_users' : tot_users,
                'active_ds' : active_ds,
                'top10_reqs':
                    {
                        'titles': top_10_req['dataset_title'].tolist(),
                        'labels': top_10_req['dataset_id'].tolist(),
                        'data': top_10_req['requests'].tolist()
                    },
                'file_by_req':
                    {
                        'labels': file_by_req[0],
                        'data' : file_by_req[1]
                    },
                'file_by_size':
                    {
                        'labels': file_by_size[0],
                        'data' : file_by_size[1]
                    },

                'oc_tot_req' : oc_tot_req,
                'oc_tot_users' : oc_tot_users,
                'oc_active_ds' : oc_active_ds,
                'oc_top10_reqs':
                    {
                        'titles': oc_top_10_req['dataset_title'].tolist(),
                        'labels': oc_top_10_req['dataset_id'].tolist(),
                        'data': oc_top_10_req['requests'].tolist()
                    },
                'oc_file_by_req':
                    {
                        'labels': oc_file_by_req[0],
                        'data' : oc_file_by_req[1]
                    },
                'oc_file_by_size':
                    {
                        'labels': oc_file_by_size[0],
                        'data' : oc_file_by_size[1]
                    }
            }



    json_dict["stats"] = stat

    outfile = os.path.join(OUT_PATH, JSON_FILE)

    with open(outfile, 'w') as file:
        json.dump(json_dict, file, indent=4)


if __name__ == "__main__":
    main()
