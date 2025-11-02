from penguins.core.symbolic import SymbolicAttr

# Define the arrange() verb
def arrange(*args, descending=False):
    """
    Sort rows by column expressions.
    
    *args: Column names (strings) or symbolic columns
           Use _.column_name for ascending
           Use -_.column_name for descending
    descending: If True, reverses all sort orders (default: False)
    
    Returns a function that performs the sort on a DataFrame.
    """
    def _arrange(df):
        cols = []
        desc_flags = []
        
        for arg in args:
            # Check if it's a SymbolicAttr
            if isinstance(arg, SymbolicAttr):
                # Check if negated
                if hasattr(arg, '_is_negated') and arg._is_negated:
                    cols.append(arg._original)
                    desc_flags.append(True)
                else:
                    cols.append(arg._expr)
                    desc_flags.append(False)
            else:
                # Regular string column name or Polars expression
                cols.append(arg)
                desc_flags.append(False)
        
        # Apply global descending flag
        if descending:
            desc_flags = [not flag for flag in desc_flags]
        
        return df.sort(cols, descending=desc_flags)
    
    return _arrange