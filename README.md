# penguins <img src="https://raw.githubusercontent.com/CBurruss/penguins/refs/heads/main/hex/penguins-hex.png" align="right" width="120" alt="Hexagonal logo for the penguins package" /> 

a port of the dplyr-based siuba package for polars

## About penguins

I developed penguins because I love what [siuba](https://github.com/machow/siuba/blob/main/README.md) provides for pandas, and I wanted to bring the same versatility of R's tidyverse to [polars](https://github.com/pola-rs/polars). With that in mind, I wanted to create a package that would let me leverage the superior performance of polars (over pandas) with the versatility of [dplyr](https://github.com/tidyverse/dplyr). This is ultimately what makes siuba so powerful as an add-on for pandas, and why I think penguins is such a great addition to polars. 

## Installation

You can install the dev version of penguins with:

```python
pip install git+https://github.com/CBurruss/penguins.git
```

## What's Inside

If we look at the penguins package, we can group its utilities into four main categories — 1) core functionality, 2) acutis methods, 3) verb functions, and 4) helper functions. 

### 1. Core functionality

At its core, penguins provides a dplyr-flavored interface for polars through two main features:

 - The pipe operator `>>` — enables function function chaining akin to R's `|>` pipe
 - The symbolic placeholder `_` — acts as a helper by standing in for two main use cases:
      1. DataFrame references in method calls — e.g. `df >> _.head(5)`
      2. Column references in verb expressions — e.g. `df >> select(_.col)`

### 2. Acutis methods

