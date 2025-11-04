"""
penguins: a siuba-styled addon for polars
"""

# core imports
from penguins.core.symbolic import _, Symbolic
from penguins.core import pipe

# acutis imports 
from penguins import acutis
from penguins.acutis.affiche import affiche
from penguins.acutis.pasteurize import pasteurize
from penguins.acutis.count_table import count_table

# verb imports
from penguins.verbs.select import select
from penguins.verbs.mutate import mutate
from penguins.verbs.filter import filter
from penguins.verbs.arrange import arrange
from penguins.verbs.rename import rename
from penguins.verbs.group_by import group_by
from penguins.verbs.summarize import summarize
from penguins.verbs.round import round
from penguins.verbs.head import head
from penguins.verbs.tail import tail
from penguins.verbs.distinct import distinct 
from penguins.verbs.slice import slice
from penguins.verbs.relocate import relocate 

# helper imports
from penguins.verbs.select import starts_with, ends_with, contains
from penguins.verbs.mutate import across, where, is_numeric, is_integer, is_float, \
    is_string, is_boolean, is_temporal

# set version
__version__ = "0.2.0"

# add to primary import 
__all__ = ['_', 'Symbolic', 'select', 'mutate', 'filter', 'arrange', 'rename', 'group_by',
           'summarize', 'round', 'head', 'tail', 'distinct', 'slice', 'relocate', 
           'affiche', 'pasteurize', 'count_table', 'starts_with', 'ends_with', 'contains', 
           'across', 'where', 'is_numeric', 'is_integer', 'is_float', 'is_string', 
           'is_boolean', 'is_temporal']