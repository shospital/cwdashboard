
class DataWorker:
    def __init__(self, df, datevar):
        self.df = df
        self.datevar = datevar
        self.latest = self.df[datevar].max()
        self.year = self.get_latest_year()

    def _check_var(self, colname):
            # Check if the column exists
        if colname not in self.df.columns:
            raise KeyError(f"Column '{colname}' does not exist in the DataFrame.")

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

    def subset_by_year(self, year=None):
        if year is None:
            year = self.year
        ds = self.df
        return ds[ds[self.datevar].dt.year == year]


    def get_stat(self, colname, op):

        self._check_var(colname)
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


    def get_stat_by(self, colname, by, op):
        df = self.subset_by_year()
        self._check_var(colname)
        self._check_var(by)
        self._check_op(op)

        # Perform the operation
        if op == 'mean':
            try:
                return df[colname].fillna(0).groupby(by).mean()
            except TypeError:
                raise TypeError(
                    f"Cannot calculate mean of non-numeric data in column '{colname}'.")
        if op == 'sum':
            try:
                return df[colname].fillna(0).groupby(by).sum()
            except TypeError:
                raise TypeError(
                    f"Cannot calculate sum of non-numeric data in column '{colname}'.")
        if op == 'count':
            return df[colname].groupby(by).count()  # count() works for any data type


    def get_most_requested(self, year=None, n=10):
        df = self.subset_by_year(year)
        df.sort_values(by='requests', ascending=False, inplace=True)
        return df[['dataset_id', 'requests']].head(n)

    def get_active_ds(self, year=None):
        df = self.subset_by_year(year)
        unique_id = len(df['dataset_id'].unique()) - 1
        if unique_id < 0:
            return 0
        else:
            return unique_id

    def get_requests_by_format(self, varnames: list):
        [s.replace("_req", "") for s in varnames]
        self.get_stat()
