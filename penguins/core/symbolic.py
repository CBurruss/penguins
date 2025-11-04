# Establish symbolic attribution for polars dataframes
import polars as pl
from penguins.core.pipe import MethodCall

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
    
    # Patch in custom not_in() function 
    def not_in(self, values):
        """
        Check if values are NOT in the given list.
        
        Inverse of is_in()
        
        Usage: df >> filter(_.col.not_in([1, 2, 3]))
        """
        return ~self._expr.is_in(values)
    
    # Patch in cusotm not_like() function
    def not_like(self, pattern):
        """
        Check if string does NOT contain the pattern.
        
        Inverse of str.contains()
        
        Usage: df >> filter(_.col.not_like("pattern"))
        """
        return ~self._expr.str.contains(pattern)
    
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