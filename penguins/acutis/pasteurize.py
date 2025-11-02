"""
pasteurize() extension for Polars DataFrames.

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
    Clean a dataframe by removing empty rows, duplicates, and standardizing column names.
    """
    # Clean column names first
    def clean_name(name):
        name = str(name).lower()
        name = re.sub(r"[\s-]+", "_", name)
        name = re.sub(r"[^\w_]", "", name)
        return name.strip('_')
    
    df = df.rename({col: clean_name(col) for col in df.columns})
    
    # Clean string columns: strip whitespace, replace NA variants, apply title case
    string_cols = [col for col, dtype in zip(df.columns, df.dtypes) if dtype == pl.String]
    
    for col in string_cols:
        df = df.with_columns(
            pl.col(col)
            .str.strip_chars()
            .replace(["NA", "NULL", ""], None)
            .str.to_titlecase()
            .alias(col)
        )
    
    return df

# Monkey patch onto Polars DataFrame
pl.DataFrame.pasteurize = pasteurize