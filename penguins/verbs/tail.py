from penguins.core.symbolic import SymbolicAttr

# Define the tail() verb
def tail(n=5):
    """
    Return last n rows.
    
    n: Number of rows to return (default: 5)
    
    Returns a function that selects the last n rows.
    """
    def _tail(df):
        return df.tail(n)
    
    return _tail