from penguins.core.symbolic import SymbolicAttr, DeSelect, ColumnRange
import polars as pl 
import re

from penguins.utils.helpers import (
    StartsWithSelector, 
    EndsWithSelector, 
    ContainsSelector,
    starts_with,
    ends_with,
    contains
)

# Define function for handling conflicts
def _resolve_column_spec(spec, all_columns, df=None):
    """
    Resolve a column specification to a list of column names.
    
    spec: A column specification (string, SymbolicAttr, ColumnRange, or selector)
    all_columns: List of all column names in the DataFrame
    df: The DataFrame (needed for where() selectors to check dtypes)
    
    Returns a list of column names matching the specification.
    """
    # Import WhereSelector here to avoid circular imports
    from penguins.verbs.mutate import WhereSelector
    
    # Handle where() selector
    if isinstance(spec, WhereSelector):
        if df is None:
            raise ValueError("DataFrame required for where() selector")
        return [col for col in all_columns if spec.predicate(df[col].dtype)]
    
    # Handle SymbolicAttr
    if isinstance(spec, SymbolicAttr):
        return [spec.name]
    
    # Handle string column names
    if isinstance(spec, str):
        return [spec]
    
    # Handle column ranges (_.col1 : _.col2)
    if isinstance(spec, ColumnRange):
        start_name = spec.start.name if isinstance(spec.start, SymbolicAttr) else spec.start
        end_name = spec.end.name if isinstance(spec.end, SymbolicAttr) else spec.end
        
        start_idx = all_columns.index(start_name)
        end_idx = all_columns.index(end_name)
        
        return all_columns[start_idx:end_idx + 1]
    
    # Handle starts_with()
    if isinstance(spec, StartsWithSelector):
        if spec.is_regex:
            pattern = re.compile(f"({spec.prefix})$")
            return [col for col in all_columns if pattern.search(col)]
        else:
            return [col for col in all_columns if col.startswith(spec.prefix)]
    
    # Handle ends_with()
    if isinstance(spec, EndsWithSelector):
        if spec.is_regex:
            pattern = re.compile(f"({spec.suffix})$")
            return [col for col in all_columns if pattern.search(col)]
        else:
            return [col for col in all_columns if col.endswith(spec.suffix)]
    
    # Handle contains()
    if isinstance(spec, ContainsSelector):
        if spec.is_regex:
            pattern = re.compile(f"({spec.substring})$")
            return [col for col in all_columns if pattern.search(col)]
        else:
            return [col for col in all_columns if spec.substring in col]
    
    return []

# Modified select() verb
def select(*cols):
    """
    Select specific columns from the DataFrame.
    
    Supports:
    - Column names as strings or SymbolicAttr objects
    - Range selection: _.col1 : _.col2
    - Deselection: ~_.col_name
    - Pattern matching: starts_with(), ends_with(), contains()
    
    *cols: Variable number of column specifications
    
    Returns a function that performs the selection on a DataFrame.
    """
    def _select(df):
        all_columns = df.columns
        selected_cols = []
        excluded_cols = []
        
        for col in cols:
            # Handle deselection with ~
            if isinstance(col, DeSelect):
                excluded_cols.extend(_resolve_column_spec(col.col, all_columns, df))
            else:
                selected_cols.extend(_resolve_column_spec(col, all_columns, df))
        
        # If we have selections, use those; otherwise use all columns
        if not selected_cols:
            selected_cols = all_columns
        
        # Remove excluded columns
        final_cols = [c for c in selected_cols if c not in excluded_cols]
        
        return df.select(final_cols)
    
    return _select