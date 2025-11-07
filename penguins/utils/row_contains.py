import polars as pl
from penguins.core.symbolic import SymbolicAttr

def row_contains(*values):
    """
    Check if any rows in a DataFrame contain any of the specified values.
    
    Handles mixed column types by only checking compatible columns.
    
    *values: Values to search for across all columns
    
    Returns a Polars expression that evaluates to True when any column matches.
    
    Usage: df >> filter(row_contains("None", "NA"))
    """
    import polars as pl
    
    # Convert values to a list for checking
    values_list = list(values)
    
    # Get expressions for each column, handling type compatibility
    # Cast all columns to string to avoid type mismatches
    return pl.any_horizontal(
        pl.all().cast(pl.String).is_in([str(v) for v in values_list])
    )