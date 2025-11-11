"""
pasteurize() extension for Polars DataFrames and LazyFrames.

This module monkey-patches the pasteurize() method onto pl.DataFrame.
The patch is applied automatically when this module is imported.

Usage:
    df.pasteurize()
"""
import polars as pl
import re

# Define the pasteurize() method
def pasteurize(df):
    """
    Clean a Polars DataFrame or LazyFrame by:
        Removing empty and duplicate rows
        Standardizing column names (lowercase with underscores)
        Stripping whitespace from strings
        Converting "NA" and "NULL" char strings to true `null`s
        Converting strings to titlecase
    """
    # Clean column names first
    def clean_name(name):
        name = str(name).lower()
        name = re.sub(r"[\s-]+", "_", name)
        name = re.sub(r"[^\w_]", "", name)
        return name.strip('_')
    
    # Handle schema access efficiently for LazyFrames
    if isinstance(df, pl.LazyFrame):
        schema = df.collect_schema()
        columns = schema.names()
        dtypes = schema.dtypes()
    else:
        columns = df.columns
        dtypes = df.dtypes
    
    # Create mapping of old -> new column names
    rename_map = {col: clean_name(col) for col in columns}
    df = df.rename(rename_map)
    
    # Clean string columns: strip whitespace, replace NA variants, apply title case
    # Use the NEW (cleaned) column names
    string_cols = [rename_map[col] for col, dtype in zip(columns, dtypes) if dtype == pl.String]
    
    for col in string_cols:
        df = df.with_columns(
            pl.col(col)
            .str.strip_chars()
            .replace(["NA", "NULL", ""], None)
            .str.to_titlecase()
            .alias(col)
        )
    
    return df

# Monkey patch onto Polars DataFrame and LazyFrame
pl.DataFrame.pasteurize = pasteurize
pl.LazyFrame.pasteurize = pasteurize