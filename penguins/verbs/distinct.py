from penguins.core.symbolic import SymbolicAttr

# Define the distinct() verb
def distinct(*args):
    """
    Keep only unique rows based on specified columns.
    
    *args: Column names (strings) or symbolic columns
           If no columns specified, uses all columns
    
    Returns a function that removes duplicate rows.
    """
    def _distinct(df):
        if not args:
            # Use all columns
            return df.unique()
        else:
            # Use specified columns
            cols = []
            for arg in args:
                if isinstance(arg, SymbolicAttr):
                    cols.append(arg.name)
                else:
                    cols.append(arg)
            return df.unique(subset=cols)
    
    return _distinct