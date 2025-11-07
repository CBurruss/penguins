from penguins.core.symbolic import SymbolicAttr

# Define the join() verb
def join(other, on=None, left_on=None, right_on=None, how="inner"):
    """
    Join two DataFrames together.
    
    Parameters:
    - other: DataFrame to join with
    - on: Column name(s) to join on (used when column names match)
    - left_on: Column name(s) from left DataFrame
    - right_on: Column name(s) from right DataFrame  
    - how: Join type:
        "inner", "left", "right", "outer", "cross", "semi", "anti"
    
    Usage:
        df >> join(other_df, on="id", how="left")
        df >> join(other_df, left_on="id", right_on="user_id", how="inner")
    """
    def _join(df):
        return df.join(other, on=on, left_on=left_on, right_on=right_on, how=how)
    return _join