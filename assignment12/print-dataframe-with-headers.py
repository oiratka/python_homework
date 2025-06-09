import pandas as pd


class DFPlus(pd.DataFrame):

    @property
    def _constructor (self):
        return DFPlus
    
    def print_with_headers(self):
        total_rows = len(self)
        for start in range(0, total_rows, 10):
            end = start + 10
            chunk = super().iloc[start:end]
            print(chunk)
            print()
    
    @classmethod
    def from_csv(cls, filepath, **kwargs):
        df = pd.read_csv(filepath, **kwargs)
        return cls(df)
    

df_plus = DFPlus.from_csv('./csv/products.csv')
df_plus.print_with_headers()


