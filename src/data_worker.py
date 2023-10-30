import pandas as pd

class DataWorker:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def get_latest_date(self, colname: str)-> pd.datetime:
        '''takes dataframe col_name'''
        return self.dataframe['colname'].max()



    # def mean_of_column(self, column):
    #     """ Returns the mean of a specified column """
    #     return self.dataframe[column].mean()

    # def summary_statistics(self, column):
    #     """ Returns summary statistics of a specified column """
    #     return self.dataframe[column].describe()
