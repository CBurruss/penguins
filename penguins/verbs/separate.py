from penguins.core.symbolic import SymbolicAttr
import polars as pl
import warnings

def separate(col, into, sep, regex=False, drop=True, fill="right"):
    """
    Split one column into multiple columns.
    
    col: SymbolicAttr or string name of column to split
    into: List of new column names
    sep: Separator string or regex pattern
    regex: Whether sep is a regex pattern (default False)
    drop: Whether to drop source column (default True)
    fill: How to handle too few splits - "right", "left", or "error" (default "right")
    
    Returns a function that takes a DataFrame and returns the modified DataFrame
    
    Usage: df >> separate(_.col, into=["a", "b"], sep="_")
    """
    def _separate(df):
        # Extract column name
        col_name = col.name if isinstance(col, SymbolicAttr) else col
        
        # Get column index to insert new columns to the right
        col_idx = df.columns.index(col_name)
        
        # Split the column
        if regex:
            split_expr = pl.col(col_name).str.split(sep)
        else:
            # Escape special regex chars for literal split
            import re
            escaped_sep = re.escape(sep)
            split_expr = pl.col(col_name).str.split(escaped_sep)
        
        # Create list column
        result = df.with_columns(split_expr.alias("__temp_split__"))
        
        # Check split counts and warn if mismatched
        split_lengths = result.select(
            pl.col("__temp_split__").list.len().alias("len")
        )["len"]
        
        max_len = split_lengths.max()
        min_len = split_lengths.min()
        expected_len = len(into)
        
        if max_len > expected_len:
            warnings.warn(
                f"Some splits produced {max_len} parts but only {expected_len} columns requested. "
                f"Extra parts will be ignored."
            )
        
        if min_len < expected_len and fill == "error":
            raise ValueError(
                f"Some splits produced fewer than {expected_len} parts. "
                f"Use fill='right' or fill='left' to handle this."
            )
        
        # Extract each position into new columns
        new_cols = []
        for i, col_name_new in enumerate(into):
            if fill == "left":
                # Fill from the right, so adjust index
                idx_expr = pl.col("__temp_split__").list.len() - expected_len + i
                new_cols.append(
                    pl.when(idx_expr >= 0)
                    .then(pl.col("__temp_split__").list.get(idx_expr))
                    .otherwise(None)
                    .alias(col_name_new)
                )
            else:  # "right" or "error"
                new_cols.append(
                    pl.col("__temp_split__").list.get(i).alias(col_name_new)
                )
        
        result = result.with_columns(new_cols)
        
        # Drop temporary column
        result = result.drop("__temp_split__")
        
        # Reorder columns to insert new ones after original
        original_cols = df.columns
        if drop:
            # Remove source column and insert new ones at its position
            reordered = (
                original_cols[:col_idx] + 
                into + 
                original_cols[col_idx + 1:]
            )
        else:
            # Insert new columns after source column
            reordered = (
                original_cols[:col_idx + 1] + 
                into + 
                original_cols[col_idx + 1:]
            )
        
        result = result.select(reordered)
        
        return result
    
    return _separate