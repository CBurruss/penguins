# penguins
penguins is a port of the dplyr-based siuba package for polars

## Extended Methods (acutis)

Penguins includes extended methods that are added to Polars objects:
```python
from penguins import acutis
import polars as pl

# Now available on any Series or DataFrame
df["species"].count_table()
```

Available methods:
- `count_table()`: Create frequency tables with counts and percentages