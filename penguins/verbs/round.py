# Define the round() verb
import polars as pl
from penguins.core.symbolic import SymbolicAttr

def round(*args, decimals=2):
    """
    Round numeric columns to specified decimal places.
    
    *args: Column names (strings) or symbolic columns to round
           If no columns specified, rounds all numeric columns
    decimals: Number of decimal places (default: 2)
    
    Returns a function that performs the rounding on a DataFrame.
    """
    def _round(df):
        if not args:
            # Round all numeric columns
            numeric_types = [pl.Float32, pl.Float64, pl.Int8, pl.Int16, pl.Int32, pl.Int64]
            if isinstance(df, pl.LazyFrame):
                schema = df.collect_schema()
                cols_to_round = [
                    pl.col(col).round(decimals).alias(col)
                    for col, dtype in schema.items()
                    if dtype in numeric_types
                ]
            else:
                cols_to_round = [
                    pl.col(col).round(decimals).alias(col)
                    for col, dtype in zip(df.columns, df.dtypes)
                    if dtype in numeric_types
                ]
            if cols_to_round:
                return df.with_columns(cols_to_round)
            return df
        else:
            # Round specified columns
            cols = []
            for arg in args:
                if isinstance(arg, SymbolicAttr):
                    cols.append(pl.col(arg.name).round(decimals).alias(arg.name))
                else:
                    cols.append(pl.col(arg).round(decimals).alias(arg))
            return df.with_columns(cols)
    
    return _round