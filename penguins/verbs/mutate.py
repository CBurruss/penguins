from penguins.core.symbolic import SymbolicAttr
import polars as pl

# Define the mutate() verb
def mutate(_before=None, _after=None, **kwargs):
    """
    Create new columns or modify existing ones.
    
    **kwargs: Column names as keys, Polars expressions as values
              Use _ to reference columns: _.column_name
              Lists will be automatically converted to Series
    _before: Column name (string) to place new columns before
    _after: Column name (string) to place new columns after
    
    Returns a function that performs the mutation on a DataFrame.
    """
    def _mutate(df):
        # Convert any Series or lists to expressions
        processed_kwargs = {}
        for key, value in kwargs.items():
            if isinstance(value, list):
                # Convert list to Series automatically
                series = pl.Series(key, value)
                if len(series) != len(df):
                    raise ValueError(f"List length ({len(series)}) must match DataFrame length ({len(df)})")
                processed_kwargs[key] = series.alias(key)
            elif isinstance(value, pl.Series):
                # Ensure the series has the right length
                if len(value) != len(df):
                    raise ValueError(f"Series length ({len(value)}) must match DataFrame length ({len(df)})")
                processed_kwargs[key] = value.alias(key)
            else:
                processed_kwargs[key] = value
        
        # Add the new columns
        result = df.with_columns(**processed_kwargs)
        
        # If positioning is specified, reorder columns
        if _before is not None or _after is not None:
            new_col_names = list(kwargs.keys())
            existing_cols = df.columns
            other_cols = [c for c in result.columns if c not in new_col_names]
            
            if _before is not None:
                # Insert before specified column
                anchor_idx = other_cols.index(_before)
                new_order = other_cols[:anchor_idx] + new_col_names + other_cols[anchor_idx:]
            else:
                # Insert after specified column
                anchor_idx = other_cols.index(_after)
                new_order = other_cols[:anchor_idx + 1] + new_col_names + other_cols[anchor_idx + 1:]
            
            result = result.select(new_order)
        
        return result
    
    return _mutate