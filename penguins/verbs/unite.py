from penguins.core.symbolic import SymbolicAttr
import polars as pl

def unite(new_col, from_cols, sep="_", drop=True):
    """
    Combine multiple columns into one with a separator.
    
    new_col: Name of the new column to create
    from_cols: List of SymbolicAttr column references or column names
    sep: Separator string (default "_")
    drop: Whether to drop source columns (default True)
    
    Returns a function that takes a DataFrame and returns the modified DataFrame
    
    Usage: df >> unite("combined", [_.col1, _.col2], sep="-")
    """
    def _unite(df):
        # Extract column names from SymbolicAttr objects
        col_names = []
        for col in from_cols:
            if isinstance(col, SymbolicAttr):
                col_names.append(col.name)
            else:
                col_names.append(col)
        
        # Coerce all columns to string and fill nulls with empty string
        string_cols = [
            pl.col(name).cast(pl.Utf8).fill_null("") 
            for name in col_names
        ]
        
        # Concatenate with separator
        united = pl.concat_str(string_cols, separator=sep).alias(new_col)
        
        # Add the new column
        result = df.with_columns(united)
        
        # Drop source columns if requested
        if drop:
            result = result.drop(col_names)
        
        return result
    
    return _unite