import os
import pandas as pd
from utils.summarizer import Summarizer
import json

DATA_PATH = "cwdashboard"
INFO_PATH = "cwdashboard"


OUT_PATH = "/Users/sunbak/PolarWatch/codebase/cwdashboard/js"
# CSV_FILE = "erddap_logs.csv"
#INFO_FILE = "wcn_log_crosswalk.csv"
CSV_FILE = "https://polarwatch.noaa.gov/erddap/tabledap/erddap_logs_monthly.csv?dataset_id%2Cdata_volume%2Crequests%2Cnc_req%2Cdods_req%2Ctext_req%2Cmetadata_req%2Cgraph_req%2Cjson_req%2Cmat_req%2Cimages_req%2Cother_req%2Cnc_size%2Cdods_size%2Ctext_size%2Cmetadata_size%2Cgraph_size%2Cjson_size%2Cmat_size%2Cimages_size%2Cother_size%2Cunique_visitors%2Ctime_epoch%2Ctime&time%3E=2020-06-15T12%3A00%3A00Z&time%3C=2022-12-15T12%3A00%3A00Z"
INFO_FILE = "https://polarwatch.noaa.gov/erddap/tabledap/wcn_log_crosswalk.csv?dataset_id%2Cgroup_title%2Cdata_source%2Cdataset_title%2Cvariable%2Csensor"

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

def get_logdata_erddap(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename)
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

def format_monthly(df, colname):
    datasets = []

    # append labels
    labels = {
        'labels' : df.columns[1:].tolist()
    }
    datasets.append(labels)
    data = []
    for index, row in df.iterrows():
        d = {
            'label' : row[colname],
            'data' : row[1:].tolist()
        }
    data.append(d)
    datasets.append(data)
    return datasets

def stats_to_json(summarizer: Summarizer):
    json_dict = {}
    # tot_req = summarizer.get_stat(colname= 'requests', op = 'sum')
    tot_req = summarizer.get_stat(colname= 'requests',  op = 'sum')
    tot_users = summarizer.get_stat(colname = 'unique_visitors', op = 'sum')
    top_10_req = summarizer.get_most_requested(year = None, n=10)
    active_ds = summarizer.get_active_ds()

    file_by_req = summarizer.get_req_by_format('req')
    file_by_size = summarizer.get_req_by_format('size')

    latest_year = summarizer.get_latest_year()

    monthly_sensor = summarizer.get_monthly_stat_by(
        colname='requests', by= 'sensor', op = 'sum')
    formatted_sensor = format_monthly(monthly_sensor, 'sensor')
    print(formatted_sensor)

    stats = {
                'latest_year': latest_year,
                'tot_req' : tot_req,
                'tot_users' : tot_users,
                'active_ds' : active_ds,
                'top10_reqs':
                    {
                        'titles': top_10_req['dataset_title'].tolist(),
                        # 'labels': top_10_req['dataset_id'].tolist(),
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
                'monthly_sensor':
                    {
                        'labels' : formatted_sensor[0],
                        'datasets' : formatted_sensor[1]
                    }


            }

    json_dict["stats"] = stats
    return json_dict


def main():

    # Get logdata (csv)
    ds = get_logdata_erddap(CSV_FILE)

    # Get data info
    ds_info = get_logdata_erddap(INFO_FILE)

    # Merge data
    merged_ds = ds.merge(ds_info, how='inner', on='dataset_id')

    # Check all colnames to be used for Summarizer()
    df = check_clean_data(merged_ds)

    # Create Summarizer instance
    worker = Summarizer(df, datevar = 'newtime')

    # Get stats in json format
    stat_json = stats_to_json(worker)

    # Write to a file
    datafile = os.path.join(OUT_PATH, "data.json")
    with open(datafile, 'w+') as file:
        json.dump(stat_json, file, indent=4)


    ## Ocean Color Stats

    oc_df = df[df['group_title'].isin(['NOAA Ocean Color', 'NASA Ocean Color'])]
    ocolor = Summarizer(oc_df, datevar = 'newtime')
    dat2json = stats_to_json(ocolor)

    # Write to a file
    ofile = os.path.join(OUT_PATH, "ocolor.json")
    with open(ofile, 'w') as file:
        json.dump(dat2json, file, indent=4)


    ## Sea Surface Temperature
    sst_df = df[df['variable'] == "sst"]
    sst = Summarizer(sst_df, datevar='newtime')
    dat2json = stats_to_json(sst)
    ofile = os.path.join(OUT_PATH, "sst.json")
    with open(ofile, 'w') as file:
        json.dump(dat2json, file, indent=4)

    ## Wind
    wind_df = df[df['variable'] == "wind"]
    wind = Summarizer(wind_df, datevar='newtime')
    dat2json = stats_to_json(wind)
    ofile = os.path.join(OUT_PATH, "wind.json")
    with open(ofile, 'w') as file:
        json.dump(dat2json, file, indent=4)

    ## Habitat
    habitat_df = df[df['variable'] == "habitat"]
    habitat = Summarizer(habitat_df, datevar='newtime')
    dat2json = stats_to_json(habitat)

    ofile = os.path.join(OUT_PATH, "habitat.json")
    with open(ofile, 'w') as file:
        json.dump(dat2json, file, indent=4)

if __name__ == "__main__":
    main()
