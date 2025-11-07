from penguins.core.symbolic import SymbolicAttr
import polars as pl

def bind_rows(*dfs):
    """
    Stack DataFrames vertically (row-wise).
    
    *dfs: Variable number of DataFrames to bind
    
    Returns a function that takes a DataFrame and concatenates it with the others
    Uses union of all columns (fills missing with null)
    
    Usage: df >> bind_rows(df2, df3)
    """
    def _bind_rows(df):
        # Combine the piped df with the additional dfs
        all_dfs = [df] + list(dfs)
        
        # Use diagonal_relaxed for union of columns
        return pl.concat(all_dfs, how="diagonal_relaxed")
    
    return _bind_rows