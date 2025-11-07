from penguins.core.symbolic import SymbolicAttr
import polars as pl

from penguins.utils.helpers import (
    WhereSelector,
    where,
    is_numeric,
    is_integer,
    is_float,
    is_string,
    is_boolean,
    is_temporal,
    is_null,
    is_cat
)

# Define Across class
class Across:
    """
    Represents an across() operation for mutating multiple columns.
    
    Applies a function to multiple columns selected by pattern or list.
    """
    def __init__(self, cols, func, names=None):
        self.cols = cols
        self.func = func
        self.names = names  # Optional naming pattern like "{col}_new"

# Define across() helper function
def across(cols, func, names=None):
    """
    Apply a function across multiple columns.
    
    cols: Column selector (list of strings/SymbolicAttr, or selector function like starts_with())
    func: Function to apply to each column (should accept a Polars expression)
    names: Optional naming pattern with {col} placeholder, e.g. "{col}_log"
    
    Usage:
        df >> mutate(across([_.col1, _.col2], lambda x: x * 2))
        df >> mutate(across(starts_with("bill"), lambda x: x.log()))
    """
    return Across(cols, func, names)

# Define resolve_across_columns() helper function
def _resolve_across_columns(cols, all_columns, df=None):
    """
    Resolve column specifications for across() to actual column names.
    
    cols: Column specification (list, selector function, or single column)
    all_columns: List of all column names in the DataFrame
    df: The DataFrame (needed for where() selectors to check dtypes)
    
    Returns a list of column names to operate on.
    """
    from penguins.verbs.select import StartsWithSelector, EndsWithSelector, ContainsSelector
    
    # Handle where() selector
    if isinstance(cols, WhereSelector):
        if df is None:
            raise ValueError("DataFrame required for where() selector")
        return [col for col in all_columns if cols.predicate(df[col].dtype)]
    
    # Handle selector functions
    if isinstance(cols, StartsWithSelector):
        return [col for col in all_columns if col.startswith(cols.prefix)]
    
    if isinstance(cols, EndsWithSelector):
        return [col for col in all_columns if col.endswith(cols.suffix)]
    
    if isinstance(cols, ContainsSelector):
        return [col for col in all_columns if cols.substring in col]
    
    # Handle list of columns
    if isinstance(cols, list):
        result = []
        for col in cols:
            if isinstance(col, SymbolicAttr):
                result.append(col.name)
            elif isinstance(col, str):
                result.append(col)
        return result
    
    # Handle single column
    if isinstance(cols, SymbolicAttr):
        return [cols.name]
    
    if isinstance(cols, str):
        return [cols]
    
    return []

def mutate(*args, _before=None, _after=None, **kwargs):
    """
    Create new columns or modify existing ones.
    
    *args: Across objects (used without keyword assignment)
    **kwargs: Column names as keys, Polars expressions as values
              Use _ to reference columns: _.column_name
              Lists will be automatically converted to Series
              Use across() to apply functions to multiple columns
    _before: Column name (string) to place new columns before
    _after: Column name (string) to place new columns after
    
    Returns a function that performs the mutation on a DataFrame.
    """
    def _mutate(df):
        # First, expand any across() calls
        expanded_kwargs = {}
        
        # Handle positional Across objects
        for arg in args:
            if isinstance(arg, Across):
                target_cols = _resolve_across_columns(arg.cols, df.columns, df)
                
                for col_name in target_cols:
                    col_expr = pl.col(col_name)
                    result_expr = arg.func(col_expr)
                    
                    if arg.names:
                        output_name = arg.names.format(col=col_name)
                    else:
                        output_name = col_name
                    
                    expanded_kwargs[output_name] = result_expr
        
        # Handle keyword arguments (including Across objects)
        for key, value in kwargs.items():
            if isinstance(value, Across):
                target_cols = _resolve_across_columns(value.cols, df.columns)
                
                for col_name in target_cols:
                    col_expr = pl.col(col_name)
                    result_expr = value.func(col_expr)
                    
                    if value.names:
                        output_name = value.names.format(col=col_name)
                    else:
                        output_name = col_name
                    
                    expanded_kwargs[output_name] = result_expr
            else:
                expanded_kwargs[key] = value
        
        # Convert any Series or lists to expressions
        processed_kwargs = {}
        for key, value in expanded_kwargs.items():
            if isinstance(value, list):
                series = pl.Series(key, value)
                if len(series) != len(df):
                    raise ValueError(f"List length ({len(series)}) must match DataFrame length ({len(df)})")
                processed_kwargs[key] = series.alias(key)
            elif isinstance(value, pl.Series):
                if len(value) != len(df):
                    raise ValueError(f"Series length ({len(value)}) must match DataFrame length ({len(df)})")
                processed_kwargs[key] = value.alias(key)
            else:
                processed_kwargs[key] = value
        
        # Add the new columns
        result = df.with_columns(**processed_kwargs)
        
        # If positioning is specified, reorder columns
        if _before is not None or _after is not None:
            new_col_names = list(processed_kwargs.keys())
            existing_cols = df.columns
            other_cols = [c for c in result.columns if c not in new_col_names]
            
            if _before is not None:
                anchor_idx = other_cols.index(_before)
                new_order = other_cols[:anchor_idx] + new_col_names + other_cols[anchor_idx:]
            else:
                anchor_idx = other_cols.index(_after)
                new_order = other_cols[:anchor_idx + 1] + new_col_names + other_cols[anchor_idx + 1:]
            
            result = result.select(new_order)
        
        return result
    
    return _mutate