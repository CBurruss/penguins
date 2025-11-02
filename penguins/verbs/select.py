from penguins.core.symbolic import SymbolicAttr

# Define the select() verb
def select(*cols):
    """
    Select specific columns from the DataFrame.
    
    *cols: Variable number of column names as strings or SymbolicAttr objects
    
    Returns a function that performs the selection on a DataFrame.
    """
    def _select(df):
        # Unwrap SymbolicAttr objects to get the underlying Polars expressions
        unwrapped_cols = []
        for col in cols:
            if isinstance(col, SymbolicAttr):
                unwrapped_cols.append(col._expr)
            else:
                unwrapped_cols.append(col)
        # Call Polars' select method with the unwrapped columns
        return df.select(unwrapped_cols)
    return _select