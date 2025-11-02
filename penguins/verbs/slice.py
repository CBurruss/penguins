from penguins.core.symbolic import SymbolicAttr

# Define the slice() verb
def slice(*args):
    """
    Select rows by position.
    
    Usage:
    - slice(5) returns first 5 rows
    - slice(5, 10) returns rows 5-14 (10 rows starting at index 5)
    - slice(-5) returns last 5 rows
    
    args: Either (n) for first/last n rows, or (offset, n) for n rows starting at offset
    
    Returns a function that applies the slice to a DataFrame
    """
    def _slice(df):
        if len(args) == 1:
            n = args[0]
            return df.slice(0, n) if n >= 0 else df.slice(n, abs(n))
        elif len(args) == 2:
            offset, n = args
            return df.slice(offset, n)
        else:
            raise ValueError("slice() takes 1 or 2 arguments")
    
    return _slice