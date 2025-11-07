from penguins.core.symbolic import SymbolicAttr

# Define the sample() verb
def sample(n=None, frac=None, with_replacement=False, shuffle=False, seed=None):
    """
    Sample rows from a DataFrame.
    
    n: Number of rows to sample (integer)
    frac: Fraction of rows to sample (float between 0 and 1)
    with_replacement: Whether to sample with replacement (default False)
    shuffle: Whether to shuffle before sampling (default False)
    seed: Random seed for reproducibility
    
    Returns a function that samples from a DataFrame when piped.
    
    Usage: df >> sample(n=10) or df >> sample(frac=0.1)
    """
    def _sample(df):
        return df.sample(n=n, fraction=frac, with_replacement=with_replacement, 
                        shuffle=shuffle, seed=seed)
    return _sample