from penguins.core.symbolic import SymbolicAttr
import polars as pl
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
        
        # Check if working with LazyFrames
        is_lazy = isinstance(df, pl.LazyFrame)
        
        # Only check row counts for DataFrames
        if not is_lazy:
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
        
        for other_df in dfs:
            # Check for duplicate column names
            if is_lazy:
                result_cols = result.collect_schema().names()
                other_cols = other_df.collect_schema().names()
            else:
                result_cols = result.columns
                other_cols = other_df.columns
                
            duplicate_cols = set(result_cols) & set(other_cols)
            
            if duplicate_cols:
                # Rename duplicates in other_df
                rename_map = {}
                for col in duplicate_cols:
                    # Find next available suffix number
                    base_name = col
                    counter = 2
                    new_name = f"{base_name}{suffix}"
                    
                    # Keep incrementing if still duplicate
                    while new_name in result_cols or new_name in other_cols:
                        counter += 1
                        new_name = f"{base_name}_{counter}"
                    
                    rename_map[col] = new_name
                
                other_df = other_df.rename(rename_map)
            
            # Stack horizontally
            if is_lazy:
                # Convert other_df to LazyFrame if needed
                if not isinstance(other_df, pl.LazyFrame):
                    other_df = other_df.lazy()
                result = pl.concat([result, other_df], how="horizontal")
            else:
                result = result.hstack(other_df)
        
        return result
    
    return _bind_cols