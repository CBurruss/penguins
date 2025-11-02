from penguins.core.symbolic import SymbolicAttr

# Define the filter() verb
def filter(*conditions):
    """
    Filter rows based on boolean conditions.
    
    *conditions: One or more boolean expressions using _
                 Multiple conditions are combined with AND logic
    
    Returns a function that performs the filtering on a DataFrame.
    """
    def _filter(df):
        # Extract expressions from SymbolicAttr if needed
        exprs = []
        for condition in conditions:
            if isinstance(condition, SymbolicAttr):
                exprs.append(condition._expr)
            else:
                # Already a Polars expression
                exprs.append(condition)
        
        # Combine all conditions with AND logic
        combined = exprs[0]
        for expr in exprs[1:]:
            combined = combined & expr
        
        # Call Polars' filter method
        return df.filter(combined)
    
    return _filter