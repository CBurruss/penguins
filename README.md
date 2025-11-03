# penguins
a port of the dplyr-based siuba package for polars

## About penguins

I developed penguins because I love what [siuba](https://github.com/machow/siuba/blob/main/README.md) provides for pandas, and I wanted to bring the same versatility of R's tidyverse to [polars](https://github.com/pola-rs/polars). With that in mind, I wanted to create a package that would let me leverage the superior performance of polars (over pandas) with the versatility of [dplyr](https://github.com/tidyverse/dplyr). This is ultimately what makes siuba so powerful as an add-on for pandas, and why I think penguins is such a great addition to polars. 

## Installation

You can install the dev version of penguins with:

```python
pip install git+https://github.com/CBurruss/penguins.git
```

## What's Inside

If we look at the penguins package, we can group its utilities into three main categories — core functionality, verb functions, and acutis functions.

### Core functionality

At its core, penguins provides a dplyr-flavored  interface for polars through two main features:

 - The pipe operator `>>` — enables function function chaining akin to R's `|>` pipe
 - The symbolic placeholder `_` — acts as a helper by standing in for two main use cases:
      1. DataFrame references in method calls — e.g. `df >> _.head(5)`
      2. Column references in verb expressions — e.g. `df >> select(_.col)`

### Verb functions

As hinted at above, penguins gains most of its utility from its dplyr-styled functions. While they'll be covered in the Examples section, here are the functions that have currently been ported over:
1. `select()` — select specific columns from the DataFrame
2. `filter()` — filter rows based on boolean conditions
3. `mutate()` — create new columns or modify existing ones
4. `group_by()` —  group DataFrame by one or more columns
5. `summarize()` — aggregate data, typically after `group_by()`
6. `head()` — return first n rows
7. `tail()` — return last n rows
8. `slice()` — select rows by position
9. `distinct()` — keep only unique rows based on specified columns
10. `arrange()` — sort rows by column expressions
11. `relocate()` — reorder columns in a DataFrame
12. `rename()` — rename columns
13. `round()` — round numeric columns to specified decimal places

### Acutis methods

Unlike its more principled pandas counterpart (siuba), penguins takes the [careless] liberty of extending polars objects with both implicit and explicit methods! Each of these were ported from my [acutis](https://github.com/CBurruss/acutis) R package and provide handy functionality for typical data processsing and handling. 

**Explicit import required:**
 - `affiche()` — display a Polars DataFrame with aethetic table borders and styling (from the French *affiche* to display something)
     - As a bonus, this is also provided as a function! 
 - `count_table()` — create a frequency table with counts and percentages
 - `pasteurize()` — clean a DataFrame by removing empty rows, duplicates, and standardizing column names

**Implicilty patched in:**  
 - `not_in()` — perform the inverse of the `is_in()` method
 -  `not_like()` — perform the inverse of the `str.contains()` method

## Examples

For starters, we'll load in the palmers penguins dataset:
```python
import polars as pl

df = pl.read_csv("./data/penguins.csv")
```

### Functions

### Methods

#### 1. `affiche()`
```python

```

#### 2. `count_table()`
```python
from penguins import acutis

df["species"].count_table()
```

## Dependencies
Obviously enough, penguins really just relies on polars for doing all of its data manipulation.

## Notes
Penguin data from `palmerpenguins` R package: https://github.com/allisonhorst/palmerpenguins