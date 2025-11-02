from penguins.core.symbolic import SymbolicAttr

# Define the summarize() verb
def summarize(**kwargs):
    """
    Aggregate data, typically after group_by().
    
    **kwargs: Column names as keys, aggregation expressions as values
              Use _.column_name with aggregation methods
    
    Returns a function that performs the aggregation on a DataFrame or GroupBy.
    """
    def _summarize(df_or_group):
        # Extract expressions from kwargs
        exprs = []
        for new_name, expr in kwargs.items():
            # Handle SymbolicAttr expressions
            if isinstance(expr, SymbolicAttr):
                exprs.append(expr._expr.alias(new_name))
            # Handle Polars expressions directly
            elif hasattr(expr, 'alias'):
                exprs.append(expr.alias(new_name))
            else:
                # Literal value
                exprs.append(pl.lit(expr).alias(new_name))
        
        # Check if grouped or ungrouped
        if isinstance(df_or_group, pl.dataframe.group_by.GroupBy):
            # Grouped: use agg()
            return df_or_group.agg(*exprs)
        else:
            # Ungrouped: use select()
            return df_or_group.select(*exprs)
    
    return _summarize