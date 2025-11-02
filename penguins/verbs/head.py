from penguins.core.symbolic import SymbolicAttr

# Define the head() verb
def head(n=5):
    """
    Return first n rows.
    
    n: Number of rows to return (default: 5)
    
    Returns a function that selects the first n rows.
    """
    def _head(df):
        return df.head(n)
    
    return _head