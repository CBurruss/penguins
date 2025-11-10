# Define the count_null() method
"""
count_null extension for Polars DataFrame and LazyFrame.

This module monkey-patches the count_null() method onto pl.DataFrame.
The patch is applied automatically when this module is imported.

Usage:
    df.count_null()
"""
import polars as pl

def count_null(self):
    """
    Count null values for each column in a DataFrame, with percentages.
    Usage: df.count_null()
    """
    # Collect LazyFrame if needed
    if isinstance(self, pl.LazyFrame):
        df = self.collect()
    else:
        df = self
    
    # Get null counts for each column
    null_counts = df.null_count().transpose(
        include_header=True,
        header_name="col",
        column_names=["null_count"]
    )
    
    # Calculate percentages
    total_rows = len(df)
    null_counts = null_counts.with_columns([
        # Calculate raw percentage
        pl.when(pl.col("null_count") == 0)
          .then(pl.lit("0%"))
          .when((pl.col("null_count") / total_rows) <= 0.0099)
          .then(pl.lit("<1%"))
          .otherwise(
              (pl.col("null_count") / total_rows * 100)
              .round(0)
              .cast(pl.Int64)
              .cast(pl.Utf8) + "%"
          )
          .alias("null_percent")
    ])
    
    # Sort by missing count descending
    return null_counts.sort("null_count", descending=True)

# Monkey patch onto polars DataFrame and LazyFrame
pl.DataFrame.count_null = count_null
pl.LazyFrame.count_null = count_null 