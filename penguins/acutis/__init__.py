"""
Acutis module: Extended methods for Polars objects.

Importing this module adds additional methods to Polars Series and DataFrame objects.
"""

from penguins.acutis.affiche import affiche             # Imports both the function and the method 
from penguins.acutis.count_table import count_table
from penguins.acutis.count_null import count_null
from penguins.acutis.pasteurize import pasteurize

__all__ = ['affiche', 'count_table', 'count_null', 'pasteurize']