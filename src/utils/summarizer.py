
class Summarizer:
    def __init__(self, df, datevar: str):

        # Remove dataset_id == 'all_datasets'
        self.df = df[df['dataset_id']!= 'all_datasets']
        self.df['month'] = self.df[datevar].dt.month

        # Get date variable
        self.datevar = datevar

        # set latest
        self.latest = self.df[datevar].max()

        # Set latest year
        self.year = self.get_latest_year()


    def _check_var(self, colname):
            # Check column names exists
        if colname not in self.df.columns:
            raise KeyError(f"Column '{colname}' does not exist in the DataFrame.")

    def get_columns(self)-> list:
        return self.df.columns

    def _check_op(self, op):
        # Check for supported operations
        if op not in ['mean', 'sum', 'count']:
            raise ValueError(
                f"Unsupported operation '{op}'. ('mean', 'sum', and 'count')")

    def get_latest_df(self):
        '''takes dataframe col_name'''
        return self.latest

    def get_latest_year(self):
        datevar = self.datevar
        year = self.df[datevar].dt.year.max()
        return year

    # def get_file_types(self, content: str, colnames: list)-> list:
    #     ftypes = [ft.split(content)[0] for ft in colnames]
    #     return ftypes

    def subset_by_year(self, year=None):
        if year is None:
            year = self.year
        ds = self.df
        return ds[ds[self.datevar].dt.year == year]


    def get_stat(self, colname, op):

        # check if colname exists in df
        self._check_var(colname)

        # check if op is available
        self._check_op(op)

        df = self.subset_by_year()

        # Perform the operation
        if op == 'mean':
            try:
                return df[colname].fillna(0).mean()
            except TypeError:
                raise TypeError(
                    f"Cannot calculate mean of non-numeric data in column '{colname}'.")
        if op == 'sum':
            try:
                return df[colname].fillna(0).sum()
            except TypeError:
                raise TypeError(
                    f"Cannot calculate sum of non-numeric data in column '{colname}'.")
        if op == 'count':
            return df[colname].count()

    # compute {sum/mean/count} of {colname} grouped by {by}
    def get_stat_by(self, colname, by, op):
        df = self.subset_by_year()
        self._check_var(colname)
        self._check_var(by)
        self._check_op(op)

        # Perform the operation
        if op == 'mean':
            try:
                return df.fillna(0).groupby(by)[colname].mean()
            except TypeError:
                raise TypeError(
                    f"Cannot calculate mean of non-numeric data in column '{colname}'.")
        if op == 'sum':
            try:
                return df.fillna(0).groupby(by)[colname].sum()
            except TypeError:
                raise TypeError(
                    f"Cannot calculate sum of non-numeric data in column '{colname}'.")
        if op == 'count':
            return df.groupby(by)[colname].count()  # count() works for any data type


    def get_monthly_stat_by(self, colname, by, op='sum'):
        df = self.subset_by_year()
        # print(df.columns)
        self._check_var(colname)
        self._check_op(op)

        stat = df.fillna(0).groupby(['month', by])[colname].sum().reset_index()
        stat_wide = stat.pivot(
            index = by, columns = 'month', values = colname).reset_index()

        return stat_wide

    def get_most_requested(self, year=None, n=10):
        # year : returns most requested of the arg:year

        df = self.subset_by_year(year)
        reqdf = df.groupby('dataset_title')['requests'].sum()
        reqdf = reqdf.reset_index().sort_values(by='requests', ascending=False)
        return reqdf[['dataset_title', 'requests']].head(n)
        # return reqdf.head(n)

    def get_active_ds(self, year=None):
        df = self.subset_by_year(year)
        unique_id = len(df['dataset_id'].unique()) - 1
        if unique_id < 0:
            return 0
        else:
            return unique_id


    def get_req_by_format(self, data_type: str):
        # format data ends with _size for size of requests
        if str(data_type) == "size":
            [s.replace('_size', '') for s in self.get_columns()]

        # format data ends with _req for no of requests
        elif str(data_type) == "req":
            [s.replace("_req", "") for s in self.get_columns()]
        else:
            print(f"Error: {data_type}  Req by format only recognizes size or req")
            return 0


        # List of column names
        type_cols = [col for col in self.get_columns() if col.endswith(data_type)]

        # List of file types
        type_names = [s.replace("_"+ data_type, "") for s in type_cols]

        # List of sums
        type_sums = [self.get_stat(cname, "sum") for cname in type_cols]

        return [type_names, type_sums]

    # Group
