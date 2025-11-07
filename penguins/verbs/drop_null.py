from penguins.core.symbolic import SymbolicAttr

# Define the drop_na() verb
def drop_null(subset=None):
    """
    Remove rows with null values.
    
    subset: Column name(s) to check for nulls. If None, checks all columns.
            Can be a string, list of strings, or SymbolicAttr
    
    Returns a function that drops null rows when piped.
    
    Usage: df >> drop_null() 
        df >> drop_null("column") 
        df >> drop_null(["col1", "col2"])
    """
    def _drop_null(df):
        # Handle SymbolicAttr objects
        if hasattr(subset, 'name'):
            cols = subset.name
        else:
            cols = subset
        return df.drop_nulls(subset=cols)
    return _drop_null