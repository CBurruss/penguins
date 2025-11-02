from penguins.core.symbolic import SymbolicAttr

# Define the relocate() verb
def relocate(*args, before=None, after=None):
    """
    Reorder columns in a DataFrame.
    
    Usage:
    - relocate(_.col1, _.col2) moves columns to the front
    - relocate(_.col1, before=_.col2) moves col1 before col2
    - relocate(_.col1, after=_.col2) moves col1 after col2
    
    args: Column expressions to relocate
    before: Column expression to place args before
    after: Column expression to place args after
    
    Returns a function that reorders columns in a DataFrame
    """
    def _relocate(df):
        # Extract column names from symbolic expressions
        cols_to_move = [arg._expr.meta.output_name() for arg in args]
        all_cols = df.columns
        remaining_cols = [c for c in all_cols if c not in cols_to_move]
        
        if before is None and after is None:
            # Move to front
            new_order = cols_to_move + remaining_cols
        elif before is not None:
            # Insert before specified column
            anchor = before._expr.meta.output_name()
            anchor_idx = remaining_cols.index(anchor)
            new_order = remaining_cols[:anchor_idx] + cols_to_move + remaining_cols[anchor_idx:]
        else:
            # Insert after specified column
            anchor = after._expr.meta.output_name()
            anchor_idx = remaining_cols.index(anchor)
            new_order = remaining_cols[:anchor_idx + 1] + cols_to_move + remaining_cols[anchor_idx + 1:]
        
        return df.select(new_order)
    
    return _relocate