Unlike its more principled pandas counterpart (siuba), penguins takes the [careless] liberty of extending polars objects with both implicit and explicit methods! Each of these were ported from my [acutis](https://github.com/CBurruss/acutis) R package and provide handy functionality for typical data processsing and handling. 

**Explicit import required:**
 - `affiche()` — display a Polars DataFrame with aethetic table borders and styling (from the French *affiche* to display something)
     - As a bonus, this is also provided as a function! 
 - `count_table()` — create a frequency table with counts and percentages
 - `pasteurize()` — clean a DataFrame by removing empty rows, duplicates, and standardizing column names

**Implicilty patched in:**  
 - `not_in()` — perform the inverse of the `is_in()` method
 - `not_like()` — perform the inverse of the `str.contains()` method

### 3. Verb functions

As hinted at above, penguins gains most of its utility from its dplyr-styled functions. While they'll be covered in the [Examples](#examples) section, here are the verb functions that have currently been ported over:
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

### 4. Helper functions

As of release `v.0.2.0`, included are various helper functions to assist in column selection within `select()` and `mutate()`:
1. `across()` — allows the application of a function across columns
2. `where()` — for subsetting columns based on one or more conditions
     - Supports `is_numeric`, `is_integer`, `is_float`, `is_string`, `is_boolean` and `is_temporal` as boolean checks for column data types
     - As well as pattern matching on column names with `starts_with()`, `ends_with()` and `contains()` 

## Examples

For starters, we'll load in the palmers penguins dataset:
```python
import polars as pl
from penguins import *
from importlib.resources import files

# Read in the penguins file
data_path = files('penguins.data').joinpath('penguins.csv')
df = pl.read_csv(data_path)

# Preview the penguins table
df.head(5) >> print
```

```
shape: (5, 9)
┌───────┬─────────┬───────────┬────────────────┬───┬───────────────────┬─────────────┬────────┬──────┐
│ rowid ┆ species ┆ island    ┆ bill_length_mm ┆ … ┆ flipper_length_mm ┆ body_mass_g ┆ sex    ┆ year │
│ ---   ┆ ---     ┆ ---       ┆ ---            ┆   ┆ ---               ┆ ---         ┆ ---    ┆ ---  │
│ i64   ┆ str     ┆ str       ┆ str            ┆   ┆ str               ┆ str         ┆ str    ┆ i64  │
╞═══════╪═════════╪═══════════╪════════════════╪═══╪═══════════════════╪═════════════╪════════╪══════╡
│ 1     ┆ Adelie  ┆ Torgersen ┆ 39.1           ┆ … ┆ 181               ┆ 3750        ┆ male   ┆ 2007 │
│ 2     ┆ Adelie  ┆ Torgersen ┆ 39.5           ┆ … ┆ 186               ┆ 3800        ┆ female ┆ 2007 │
│ 3     ┆ Adelie  ┆ Torgersen ┆ 40.3           ┆ … ┆ 195               ┆ 3250        ┆ female ┆ 2007 │
│ 4     ┆ Adelie  ┆ Torgersen ┆ NA             ┆ … ┆ NA                ┆ NA          ┆ NA     ┆ 2007 │
│ 5     ┆ Adelie  ┆ Torgersen ┆ 36.7           ┆ … ┆ 193               ┆ 3450        ┆ female ┆ 2007 │
└───────┴─────────┴───────────┴────────────────┴───┴───────────────────┴─────────────┴────────┴──────┘
```

### Methods

#### 1. `affiche()`

<details>
<summary>View examples</summary>

```python
df.head(5).affiche()
```

```
╔═══════╦═════════╦═══════════╦════════════════╦═══════════════╦═══════════════════╦═════════════╦════════╦═══════╗
║ rowid ║ species ║ island    ║ bill_length_mm ║ bill_depth_mm ║ flipper_length_mm ║ body_mass_g ║ sex    ║ year  ║
║ int64 ║ str     ║ str       ║ str            ║ str           ║ str               ║ str         ║ str    ║ int64 ║
╠═══════╬═════════╬═══════════╬════════════════╬═══════════════╬═══════════════════╬═════════════╬════════╬═══════╣
║ 1     ║ Adelie  ║ Torgersen ║ 39.1           ║ 18.7          ║ 181               ║ 3750        ║ male   ║ 2007  ║
║ 2     ║ Adelie  ║ Torgersen ║ 39.5           ║ 17.4          ║ 186               ║ 3800        ║ female ║ 2007  ║
║ 3     ║ Adelie  ║ Torgersen ║ 40.3           ║ 18            ║ 195               ║ 3250        ║ female ║ 2007  ║
║ 4     ║ Adelie  ║ Torgersen ║ NA             ║ NA            ║ NA                ║ NA          ║ NA     ║ 2007  ║
║ 5     ║ Adelie  ║ Torgersen ║ 36.7           ║ 19.3          ║ 193               ║ 3450        ║ female ║ 2007  ║
╚═══════╩═════════╩═══════════╩════════════════╩═══════════════╩═══════════════════╩═════════════╩════════╩═══════╝
```
</details> 

#### 2. `count_table()`

<details>
<summary>View examples</summary>

```python
df["island"].count_table().affiche()
```

```
╔═══════════╦════════╦═════════╗
║ island    ║ count  ║ percent ║
║ str       ║ uint32 ║ str     ║
╠═══════════╬════════╬═════════╣
║ Biscoe    ║ 168    ║ 49%     ║
║ Dream     ║ 124    ║ 36%     ║
║ Torgersen ║ 52     ║ 15%     ║
╚═══════════╩════════╩═════════╝
```
</details> 

#### 3. `pasteurize()`

<details>
<summary>View examples</summary>

By default, this palmers dataset has "NA" string values:

```python
df["sex"].count_table().affiche()

```
```
╔════════╦════════╦═════════╗
║ sex    ║ count  ║ percent ║
║ str    ║ uint32 ║ str     ║
╠════════╬════════╬═════════╣
║ male   ║ 168    ║ 49%     ║
║ female ║ 165    ║ 48%     ║
║ NA     ║ 11     ║ 3%      ║
╚════════╩════════╩═════════╝
```

However, applying `pasteurize()` automatically converts them to true missing `null` values:

```python
df.pasteurize()["sex"].count_table().affiche()
```
```
╔════════╦════════╦═════════╗
║ sex    ║ count  ║ percent ║
║ str    ║ uint32 ║ str     ║
╠════════╬════════╬═════════╣
║ Male   ║ 168    ║ 49%     ║
║ Female ║ 165    ║ 48%     ║
║ null   ║ 11     ║ 3%      ║
╚════════╩════════╩═════════╝
```

</details> 

#### 4. `not_in()`

<details>
<summary>View examples</summary>

```python
# We'll preview the filter() function here,
# which will be covered in the Functions examples
# And use affiche() as function instead of a method
df >> filter(_.rowid.not_in(range(1, 339))) \
    >> affiche()
```

```
╔═══════╦═══════════╦════════╦════════════════╦═══════════════╦═══════════════════╦═════════════╦════════╦═══════╗
║ rowid ║ species   ║ island ║ bill_length_mm ║ bill_depth_mm ║ flipper_length_mm ║ body_mass_g ║ sex    ║ year  ║
║ int64 ║ str       ║ str    ║ str            ║ str           ║ str               ║ str         ║ str    ║ int64 ║
╠═══════╬═══════════╬════════╬════════════════╬═══════════════╬═══════════════════╬═════════════╬════════╬═══════╣
║ 339   ║ Chinstrap ║ Dream  ║ 45.7           ║ 17            ║ 195               ║ 3650        ║ female ║ 2009  ║
║ 340   ║ Chinstrap ║ Dream  ║ 55.8           ║ 19.8          ║ 207               ║ 4000        ║ male   ║ 2009  ║
║ 341   ║ Chinstrap ║ Dream  ║ 43.5           ║ 18.1          ║ 202               ║ 3400        ║ female ║ 2009  ║
║ 342   ║ Chinstrap ║ Dream  ║ 49.6           ║ 18.2          ║ 193               ║ 3775        ║ male   ║ 2009  ║
║ 343   ║ Chinstrap ║ Dream  ║ 50.8           ║ 19            ║ 210               ║ 4100        ║ male   ║ 2009  ║
║ 344   ║ Chinstrap ║ Dream  ║ 50.2           ║ 18.7          ║ 198               ║ 3775        ║ female ║ 2009  ║
╚═══════╩═══════════╩════════╩════════════════╩═══════════════╩═══════════════════╩═════════════╩════════╩═══════╝
```

</details> 

#### 5. `not_like()`

<details>
<summary>View examples</summary>

```python
# And here, we'll preview the head() function to be covered below
df >> filter(_.island.not_like("^B|D")) \
    >> head() \
    >> affiche()
```

```
╔═══════╦═════════╦═══════════╦════════════════╦═══════════════╦═══════════════════╦═════════════╦════════╦═══════╗
║ rowid ║ species ║ island    ║ bill_length_mm ║ bill_depth_mm ║ flipper_length_mm ║ body_mass_g ║ sex    ║ year  ║
║ int64 ║ str     ║ str       ║ str            ║ str           ║ str               ║ str         ║ str    ║ int64 ║
╠═══════╬═════════╬═══════════╬════════════════╬═══════════════╬═══════════════════╬═════════════╬════════╬═══════╣
║ 1     ║ Adelie  ║ Torgersen ║ 39.1           ║ 18.7          ║ 181               ║ 3750        ║ male   ║ 2007  ║
║ 2     ║ Adelie  ║ Torgersen ║ 39.5           ║ 17.4          ║ 186               ║ 3800        ║ female ║ 2007  ║
║ 3     ║ Adelie  ║ Torgersen ║ 40.3           ║ 18            ║ 195               ║ 3250        ║ female ║ 2007  ║
║ 4     ║ Adelie  ║ Torgersen ║ NA             ║ NA            ║ NA                ║ NA          ║ NA     ║ 2007  ║
║ 5     ║ Adelie  ║ Torgersen ║ 36.7           ║ 19.3          ║ 193               ║ 3450        ║ female ║ 2007  ║
╚═══════╩═════════╩═══════════╩════════════════╩═══════════════╩═══════════════════╩═════════════╩════════╩═══════╝
```

</details> 

### Functions

#### 1. `select()`

<details>
<summary>View examples</summary>

The simplest way of using `select()` is to specify columns with the underscore accessor `_`:

```python
df >> select(_.species, _.sex, _.year) \
    >> head() \
    >> affiche()
```
```
╔═════════╦════════╦═══════╗
║ species ║ sex    ║ year  ║
║ str     ║ str    ║ int64 ║
╠═════════╬════════╬═══════╣
║ Adelie  ║ male   ║ 2007  ║
║ Adelie  ║ female ║ 2007  ║
║ Adelie  ║ female ║ 2007  ║
║ Adelie  ║ NA     ║ 2007  ║
║ Adelie  ║ female ║ 2007  ║
╚═════════╩════════╩═══════╝
```

We can also use the inverse operator `~` for de-selecting columns:

```python
df >> select(~_.species, ~_.island, ~_.body_mass_g, ~_.sex) \
    >> head() \
    >> affiche()
```
```
╔═══════╦════════════════╦═══════════════╦═══════════════════╦═══════╗
║ rowid ║ bill_length_mm ║ bill_depth_mm ║ flipper_length_mm ║ year  ║
║ int64 ║ str            ║ str           ║ str               ║ int64 ║
╠═══════╬════════════════╬═══════════════╬═══════════════════╬═══════╣
║ 1     ║ 39.1           ║ 18.7          ║ 181               ║ 2007  ║
║ 2     ║ 39.5           ║ 17.4          ║ 186               ║ 2007  ║
║ 3     ║ 40.3           ║ 18            ║ 195               ║ 2007  ║
║ 4     ║ NA             ║ NA            ║ NA                ║ 2007  ║
║ 5     ║ 36.7           ║ 19.3          ║ 193               ║ 2007  ║
╚═══════╩════════════════╩═══════════════╩═══════════════════╩═══════╝
```

As well as the column range operator `|` for specifying a range of columns
```python
df >> select(_.bill_length_mm | _.body_mass_g) \
    >> head() \
    >> affiche()
```
```
╔════════════════╦═══════════════╦═══════════════════╦═════════════╗
║ bill_length_mm ║ bill_depth_mm ║ flipper_length_mm ║ body_mass_g ║
║ str            ║ str           ║ str               ║ str         ║
╠════════════════╬═══════════════╬═══════════════════╬═════════════╣
║ 39.1           ║ 18.7          ║ 181               ║ 3750        ║
║ 39.5           ║ 17.4          ║ 186               ║ 3800        ║
║ 40.3           ║ 18            ║ 195               ║ 3250        ║
║ NA             ║ NA            ║ NA                ║ NA          ║
║ 36.7           ║ 19.3          ║ 193               ║ 3450        ║
╚════════════════╩═══════════════╩═══════════════════╩═════════════╝
```

We can also use the unpacking operator `*` here:

```python
cols = ["species", "sex", "year"]

df >> select(*cols) \
    >> head(5) \
    >> affiche()
```
```
╔═════════╦════════╦═══════╗
║ species ║ sex    ║ year  ║
║ str     ║ str    ║ int64 ║
╠═════════╬════════╬═══════╣
║ Adelie  ║ male   ║ 2007  ║
║ Adelie  ║ female ║ 2007  ║
║ Adelie  ║ female ║ 2007  ║
║ Adelie  ║ NA     ║ 2007  ║
║ Adelie  ║ female ║ 2007  ║
╚═════════╩════════╩═══════╝
```

Further, `select()` allows for various selector functions: `starts_with()`, `ends_with()` and `contains()` 

```python
df >> select(ends_with("mm")) \
    >> head(5) \
    >> affiche()
```
```
╔════════════════╦═══════════════╦═══════════════════╗
║ bill_length_mm ║ bill_depth_mm ║ flipper_length_mm ║
║ str            ║ str           ║ str               ║
╠════════════════╬═══════════════╬═══════════════════╣
║ 39.1           ║ 18.7          ║ 181               ║
║ 39.5           ║ 17.4          ║ 186               ║
║ 40.3           ║ 18            ║ 195               ║
║ NA             ║ NA            ║ NA                ║
║ 36.7           ║ 19.3          ║ 193               ║
╚════════════════╩═══════════════╩═══════════════════╝
```

As well as using the inverse operator `~` on these helpers:

```python
df >> select(~(_.bill_length_mm | _.body_mass_g)) \
    >> select(~starts_with("row")) \
    >> head() \
    >> affiche()
```
```
╔═════════╦═══════════╦════════╦═══════╗
║ species ║ island    ║ sex    ║ year  ║
║ str     ║ str       ║ str    ║ int64 ║
╠═════════╬═══════════╬════════╬═══════╣
║ Adelie  ║ Torgersen ║ male   ║ 2007  ║
║ Adelie  ║ Torgersen ║ female ║ 2007  ║
║ Adelie  ║ Torgersen ║ female ║ 2007  ║
║ Adelie  ║ Torgersen ║ NA     ║ 2007  ║
║ Adelie  ║ Torgersen ║ female ║ 2007  ║
╚═════════╩═══════════╩════════╩═══════╝
```

</details> 

#### 2. `filter()`

<details>
<summary>View examples</summary>

```python
df >> filter(_.sex == "male", _.year == 2008) \
    >> select(_.rowid, _.sex, _.year) \
    >> head() \
    >> affiche()
```

```
╔═══════╦══════╦═══════╗
║ rowid ║ sex  ║ year  ║
║ int64 ║ str  ║ int64 ║
╠═══════╬══════╬═══════╣
║ 52    ║ male ║ 2008  ║
║ 54    ║ male ║ 2008  ║
║ 56    ║ male ║ 2008  ║
║ 58    ║ male ║ 2008  ║
║ 60    ║ male ║ 2008  ║
╚═══════╩══════╩═══════╝
```

</details> 

#### 3. `mutate()`

<details>
<summary>View examples</summary>

Conventionally, `mutate()` can be used to either modify columns in place or create new columns:

```python
df >> mutate(is_male = _.sex == "male") \
    >> select(_.rowid, _.sex, _.is_male) \
    >> head() \
    >> affiche()
```
```
╔═══════╦════════╦═════════╗
║ rowid ║ sex    ║ is_male ║
║ int64 ║ str    ║ bool    ║
╠═══════╬════════╬═════════╣
║ 1     ║ male   ║ True    ║
║ 2     ║ female ║ False   ║
║ 3     ║ female ║ False   ║
║ 4     ║ NA     ║ False   ║
║ 5     ║ female ║ False   ║
╚═══════╩════════╩═════════╝
```

But we can also specify `_before` or `_after` positional arguments: 

```python
df >> mutate(genus = None, _after = "species") \
    >> select(_.rowid | _.genus) \
    >> head() \
    >> affiche()
```
```
╔═══════╦═════════╦═══════╗
║ rowid ║ species ║ genus ║
║ int64 ║ str     ║ null  ║
╠═══════╬═════════╬═══════╣
║ 1     ║ Adelie  ║ null  ║
║ 2     ║ Adelie  ║ null  ║
║ 3     ║ Adelie  ║ null  ║
║ 4     ║ Adelie  ║ null  ║
║ 5     ║ Adelie  ║ null  ║
╚═══════╩═════════╩═══════╝
```

Importantly, `mutate()` allows for applying transformations across multiple columns with `across()`:

```python
df >> mutate(across([_.species, _.island], lambda x: x.str.to_lowercase())) \
    >> select(_.species, _.island) \
    >> head() \
    >> affiche()
```
```
╔═════════╦═══════════╗
║ species ║ island    ║
║ str     ║ str       ║
╠═════════╬═══════════╣
║ adelie  ║ torgersen ║
║ adelie  ║ torgersen ║
║ adelie  ║ torgersen ║
║ adelie  ║ torgersen ║
║ adelie  ║ torgersen ║
╚═════════╩═══════════╝
```

We can even use the selector helpers — `starts_with()`, `ends_with()` and `contains()` — within our `where()` call:

```python
df >> mutate(across(ends_with("mm"), lambda x: x.cast(pl.Float64, strict = False))) \
    >> select(ends_with("mm")) \
    >> head() \
    >> affiche()
```
```
╔════════════════╦═══════════════╦═══════════════════╗
║ bill_length_mm ║ bill_depth_mm ║ flipper_length_mm ║
║ float64        ║ float64       ║ float64           ║
╠════════════════╬═══════════════╬═══════════════════╣
║ 39.1           ║ 18.7          ║ 181.0             ║
║ 39.5           ║ 17.4          ║ 186.0             ║
║ 40.3           ║ 18.0          ║ 195.0             ║
║ null           ║ null          ║ null              ║
║ 36.7           ║ 19.3          ║ 193.0             ║
╚════════════════╩═══════════════╩═══════════════════╝
```

We also have access to the following helper functions within `where()`: `is_numeric`, `is_integer`, `is_float`, `is_string`, `is_boolean` and `is_temporal` 

```python
# Covert strings to uppercase
df >> mutate(across(where(is_string), lambda x: x.str.to_uppercase())) \
    >> select(where(is_string)) \
    >> select(~(_.bill_length_mm | _.body_mass_g)) \
    >> distinct() \
    >> head() \
    >> affiche()
```
```
╔═════════╦════════╦════════╗
║ species ║ island ║ sex    ║
║ str     ║ str    ║ str    ║
╠═════════╬════════╬════════╣
║ GENTOO  ║ BISCOE ║ NA     ║
║ GENTOO  ║ BISCOE ║ FEMALE ║
║ ADELIE  ║ BISCOE ║ FEMALE ║
║ ADELIE  ║ DREAM  ║ NA     ║
║ ADELIE  ║ BISCOE ║ MALE   ║
╚═════════╩════════╩════════╝
```

</details> 

#### 4. `group_by()` + `summarize()`

<details>
<summary>View examples</summary>

```python
df >> group_by(_.species) \
    >> summarize(count = _.species.count()) \
    >> affiche()
```

```
╔═══════════╦════════╗
║ species   ║ count  ║
║ str       ║ uint32 ║
╠═══════════╬════════╣
║ Chinstrap ║ 68     ║
║ Gentoo    ║ 124    ║
║ Adelie    ║ 152    ║
╚═══════════╩════════╝
```

</details> 


#### 5. `head()`

<details>
<summary>View examples</summary>

The default is 5 rows but can be specified:

```python
df >> head() \
    >> affiche()
```

```
╔═══════╦═════════╦═══════════╦════════════════╦═══════════════╦═══════════════════╦═════════════╦════════╦═══════╗
║ rowid ║ species ║ island    ║ bill_length_mm ║ bill_depth_mm ║ flipper_length_mm ║ body_mass_g ║ sex    ║ year  ║
║ int64 ║ str     ║ str       ║ str            ║ str           ║ str               ║ str         ║ str    ║ int64 ║
╠═══════╬═════════╬═══════════╬════════════════╬═══════════════╬═══════════════════╬═════════════╬════════╬═══════╣
║ 1     ║ Adelie  ║ Torgersen ║ 39.1           ║ 18.7          ║ 181               ║ 3750        ║ male   ║ 2007  ║
║ 2     ║ Adelie  ║ Torgersen ║ 39.5           ║ 17.4          ║ 186               ║ 3800        ║ female ║ 2007  ║
║ 3     ║ Adelie  ║ Torgersen ║ 40.3           ║ 18            ║ 195               ║ 3250        ║ female ║ 2007  ║
║ 4     ║ Adelie  ║ Torgersen ║ NA             ║ NA            ║ NA                ║ NA          ║ NA     ║ 2007  ║
║ 5     ║ Adelie  ║ Torgersen ║ 36.7           ║ 19.3          ║ 193               ║ 3450        ║ female ║ 2007  ║
╚═══════╩═════════╩═══════════╩════════════════╩═══════════════╩═══════════════════╩═════════════╩════════╩═══════╝
```

</details> 

#### 6. `tail()`

<details>
<summary>View examples</summary>

Similar to `head()`, default of 5 with an optional argument:

```python
# Tail also has a default of 5, but we'll provide 2 here
df >> tail(2) \
    >> affiche()
```

```
╔═══════╦═══════════╦════════╦════════════════╦═══════════════╦═══════════════════╦═════════════╦════════╦═══════╗
║ rowid ║ species   ║ island ║ bill_length_mm ║ bill_depth_mm ║ flipper_length_mm ║ body_mass_g ║ sex    ║ year  ║
║ int64 ║ str       ║ str    ║ str            ║ str           ║ str               ║ str         ║ str    ║ int64 ║
╠═══════╬═══════════╬════════╬════════════════╬═══════════════╬═══════════════════╬═════════════╬════════╬═══════╣
║ 343   ║ Chinstrap ║ Dream  ║ 50.8           ║ 19            ║ 210               ║ 4100        ║ male   ║ 2009  ║
║ 344   ║ Chinstrap ║ Dream  ║ 50.2           ║ 18.7          ║ 198               ║ 3775        ║ female ║ 2009  ║
╚═══════╩═══════════╩════════╩════════════════╩═══════════════╩═══════════════════╩═════════════╩════════╩═══════╝
```

</details> 

#### 7. `slice()`

<details>
<summary>View examples</summary>

With one argument, `slice()` accesses rows at that position — here, the last five rows (-5):

```python
df >> slice(-5) \
    >> select(_.rowid, _.island) \
    >> affiche()
```
```
╔═══════╦════════╗
║ rowid ║ island ║
║ int64 ║ str    ║
╠═══════╬════════╣
║ 340   ║ Dream  ║
║ 341   ║ Dream  ║
║ 342   ║ Dream  ║
║ 343   ║ Dream  ║
║ 344   ║ Dream  ║
╚═══════╩════════╝
```

But with two arguments, it grabs the starting position (9), followed by the number of rows (5):

```python
df >> slice(9, 5) \
    >> select(_.rowid, _.island) \
    >> affiche()
```
```
╔═══════╦═══════════╗
║ rowid ║ island    ║
║ int64 ║ str       ║
╠═══════╬═══════════╣
║ 10    ║ Torgersen ║
║ 11    ║ Torgersen ║
║ 12    ║ Torgersen ║
║ 13    ║ Torgersen ║
║ 14    ║ Torgersen ║
╚═══════╩═══════════╝
```

</details> 

#### 8. `distinct()`

<details>
<summary>View examples</summary>


The default behavior of `distinct()` is application to all columns, but can be specified: 

```python
df >> select(_.island, _.species) \
    >> distinct() \
    >> affiche()
```

```
╔═══════════╦═══════════╗
║ island    ║ species   ║
║ str       ║ str       ║
╠═══════════╬═══════════╣
║ Biscoe    ║ Adelie    ║
║ Torgersen ║ Adelie    ║
║ Biscoe    ║ Gentoo    ║
║ Dream     ║ Adelie    ║
║ Dream     ║ Chinstrap ║
╚═══════════╩═══════════╝
```

</details> 

#### 9. `arrange()`

<details>
<summary>View examples</summary>

By default, `arrange()` sorts ascending:

```python
df >> arrange(_.body_mass_g) \
    >> select(_.rowid, _.species, _.body_mass_g) \
    >> head() \
    >> affiche()
```
```
╔═══════╦═══════════╦═════════════╗
║ rowid ║ species   ║ body_mass_g ║
║ int64 ║ str       ║ str         ║
╠═══════╬═══════════╬═════════════╣
║ 315   ║ Chinstrap ║ 2700        ║
║ 59    ║ Adelie    ║ 2850        ║
║ 65    ║ Adelie    ║ 2850        ║
║ 55    ║ Adelie    ║ 2900        ║
║ 99    ║ Adelie    ║ 2900        ║
╚═══════╩═══════════╩═════════════╝
```

But we can use the `-` operator to sort descending:

```python
df >> filter(_.body_mass_g != "NA") \
    >> arrange(-_.body_mass_g) \
    >> select(_.rowid, _.species, _.body_mass_g) \
    >> head() \
    >> affiche()
```
```
╔═══════╦═════════╦═════════════╗
║ rowid ║ species ║ body_mass_g ║
║ int64 ║ str     ║ str         ║
╠═══════╬═════════╬═════════════╣
║ 170   ║ Gentoo  ║ 6300        ║
║ 186   ║ Gentoo  ║ 6050        ║
║ 230   ║ Gentoo  ║ 6000        ║
║ 270   ║ Gentoo  ║ 6000        ║
║ 232   ║ Gentoo  ║ 5950        ║
╚═══════╩═════════╩═════════════╝
```

</details> 

#### 10. `relocate()`

<details>
<summary>View examples</summary>

Like `mutate()`, we have optional `after` and `before` arguments:

```python
df >> relocate(_.sex, after = _.rowid) \
    >> head() \
    >> affiche()
```

```
╔═══════╦════════╦═════════╦═══════════╦════════════════╦═══════════════╦═══════════════════╦═════════════╦═══════╗
║ rowid ║ sex    ║ species ║ island    ║ bill_length_mm ║ bill_depth_mm ║ flipper_length_mm ║ body_mass_g ║ year  ║
║ int64 ║ str    ║ str     ║ str       ║ str            ║ str           ║ str               ║ str         ║ int64 ║
╠═══════╬════════╬═════════╬═══════════╬════════════════╬═══════════════╬═══════════════════╬═════════════╬═══════╣
║ 1     ║ male   ║ Adelie  ║ Torgersen ║ 39.1           ║ 18.7          ║ 181               ║ 3750        ║ 2007  ║
║ 2     ║ female ║ Adelie  ║ Torgersen ║ 39.5           ║ 17.4          ║ 186               ║ 3800        ║ 2007  ║
║ 3     ║ female ║ Adelie  ║ Torgersen ║ 40.3           ║ 18            ║ 195               ║ 3250        ║ 2007  ║
║ 4     ║ NA     ║ Adelie  ║ Torgersen ║ NA             ║ NA            ║ NA                ║ NA          ║ 2007  ║
║ 5     ║ female ║ Adelie  ║ Torgersen ║ 36.7           ║ 19.3          ║ 193               ║ 3450        ║ 2007  ║
╚═══════╩════════╩═════════╩═══════════╩════════════════╩═══════════════╩═══════════════════╩═════════════╩═══════╝
```

</details> 

#### 11. `rename()`

<details>
<summary>View examples</summary>

Like siuba, `rename()` expects `new_name = _.old_name`


```python
df >> rename(row_id = _.rowid, 
             gender = _.sex) \
    >> select(_.row_id, _.gender) \
    >> head() \
    >> affiche()
```

```
╔════════╦════════╗
║ row_id ║ gender ║
║ int64  ║ str    ║
╠════════╬════════╣
║ 1      ║ male   ║
║ 2      ║ female ║
║ 3      ║ female ║
║ 4      ║ NA     ║
║ 5      ║ female ║
╚════════╩════════╝
```

</details> 

#### 12. `round()`

<details>
<summary>View examples</summary>

By default, `round()` will round all numeric columns to two decimals:

```python
int_cols = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]

df >> mutate(across(int_cols, lambda x: x.cast(pl.Float64, strict = False))) \
    >> _.describe() \
    >> select(_.statistic, *int_cols) \
    >> round() \
    >> affiche()
```
```
╔════════════╦════════════════╦═══════════════╦═══════════════════╦═════════════╗
║ statistic  ║ bill_length_mm ║ bill_depth_mm ║ flipper_length_mm ║ body_mass_g ║
║ str        ║ float64        ║ float64       ║ float64           ║ float64     ║
╠════════════╬════════════════╬═══════════════╬═══════════════════╬═════════════╣
║ count      ║ 342.0          ║ 342.0         ║ 342.0             ║ 342.0       ║
║ null_count ║ 2.0            ║ 2.0           ║ 2.0               ║ 2.0         ║
║ mean       ║ 43.92          ║ 17.15         ║ 200.92            ║ 4201.75     ║
║ std        ║ 5.46           ║ 1.97          ║ 14.06             ║ 801.95      ║
║ min        ║ 32.1           ║ 13.1          ║ 172.0             ║ 2700.0      ║
║ 25%        ║ 39.2           ║ 15.6          ║ 190.0             ║ 3550.0      ║
║ 50%        ║ 44.5           ║ 17.3          ║ 197.0             ║ 4050.0      ║
║ 75%        ║ 48.5           ║ 18.7          ║ 213.0             ║ 4750.0      ║
║ max        ║ 59.6           ║ 21.5          ║ 231.0             ║ 6300.0      ║
╚════════════╩════════════════╩═══════════════╩═══════════════════╩═════════════╝
```

But we can also specify columns, and to how many decimals:

```python
int_cols = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]

# Here, we use the unpacking operator * to unpack the list, filtered with a range
df >> mutate(across(int_cols, lambda x: x.cast(pl.Float64, strict = False))) \
    >> _.describe() \
    >> select(_.statistic, *int_cols) \
    >> round(_.body_mass_g, decimals = 5) \
    >> round(*int_cols[0:3], decimals = 0) \
    >> affiche()
```
```
╔════════════╦════════════════╦═══════════════╦═══════════════════╦═════════════╗
║ statistic  ║ bill_length_mm ║ bill_depth_mm ║ flipper_length_mm ║ body_mass_g ║
║ str        ║ float64        ║ float64       ║ float64           ║ float64     ║
╠════════════╬════════════════╬═══════════════╬═══════════════════╬═════════════╣
║ count      ║ 342.0          ║ 342.0         ║ 342.0             ║ 342.0       ║
║ null_count ║ 2.0            ║ 2.0           ║ 2.0               ║ 2.0         ║
║ mean       ║ 44.0           ║ 17.0          ║ 201.0             ║ 4201.75439  ║
║ std        ║ 5.0            ║ 2.0           ║ 14.0              ║ 801.95454   ║
║ min        ║ 32.0           ║ 13.0          ║ 172.0             ║ 2700.0      ║
║ 25%        ║ 39.0           ║ 16.0          ║ 190.0             ║ 3550.0      ║
║ 50%        ║ 44.0           ║ 17.0          ║ 197.0             ║ 4050.0      ║
║ 75%        ║ 48.0           ║ 19.0          ║ 213.0             ║ 4750.0      ║
║ max        ║ 60.0           ║ 22.0          ║ 231.0             ║ 6300.0      ║
╚════════════╩════════════════╩═══════════════╩═══════════════════╩═════════════╝
```

</details> 

## Dependencies
Penguins really just relies on polars for doing all of its data manipulation.

## Notes
Palmer penguin data from [palmerpenguins](https://github.com/allisonhorst/palmerpenguins) R package