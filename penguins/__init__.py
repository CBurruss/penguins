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
from penguins.acutis.count_null import count_null

# verb imports
from penguins.verbs.select import select
from penguins.verbs.mutate import mutate, across
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
from penguins.verbs.drop_null import drop_null
from penguins.verbs.pull import pull
from penguins.verbs.sample import sample
from penguins.verbs.join import join
from penguins.verbs.pivot import pivot_longer, pivot_wider
from penguins.verbs.unite import unite
from penguins.verbs.separate import separate
from penguins.verbs.bind_cols import bind_cols
from penguins.verbs.bind_rows import bind_rows
from penguins.verbs.reframe import reframe

# utils + helper imports
from penguins.utils.if_else import if_else
from penguins.utils.case_when import case_when
from penguins.utils.row_contains import row_contains
from penguins.utils.helpers import starts_with, ends_with, contains, where, is_numeric, \
    is_integer, is_float, is_string, is_boolean, is_temporal, is_null, is_cat
    
# set version
__version__ = "0.3.1"

# add to primary import 
__all__ = ['_', 'Symbolic', 'select', 'mutate', 'filter', 'arrange', 'rename', 'group_by',
           'summarize', 'round', 'head', 'tail', 'distinct', 'slice', 'relocate', 'drop_null',
           'pull', 'sample', 'affiche', 'pasteurize', 'count_table', 'count_null', 'starts_with', 
           'ends_with', 'contains', 'across', 'where', 'is_numeric', 'is_integer', 'is_float', 
           'is_string', 'is_boolean', 'is_temporal', 'is_null', 'if_else', 'is_null', 'is_cat', 
           'case_when', 'join', 'pivot_longer', 'pivot_wider', 'unite', 'separate', 'bind_rows', 'bind_cols', 
           'row_contains', 'reframe']