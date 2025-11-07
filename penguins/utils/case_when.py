import polars as pl
from penguins.core.symbolic import SymbolicAttr

def case_when(*conditions, default=None):
    """
    Vectorized multi-condition case statement (similar to SQL CASE WHEN).
    
    Parameters:
    -----------
    *conditions : tuples of (condition, value)
        Each tuple contains a condition expression and the value to return
        Conditions are evaluated in order
    default : scalar, expression, or SymbolicAttr, optional
        Value to return when no conditions are met (default: None)
    
    Returns:
    --------
    Polars expression
    
    Usage:
    ------
    df >> mutate(
        size = case_when(
            (_.bill_length_mm < 35, "small"),
            (_.bill_length_mm < 45, "medium"),
            (_.bill_length_mm >= 45, "large"),
            default="unknown"
        )
    )
    
    df >> mutate(
        price_tier = case_when(
            ((_.species == "Adelie") & (_.island == "Torgersen"), "tier_1"),
            (_.species == "Gentoo", "tier_2"),
            default="tier_3"
        )
    )
    
    # Can also use column values as results
    df >> mutate(
        adjusted = case_when(
            (_.bill_length_mm > 50, _.bill_length_mm * 0.9),
            (_.bill_length_mm < 30, _.bill_length_mm * 1.1),
            default=_.bill_length_mm
        )
    )
    """
    if not conditions:
        raise ValueError("case_when requires at least one condition")
    
    # Start with the first condition
    first_condition, first_value = conditions[0]
    if isinstance(first_value, SymbolicAttr):
        first_value = first_value._expr
    elif not isinstance(first_value, pl.Expr):
        first_value = pl.lit(first_value)
    
    result = pl.when(first_condition).then(first_value)
    
    # Chain additional conditions
    for condition, value in conditions[1:]:
        if isinstance(value, SymbolicAttr):
            value = value._expr
        elif not isinstance(value, pl.Expr):
            value = pl.lit(value)
        result = result.when(condition).then(value)
    
    # Apply default value
    if default is not None:
        if isinstance(default, SymbolicAttr):
            default = default._expr
        elif not isinstance(default, pl.Expr):
            default = pl.lit(default)
        result = result.otherwise(default)
    else:
        result = result.otherwise(None)
    
    return result