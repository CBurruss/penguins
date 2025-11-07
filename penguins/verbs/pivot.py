from penguins.core.symbolic import SymbolicAttr, DeSelect, ColumnRange

# Define the pivot_wider() verb
def pivot_wider(names_from, values_from=None, id_cols=None, 
                values_fill=None, values_fn="first", names_sep="_",
                names_prefix="", sort_columns=False):
    """
    Pivot DataFrame from long to wide format.
    
    names_from: Column(s) whose unique values become new column names
    values_from: Column(s) to fill the new columns with (if None, uses all remaining columns)
    id_cols: Column(s) to use as identifier variables (if None, uses all remaining columns)
    values_fill: Value to use for missing combinations (default None keeps nulls)
    values_fn: Aggregation function if multiple values per group ("first", "sum", "mean", "min", "max", "count", "len")
    names_sep: Separator when multiple values_from columns create compound names
    names_prefix: Prefix to add to all pivoted column names
    sort_columns: Whether to sort the pivoted columns alphabetically
    
    Usage:
        df >> pivot_wider(names_from=_.category, values_from=_.value, id_cols=_.id)
    """
    def _pivot_wider(df):
        # Convert symbolic references to column names
        names_col = _resolve_columns(names_from, df, single=True)
        
        # Handle id_cols
        if id_cols is None:
            # Use all columns except names_from and values_from
            id_columns = [col for col in df.columns 
                         if col != names_col and 
                         (values_from is None or col not in _resolve_columns(values_from, df))]
        else:
            id_columns = _resolve_columns(id_cols, df)
        
        # Handle values_from
        if values_from is None:
            # Use all columns except names_from and id_cols
            value_columns = [col for col in df.columns 
                           if col != names_col and col not in id_columns]
        else:
            value_columns = _resolve_columns(values_from, df)
        
        # Perform the pivot
        result = df.pivot(
            on=names_col,
            index=id_columns if id_columns else None,
            values=value_columns if value_columns else None,
            aggregate_function=values_fn,
            sort_columns=sort_columns
        )
        
        # Apply names_prefix if specified
        if names_prefix:
            # Get columns that were created by pivoting (exclude id_cols)
            pivoted_cols = [col for col in result.columns if col not in id_columns]
            rename_map = {col: f"{names_prefix}{col}" for col in pivoted_cols}
            result = result.rename(rename_map)
        
        # Apply values_fill if specified
        if values_fill is not None:
            result = result.fill_null(values_fill)
        
        return result
    
    return _pivot_wider

# Define the pivot_longer() verb
def pivot_longer(cols=None, names_to="name", values_to="value", 
                 cols_vary="fastest"):
    """
    Pivot DataFrame from wide to long format.
    
    cols: Column(s) to pivot into longer format (if None, pivots all columns)
          Can use _.col, [_.col1, _.col2], ~_.col for exclusion, or _.col1 | _.col2 for ranges
    names_to: Name for the new column containing former column names
    values_to: Name for the new column containing the values
    cols_vary: Not implemented yet (for future compatibility with tidyr)
    
    Usage:
        df >> pivot_longer(cols=[_.cat1, _.cat2, _.cat3], names_to="category", values_to="value")
        df >> pivot_longer(cols=~_.id, names_to="variable", values_to="measurement")
    """
    def _pivot_longer(df):
        # Handle column selection
        if cols is None:
            # Pivot all columns
            cols_to_pivot = df.columns
            id_cols = None
        else:
            cols_to_pivot, id_cols = _resolve_pivot_cols(cols, df)
        
        # Perform the unpivot
        result = df.unpivot(
            on=cols_to_pivot,
            index=id_cols,
            variable_name=names_to,
            value_name=values_to
        )
        
        return result
    
    return _pivot_longer


def _resolve_columns(cols, df, single=False):
    """
    Convert symbolic column references to actual column names.
    
    cols: SymbolicAttr, list of SymbolicAttr, or string/list of strings
    df: The DataFrame to resolve against
    single: If True, return a single string; if False, return a list
    
    Returns column name(s) as string or list of strings
    """    
    if isinstance(cols, SymbolicAttr):
        result = cols.name
    elif isinstance(cols, (list, tuple)):
        result = [c.name if isinstance(c, SymbolicAttr) else c for c in cols]
        if single and len(result) == 1:
            result = result[0]
    else:
        result = cols
    
    return result


def _resolve_pivot_cols(cols, df):
    """
    Resolve column selection for pivot_longer, handling exclusions and ranges.
    
    cols: Column specification (can include ~_.col for exclusion or _.col1 | _.col2 for range)
    df: The DataFrame to resolve against
    
    Returns: (cols_to_pivot, id_cols) tuple of lists
    """    
    # Handle DeSelect (~_.col syntax)
    if isinstance(cols, DeSelect):
        if isinstance(cols.col, SymbolicAttr):
            # Exclude single column
            excluded = [cols.col.name]
        elif isinstance(cols.col, (list, tuple)):
            # Exclude multiple columns
            excluded = [c.name if isinstance(c, SymbolicAttr) else c for c in cols.col]
        else:
            excluded = [cols.col]
        
        id_cols = excluded
        cols_to_pivot = [c for c in df.columns if c not in excluded]
    
    # Handle ColumnRange (_.col1 | _.col2 syntax)
    elif isinstance(cols, ColumnRange):
        start_name = cols.start.name if isinstance(cols.start, SymbolicAttr) else cols.start
        end_name = cols.end.name if isinstance(cols.end, SymbolicAttr) else cols.end
        
        # Get slice of columns between start and end (inclusive)
        start_idx = df.columns.index(start_name)
        end_idx = df.columns.index(end_name)
        cols_to_pivot = df.columns[start_idx:end_idx + 1]
        id_cols = [c for c in df.columns if c not in cols_to_pivot]
    
    # Handle normal column selection
    else:
        cols_to_pivot = _resolve_columns(cols, df)
        if not isinstance(cols_to_pivot, list):
            cols_to_pivot = [cols_to_pivot]
        id_cols = [c for c in df.columns if c not in cols_to_pivot]
    
    return cols_to_pivot, id_cols if id_cols else None