from penguins.core.symbolic import SymbolicAttr

# Define the group_by() verb
def group_by(*args):
    """
    Group DataFrame by one or more columns.
    
    *args: Column names (strings) or symbolic columns
    
    Returns a function that performs the grouping on a DataFrame.
    """
    def _group_by(df):
        cols = []
        
        for arg in args:
            if isinstance(arg, SymbolicAttr):
                cols.append(arg.name)
            else:
                cols.append(arg)
        
        return df.group_by(cols)
    
    return _group_by