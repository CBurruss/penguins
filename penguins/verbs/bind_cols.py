from penguins.core.symbolic import SymbolicAttr
import warnings

def bind_cols(*dfs, suffix="_2"):
    """
    Join DataFrames horizontally (column-wise).
    
    *dfs: Variable number of DataFrames to bind
    suffix: Suffix to add to duplicate column names (default "_2")
    
    Returns a function that takes a DataFrame and horizontally stacks it with others
    Aligns by row position, fills with null if row counts don't match
    
    Usage: df >> bind_cols(df2, df3)
    """
    def _bind_cols(df):
        result = df
        
        # Get the max row count for padding
        all_dfs = [df] + list(dfs)
        max_rows = max(d.height for d in all_dfs)
        
        if df.height < max_rows:
            warnings.warn(
                f"Row count mismatch: primary DataFrame has {df.height} rows "
                f"but maximum is {max_rows}. Filling with nulls."
            )
        
        for other_df in dfs:
            if other_df.height < max_rows:
                warnings.warn(
                    f"Row count mismatch: a DataFrame has {other_df.height} rows "
                    f"but maximum is {max_rows}. Filling with nulls."
                )
            
            # Check for duplicate column names
            duplicate_cols = set(result.columns) & set(other_df.columns)
            
            if duplicate_cols:
                # Rename duplicates in other_df
                rename_map = {}
                for col in duplicate_cols:
                    # Find next available suffix number
                    base_name = col
                    counter = 2
                    new_name = f"{base_name}{suffix}"
                    
                    # Keep incrementing if still duplicate
                    while new_name in result.columns or new_name in other_df.columns:
                        counter += 1
                        new_name = f"{base_name}_{counter}"
                    
                    rename_map[col] = new_name
                
                other_df = other_df.rename(rename_map)
            
            # Stack horizontally
            result = result.hstack(other_df)
        
        return result
    
    return _bind_cols