import polars as pl
from penguins.core.symbolic import SymbolicAttr

def if_else(condition, true, false):
    """
    Vectorized if-else statement for creating conditional columns.
    
    Parameters:
    -----------
    condition : Polars expression or boolean
        The condition to evaluate (use _ for column references)
    true : Polars expression, scalar, or SymbolicAttr
        Value to return when condition is True
    false : Polars expression, scalar, or SymbolicAttr
        Value to return when condition is False
    
    Returns:
    --------
    Polars expression
    
    Usage:
    ------
    df >> mutate(
        size_category = if_else(
            _.bill_length_mm > 45,
            "large",
            "small"
        )
    )
    
    df >> mutate(
        adjusted_length = if_else(
            _.species == "Adelie",
            _.bill_length_mm * 1.1,
            _.bill_length_mm
        )
    )
    """
    # Convert SymbolicAttr to expressions
    if isinstance(true, SymbolicAttr):
        true = true._expr
    elif not isinstance(true, pl.Expr):
        true = pl.lit(true)
    
    if isinstance(false, SymbolicAttr):
        false = false._expr
    elif not isinstance(false, pl.Expr):
        false = pl.lit(false)
    
    return pl.when(condition).then(true).otherwise(false)