# Define the count_table() method
"""
count_table extension for Polars Series, DataFrame and LazyFrame.

This module monkey-patches the count_table() method onto pl.Series and pl.DataFrame.
The patch is applied automatically when this module is imported.

Usage:
    For Series: series.count_table()
    For DataFrame: df["column"].count_table()
    For LazyFrame: lf.select("column").count_table()
"""
import polars as pl

def count_table(self):
    """
    Create a count table with counts and percentages for a Series or DataFrame column.
    
    For Series: series.count_table()
    For DataFrame: df["column"].count_table()
    For LazyFrame: lf.select("column").count_table()
    """
    # Handle DataFrame/LazyFrame - take first column
    if isinstance(self, (pl.DataFrame, pl.LazyFrame)):
        # Collect LazyFrame if needed
        if isinstance(self, pl.LazyFrame):
            self = self.collect()
            
        if self.shape[1] != 1:
            raise ValueError("count_table() requires a DataFrame with exactly one column")
        series = self[self.columns[0]]
        col_name = self.columns[0]
    else:
        series = self
        col_name = series.name or "value"
    
    # Get value counts including nulls
    table = (
        series.value_counts(sort=True)
        .sort(pl.col("count"), descending=True)
    )
    
    # Rename columns
    table = table.rename({series.name: col_name})
    
    # Calculate percentages
    total = table["count"].sum()
    table = table.with_columns(
        pl.when(pl.col("count") == 0)
        .then(pl.lit("0%"))
        .when((pl.col("count") / total * 100) < 1)
        .then(pl.lit("<1%"))
        .otherwise(
            (pl.col("count") / total * 100).round(0).cast(pl.Int64).cast(pl.Utf8) + "%"
        )
        .alias("percent")
    )
    
    return table

# Monkey-patch onto both Series and DataFrame
pl.Series.count_table = count_table
pl.DataFrame.count_table = count_table
pl.LazyFrame.count_table = count_table  