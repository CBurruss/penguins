from penguins.core.symbolic import SymbolicAttr

# Define the rename() verb
def rename(**kwargs):
    """
    Rename columns.
    
    **kwargs: new_name=old_name pairs
              Can use strings or symbolic columns for old names
    
    Returns a function that performs the rename on a DataFrame.
    """
    def _rename(df):
        mapping = {}
        
        for new_name, old_name in kwargs.items():
            # Extract column name from SymbolicAttr if needed
            if isinstance(old_name, SymbolicAttr):
                mapping[old_name.name] = new_name
            else:
                # Regular string column name
                mapping[old_name] = new_name
        
        return df.rename(mapping)
    
    return _rename