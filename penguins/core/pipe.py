# Establish the pipe operator >> for polars
import polars as pl

class MethodCall:
    """
    Represents a method call to be executed on a DataFrame.
    
    Used when piping to DataFrame methods via _.method_name()
    """
    def __init__(self, method_name, args, kwargs):
        self.method_name = method_name
        self.args = args
        self.kwargs = kwargs
    
    def __call__(self, df):
        """
        Execute the method call on the DataFrame.
        
        df: The Polars DataFrame to call the method on
        
        Returns the result of the method call
        """
        method = getattr(df, self.method_name)
        return method(*self.args, **self.kwargs)

def _pipe_rshift(self, other):
    """
    Pipe operator for Polars DataFrames.
    
    self: The Polars DataFrame
    other: Either a verb function or a MethodCall object
    
    Returns the result of applying the verb function or method call.
    """
    # Check if other is a MethodCall (from _.method_name())
    if isinstance(other, MethodCall):
        return other(self)
    # Otherwise it's a verb function
    return other(self)

# Monkey-patch Polars DataFrame
pl.DataFrame.__rshift__ = _pipe_rshift

# Make Polars GroupBy pipeable
pl.dataframe.group_by.GroupBy.__rshift__ = _pipe_rshift

# Add LazyFrame support
pl.LazyFrame.__rshift__ = _pipe_rshift
pl.lazyframe.group_by.LazyGroupBy.__rshift__ = _pipe_rshift