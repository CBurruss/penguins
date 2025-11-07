from penguins.core.symbolic import SymbolicAttr

# Define the pull() verb
def pull(column, to_series=False):
    """
    Extract a single column as a Series or scalar value.
    
    column: Column name (string) or SymbolicAttr (_.column_name)
    to_series: If False (default), returns first value when Series has length 1.
               If True, always returns the full Series.
    
    Returns a function that extracts the column when piped.
    
    Usage: df >> pull("column_name") or df >> pull(_.column_name)
    """
    def _pull(df):
        # Handle SymbolicAttr objects
        if hasattr(column, 'name'):
            col_name = column.name
        else:
            col_name = column
        
        series = df[col_name]
        
        # If single value and not explicitly requesting series, return scalar
        if not to_series and len(series) == 1:
            return series[0]
        
        return series
    return _pull