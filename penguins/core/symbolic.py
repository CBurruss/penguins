# Establish symbolic attribution for polars dataframes
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
        
        df: The DataFrame to call the method on
        
        Returns the result of the method call
        """
        method = getattr(df, self.method_name)
        return method(*self.args, **self.kwargs)

class SymbolicAttr:
    """
    Intermediate object returned by _.attribute_name
    
    Can become either a Polars expression or a method call.
    """
    def __init__(self, name):
        self.name = name
        self._expr = pl.col(name)
    
    def __call__(self, *args, **kwargs):
        """
        Called when used as _.method_name() in a pipe.
        
        Returns a MethodCall object for piping.
        """
        return MethodCall(self.name, args, kwargs)
    
    def __getattr__(self, attr):
        """
        Forward attribute access to the Polars expression.
    
        Allows chaining like _.column_name.fill_null()
        """
        # Check if this is an aggregation method we need to track for pandas
        if attr in ['count', 'sum', 'mean', 'min', 'max', 'std', 'var', 'first', 'last', 'median']:
            # Return a ChainedSymbolicAttr that tracks the aggregation
            return ChainedSymbolicAttr(self.name, attr)
    
        return getattr(self._expr, attr)
    
    def __repr__(self):
        return repr(self._expr)
    
    def __neg__(self):
        """
        Support negation for descending sorts.
    
        Usage: df >> arrange(-_.column_name)
        """
        negated = SymbolicAttr(self.name)
        negated._is_negated = True
        negated._original = self._expr
        return negated
    
    def __eq__(self, other):
        """Support == comparisons"""
        return self._expr.__eq__(other)

    def __ne__(self, other):
        """Support != comparisons"""
        return self._expr.__ne__(other)

    def __lt__(self, other):
        """Support < comparisons"""
        return self._expr.__lt__(other)

    def __le__(self, other):
        """Support <= comparisons"""
        return self._expr.__le__(other)

    def __gt__(self, other):
        """Support > comparisons"""
        return self._expr.__gt__(other)

    def __ge__(self, other):
        """Support >= comparisons"""
        return self._expr.__ge__(other)
    
    # Add invert method to select()
    def __invert__(self):
        """
        Support deselection with ~ operator.
    
        Usage: df >> select(~_.column_name)
        """
        return DeSelect(self)
    
    # Add or method to select()
    def __or__(self, other):
        """
        Support range selection with | operator.
    
        Usage: df >> select(_.col1 | _.col2)
        """
        return ColumnRange(self, other)
    
    # Patch in custom not_in() method
    def not_in(self, values):
        """
        Check if values are NOT in the given list.
        
        Inverse of is_in()
        
        Usage: df >> filter(_.col.not_in([1, 2, 3]))
        """
        return ~self._expr.is_in(values)
    
    # Patch in custom not_like() method
    def not_like(self, pattern):
        """
        Check if string does NOT contain the pattern.
        
        Inverse of str.contains()
        
        Usage: df >> filter(_.col.not_like("pattern"))
        """
        return ~self._expr.str.contains(pattern)
    
    def __add__(self, other):
        """Support + addition"""
        if isinstance(other, SymbolicAttr):
            other = other._expr
        return self._expr.__add__(other)

    def __sub__(self, other):
        """Support - subtraction"""
        if isinstance(other, SymbolicAttr):
            other = other._expr
        return self._expr.__sub__(other)

    def __mul__(self, other):
        """Support * multiplication"""
        if isinstance(other, SymbolicAttr):
            other = other._expr
        return self._expr.__mul__(other)

    def __truediv__(self, other):
        """Support / division"""
        if isinstance(other, SymbolicAttr):
            other = other._expr
        return self._expr.__truediv__(other)

    def __floordiv__(self, other):
        """Support // floor division"""
        if isinstance(other, SymbolicAttr):
            other = other._expr
        return self._expr.__floordiv__(other)

    def __mod__(self, other):
        """Support % modulo"""
        if isinstance(other, SymbolicAttr):
            other = other._expr
        return self._expr.__mod__(other)

    def __pow__(self, other):
        """Support ** exponentiation"""
        if isinstance(other, SymbolicAttr):
            other = other._expr
        return self._expr.__pow__(other)
    
class ChainedSymbolicAttr(SymbolicAttr):
    """
    Tracks chained method calls on symbolic attributes for pandas compatibility.
    """
    def __init__(self, name, agg_func):
        self.name = name
        self._agg_func = agg_func
        self._expr = pl.col(name)
    
# Establish symbolic class for polars dataframes
class Symbolic:
    """
    Symbolic column reference object that creates Polars expressions.
    
    Usage: 
    - _.column_name returns a SymbolicAttr (acts like pl.col("column_name"))
    - _.method() returns a MethodCall for piping to DataFrame methods
    """
    def __getattr__(self, name):
        """
        Intercept attribute access to create SymbolicAttr objects.
        
        name: The column or method name being referenced
        
        Returns a SymbolicAttr that can be used as an expression or called as a method
        """
        return SymbolicAttr(name)
    
# Helper classes for column selection patterns
class ColumnRange:
    """
    Represents a range of columns for selection.
    
    Created using the : operator between two SymbolicAttr objects.
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def __invert__(self):
        """Support ~ operator for deselection."""
        return DeSelect(self)

class DeSelect:
    """
    Represents columns to exclude from selection.
    
    Created using the ~ operator before a SymbolicAttr or helper function.
    """
    def __init__(self, col):
        self.col = col
    
# Create the global _ object for column references
_ = Symbolic()