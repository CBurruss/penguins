from penguins.core.symbolic import SymbolicAttr
from penguins.verbs.mutate import _resolve_across_columns, Across
import polars as pl

def reframe(*args, **kwargs):
    """
    Group-wise computation that creates new rows based on group summaries.
    Unlike mutate(), reframe() can change the number of rows.
    
    *args: Across objects (used without keyword assignment)
    **kwargs: Column names as keys, Polars expressions as values
    
    Returns a function that performs the reframe operation on a DataFrame.
    """
    def _reframe(df):
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
        
        # Handle keyword arguments
        for key, value in kwargs.items():
            if isinstance(value, Across):
                target_cols = _resolve_across_columns(value.cols, df.columns, df)
                
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
        
        # Perform the aggregation
        result = df.agg(**expanded_kwargs)
        
        return result
    
    return _reframe