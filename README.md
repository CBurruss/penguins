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

If we look at the penguins package, we can group its utilities into three main categories — core functionality, acutis methods, and verb functions. 

### Core functionality

At its core, penguins provides a dplyr-flavored  interface for polars through two main features:

 - The pipe operator `>>` — enables function function chaining akin to R's `|>` pipe
 - The symbolic placeholder `_` — acts as a helper by standing in for two main use cases:
      1. DataFrame references in method calls — e.g. `df >> _.head(5)`
      2. Column references in verb expressions — e.g. `df >> select(_.col)`

### Acutis methods

Unlike its more principled pandas counterpart (siuba), penguins takes the [careless] liberty of extending polars objects with both implicit and explicit methods! Each of these were ported from my [acutis](https://github.com/CBurruss/acutis) R package and provide handy functionality for typical data processsing and handling. 

**Explicit import required:**
 - `affiche()` — display a Polars DataFrame with aethetic table borders and styling (from the French *affiche* to display something)
     - As a bonus, this is also provided as a function! 
 - `count_table()` — create a frequency table with counts and percentages
 - `pasteurize()` — clean a DataFrame by removing empty rows, duplicates, and standardizing column names

**Implicilty patched in:**  
 - `not_in()` — perform the inverse of the `is_in()` method
 - `not_like()` — perform the inverse of the `str.contains()` method

### Verb functions

As hinted at above, penguins gains most of its utility from its dplyr-styled functions. While they'll be covered in the [Examples](#examples) section, here are the functions that have currently been ported over:
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
╔═══════╦═════════╦═══════════╦════════════════╦═══════════════╦═══════════════════╦═════════════╦════════╦══════╗
║ rowid ║ species ║ island    ║ bill_length_mm ║ bill_depth_mm ║ flipper_length_mm ║ body_mass_g ║ sex    ║ year ║
╠═══════╬═════════╬═══════════╬════════════════╬═══════════════╬═══════════════════╬═════════════╬════════╬══════╣
║ 1     ║ Adelie  ║ Torgersen ║ 39.1           ║ 18.7          ║ 181               ║ 3750        ║ male   ║ 2007 ║
║ 2     ║ Adelie  ║ Torgersen ║ 39.5           ║ 17.4          ║ 186               ║ 3800        ║ female ║ 2007 ║
║ 3     ║ Adelie  ║ Torgersen ║ 40.3           ║ 18            ║ 195               ║ 3250        ║ female ║ 2007 ║
║ 4     ║ Adelie  ║ Torgersen ║ NA             ║ NA            ║ NA                ║ NA          ║ NA     ║ 2007 ║
║ 5     ║ Adelie  ║ Torgersen ║ 36.7           ║ 19.3          ║ 193               ║ 3450        ║ female ║ 2007 ║
╚═══════╩═════════╩═══════════╩════════════════╩═══════════════╩═══════════════════╩═════════════╩════════╩══════╝
```
</details> 

#### 2. `count_table()`

<details>
<summary>View examples</summary>

```python
df["island"].count_table().affiche()
```

```
╔═══════════╦═══════╦═════════╗
║ island    ║ count ║ percent ║
╠═══════════╬═══════╬═════════╣
║ Biscoe    ║ 168   ║ 49%     ║
║ Dream     ║ 124   ║ 36%     ║
║ Torgersen ║ 52    ║ 15%     ║
╚═══════════╩═══════╩═════════╝
```
</details> 

#### 3. `pasteurize()`

<details>
<summary>View examples</summary>

```python
print("Without pasteurize():")
df["sex"].count_table().affiche()

print("With pasteurize():")
df.pasteurize()["sex"].count_table().affiche()
```

```
Without pasteurize():
╔════════╦═══════╦═════════╗
║ sex    ║ count ║ percent ║
╠════════╬═══════╬═════════╣
║ male   ║ 168   ║ 49%     ║
║ female ║ 165   ║ 48%     ║
║ NA     ║ 11    ║ 3%      ║
╚════════╩═══════╩═════════╝
With pasteurize():
╔════════╦═══════╦═════════╗
║ sex    ║ count ║ percent ║
╠════════╬═══════╬═════════╣
║ Male   ║ 168   ║ 49%     ║
║ Female ║ 165   ║ 48%     ║
║ null   ║ 11    ║ 3%      ║
╚════════╩═══════╩═════════╝
# Note how the "NA" character string was converted to a true missing value
# and now displays as `null`
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
╔═══════╦═══════════╦════════╦════════════════╦═══════════════╦═══════════════════╦═════════════╦════════╦══════╗
║ rowid ║ species   ║ island ║ bill_length_mm ║ bill_depth_mm ║ flipper_length_mm ║ body_mass_g ║ sex    ║ year ║
╠═══════╬═══════════╬════════╬════════════════╬═══════════════╬═══════════════════╬═════════════╬════════╬══════╣
║ 339   ║ Chinstrap ║ Dream  ║ 45.7           ║ 17            ║ 195               ║ 3650        ║ female ║ 2009 ║
║ 340   ║ Chinstrap ║ Dream  ║ 55.8           ║ 19.8          ║ 207               ║ 4000        ║ male   ║ 2009 ║
║ 341   ║ Chinstrap ║ Dream  ║ 43.5           ║ 18.1          ║ 202               ║ 3400        ║ female ║ 2009 ║
║ 342   ║ Chinstrap ║ Dream  ║ 49.6           ║ 18.2          ║ 193               ║ 3775        ║ male   ║ 2009 ║
║ 343   ║ Chinstrap ║ Dream  ║ 50.8           ║ 19            ║ 210               ║ 4100        ║ male   ║ 2009 ║
║ 344   ║ Chinstrap ║ Dream  ║ 50.2           ║ 18.7          ║ 198               ║ 3775        ║ female ║ 2009 ║
╚═══════╩═══════════╩════════╩════════════════╩═══════════════╩═══════════════════╩═════════════╩════════╩══════╝
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
╔═══════╦═════════╦═══════════╦════════════════╦═══════════════╦═══════════════════╦═════════════╦════════╦══════╗
║ rowid ║ species ║ island    ║ bill_length_mm ║ bill_depth_mm ║ flipper_length_mm ║ body_mass_g ║ sex    ║ year ║
╠═══════╬═════════╬═══════════╬════════════════╬═══════════════╬═══════════════════╬═════════════╬════════╬══════╣
║ 1     ║ Adelie  ║ Torgersen ║ 39.1           ║ 18.7          ║ 181               ║ 3750        ║ male   ║ 2007 ║
║ 2     ║ Adelie  ║ Torgersen ║ 39.5           ║ 17.4          ║ 186               ║ 3800        ║ female ║ 2007 ║
║ 3     ║ Adelie  ║ Torgersen ║ 40.3           ║ 18            ║ 195               ║ 3250        ║ female ║ 2007 ║
║ 4     ║ Adelie  ║ Torgersen ║ NA             ║ NA            ║ NA                ║ NA          ║ NA     ║ 2007 ║
║ 5     ║ Adelie  ║ Torgersen ║ 36.7           ║ 19.3          ║ 193               ║ 3450        ║ female ║ 2007 ║
╚═══════╩═════════╩═══════════╩════════════════╩═══════════════╩═══════════════════╩═════════════╩════════╩══════╝
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
╔═════════╦════════╦══════╗
║ species ║ sex    ║ year ║
╠═════════╬════════╬══════╣
║ Adelie  ║ male   ║ 2007 ║
║ Adelie  ║ female ║ 2007 ║
║ Adelie  ║ female ║ 2007 ║
║ Adelie  ║ NA     ║ 2007 ║
║ Adelie  ║ female ║ 2007 ║
╚═════════╩════════╩══════╝
```

We can also use the inverse operator `~` for de-selecting columns:

```python
df >> select(~_.species, ~_.island, ~_.body_mass_g, ~_.sex) \
    >> head() \
    >> affiche()
```
```
╔═══════╦════════════════╦═══════════════╦═══════════════════╦══════╗
║ rowid ║ bill_length_mm ║ bill_depth_mm ║ flipper_length_mm ║ year ║
╠═══════╬════════════════╬═══════════════╬═══════════════════╬══════╣
║ 1     ║ 39.1           ║ 18.7          ║ 181               ║ 2007 ║
║ 2     ║ 39.5           ║ 17.4          ║ 186               ║ 2007 ║
║ 3     ║ 40.3           ║ 18            ║ 195               ║ 2007 ║
║ 4     ║ NA             ║ NA            ║ NA                ║ 2007 ║
║ 5     ║ 36.7           ║ 19.3          ║ 193               ║ 2007 ║
╚═══════╩════════════════╩═══════════════╩═══════════════════╩══════╝
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
╔═════════╦════════╦══════╗
║ species ║ sex    ║ year ║
╠═════════╬════════╬══════╣
║ Adelie  ║ male   ║ 2007 ║
║ Adelie  ║ female ║ 2007 ║
║ Adelie  ║ female ║ 2007 ║
║ Adelie  ║ NA     ║ 2007 ║
║ Adelie  ║ female ║ 2007 ║
╚═════════╩════════╩══════╝
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
╔═════════╦═══════════╦════════╦══════╗
║ species ║ island    ║ sex    ║ year ║
╠═════════╬═══════════╬════════╬══════╣
║ Adelie  ║ Torgersen ║ male   ║ 2007 ║
║ Adelie  ║ Torgersen ║ female ║ 2007 ║
║ Adelie  ║ Torgersen ║ female ║ 2007 ║
║ Adelie  ║ Torgersen ║ NA     ║ 2007 ║
║ Adelie  ║ Torgersen ║ female ║ 2007 ║
╚═════════╩═══════════╩════════╩══════╝
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
╔═══════╦══════╦══════╗
║ rowid ║ sex  ║ year ║
╠═══════╬══════╬══════╣
║ 52    ║ male ║ 2008 ║
║ 54    ║ male ║ 2008 ║
║ 56    ║ male ║ 2008 ║
║ 58    ║ male ║ 2008 ║
║ 60    ║ male ║ 2008 ║
╚═══════╩══════╩══════╝
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
# We'll use print() since it tells us our data types
df >> mutate(across(ends_with("mm"), lambda x: x.cast(pl.Float64, strict = False))) \
    >> select(ends_with("mm")) \
    >> print
```
```
┌────────────────┬───────────────┬───────────────────┐
│ bill_length_mm ┆ bill_depth_mm ┆ flipper_length_mm │
│ ---            ┆ ---           ┆ ---               │
│ f64            ┆ f64           ┆ f64               │
╞════════════════╪═══════════════╪═══════════════════╡
│ 39.1           ┆ 18.7          ┆ 181.0             │
│ 39.5           ┆ 17.4          ┆ 186.0             │
│ 40.3           ┆ 18.0          ┆ 195.0             │
│ null           ┆ null          ┆ null              │
│ 36.7           ┆ 19.3          ┆ 193.0             │
└────────────────┴───────────────┴───────────────────┘
```

We also have access to the following helper functions within `where()`: `is_numeric()`, `is_integer()`, `is_float()`, `is_string()`, `is_boolean()` and `is_temporal()` 

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
╔═══════════╦═══════════╦════════╗
║ species   ║ island    ║ sex    ║
╠═══════════╬═══════════╬════════╣
║ ADELIE    ║ DREAM     ║ NA     ║
║ CHINSTRAP ║ DREAM     ║ MALE   ║
║ ADELIE    ║ BISCOE    ║ FEMALE ║
║ ADELIE    ║ TORGERSEN ║ NA     ║
║ ADELIE    ║ TORGERSEN ║ MALE   ║
╚═══════════╩═══════════╩════════╝
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
╔═══════════╦═══════╗
║ species   ║ count ║
╠═══════════╬═══════╣
║ Adelie    ║ 152   ║
║ Chinstrap ║ 68    ║
║ Gentoo    ║ 124   ║
╚═══════════╩═══════╝
```

</details> 


#### 5. `head()`

<details>
<summary>View examples</summary>

```python
# Where the default is 5 rows but can be specified
df >> head() >> affiche()
```

```
╔═══════╦═════════╦═══════════╦════════════════╦═══════════════╦═══════════════════╦═════════════╦════════╦══════╗
║ rowid ║ species ║ island    ║ bill_length_mm ║ bill_depth_mm ║ flipper_length_mm ║ body_mass_g ║ sex    ║ year ║
╠═══════╬═════════╬═══════════╬════════════════╬═══════════════╬═══════════════════╬═════════════╬════════╬══════╣
║ 1     ║ Adelie  ║ Torgersen ║ 39.1           ║ 18.7          ║ 181               ║ 3750        ║ male   ║ 2007 ║
║ 2     ║ Adelie  ║ Torgersen ║ 39.5           ║ 17.4          ║ 186               ║ 3800        ║ female ║ 2007 ║
║ 3     ║ Adelie  ║ Torgersen ║ 40.3           ║ 18            ║ 195               ║ 3250        ║ female ║ 2007 ║
║ 4     ║ Adelie  ║ Torgersen ║ NA             ║ NA            ║ NA                ║ NA          ║ NA     ║ 2007 ║
║ 5     ║ Adelie  ║ Torgersen ║ 36.7           ║ 19.3          ║ 193               ║ 3450        ║ female ║ 2007 ║
╚═══════╩═════════╩═══════════╩════════════════╩═══════════════╩═══════════════════╩═════════════╩════════╩══════╝
```

</details> 

#### 6. `tail()`

<details>
<summary>View examples</summary>

```python
# Tail also has a default of 5, but we'll provide 2 here
df >> tail(2) >> affiche()
```

```
╔═══════╦═══════════╦════════╦════════════════╦═══════════════╦═══════════════════╦═════════════╦════════╦══════╗
║ rowid ║ species   ║ island ║ bill_length_mm ║ bill_depth_mm ║ flipper_length_mm ║ body_mass_g ║ sex    ║ year ║
╠═══════╬═══════════╬════════╬════════════════╬═══════════════╬═══════════════════╬═════════════╬════════╬══════╣
║ 343   ║ Chinstrap ║ Dream  ║ 50.8           ║ 19            ║ 210               ║ 4100        ║ male   ║ 2009 ║
║ 344   ║ Chinstrap ║ Dream  ║ 50.2           ║ 18.7          ║ 198               ║ 3775        ║ female ║ 2009 ║
╚═══════╩═══════════╩════════╩════════════════╩═══════════════╩═══════════════════╩═════════════╩════════╩══════╝
```

</details> 

#### 7. `slice()`

<details>
<summary>View examples</summary>

```python
# With one argument, slice() accesses rows at that position
# Here, the last five rows (-5)
df >> slice(-5) \
    >> select(_.rowid, _.island) \
    >> affiche()
```
```
╔═══════╦════════╗
║ rowid ║ island ║
╠═══════╬════════╣
║ 340   ║ Dream  ║
║ 341   ║ Dream  ║
║ 342   ║ Dream  ║
║ 343   ║ Dream  ║
║ 344   ║ Dream  ║
╚═══════╩════════╝
```

```python
# But with two arguments, it grabs the starting position (100),
# followed by the number of rows (5)
df >> slice(9, 5) \
    >> select(_.rowid, _.island) \
    >> affiche()
```
```
╔═══════╦═══════════╗
║ rowid ║ island    ║
╠═══════╬═══════════╣
║ 11    ║ Torgersen ║
║ 12    ║ Torgersen ║
║ 13    ║ Torgersen ║
║ 14    ║ Torgersen ║
║ 15    ║ Torgersen ║
╚═══════╩═══════════╝
```

</details> 

#### 8. `distinct()`

<details>
<summary>View examples</summary>

```python
# Default behavior is to pull distinct() on all columns 
df >> select(_.island, _.species) \
    >> distinct() \
    >> affiche()
```

```
╔═══════════╦═══════════╗
║ island    ║ species   ║
╠═══════════╬═══════════╣
║ Dream     ║ Adelie    ║
║ Biscoe    ║ Gentoo    ║
║ Biscoe    ║ Adelie    ║
║ Dream     ║ Chinstrap ║
║ Torgersen ║ Adelie    ║
╚═══════════╩═══════════╝
```

</details> 

#### 9. `arrange()`

<details>
<summary>View examples</summary>

```python
# By default, arrange() sorts ascending
df >> arrange(_.body_mass_g) \
    >> select(_.rowid, _.species, _.body_mass_g) \
    >> head() \
    >> affiche()
```
```
╔═══════╦═══════════╦═════════════╗
║ rowid ║ species   ║ body_mass_g ║
╠═══════╬═══════════╬═════════════╣
║ 315   ║ Chinstrap ║ 2700        ║
║ 59    ║ Adelie    ║ 2850        ║
║ 65    ║ Adelie    ║ 2850        ║
║ 55    ║ Adelie    ║ 2900        ║
║ 99    ║ Adelie    ║ 2900        ║
╚═══════╩═══════════╩═════════════╝
```

```python
# But we can use the - to sort descending
df >> filter(_.body_mass_g != "NA") \
    >> arrange(-_.body_mass_g) \
    >> select(_.rowid, _.species, _.body_mass_g) \
    >> head() \
    >> affiche()
```
```
╔═══════╦═════════╦═════════════╗
║ rowid ║ species ║ body_mass_g ║
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

```python
# Like mutate(), we have optional `after` and `before` arguments
df >> relocate(_.sex, after = _.rowid) \
    >> head() \
    >> affiche()
```

```
╔═══════╦════════╦═════════╦═══════════╦════════════════╦═══════════════╦═══════════════════╦═════════════╦══════╗
║ rowid ║ sex    ║ species ║ island    ║ bill_length_mm ║ bill_depth_mm ║ flipper_length_mm ║ body_mass_g ║ year ║
╠═══════╬════════╬═════════╬═══════════╬════════════════╬═══════════════╬═══════════════════╬═════════════╬══════╣
║ 1     ║ male   ║ Adelie  ║ Torgersen ║ 39.1           ║ 18.7          ║ 181               ║ 3750        ║ 2007 ║
║ 2     ║ female ║ Adelie  ║ Torgersen ║ 39.5           ║ 17.4          ║ 186               ║ 3800        ║ 2007 ║
║ 3     ║ female ║ Adelie  ║ Torgersen ║ 40.3           ║ 18            ║ 195               ║ 3250        ║ 2007 ║
║ 4     ║ NA     ║ Adelie  ║ Torgersen ║ NA             ║ NA            ║ NA                ║ NA          ║ 2007 ║
║ 5     ║ female ║ Adelie  ║ Torgersen ║ 36.7           ║ 19.3          ║ 193               ║ 3450        ║ 2007 ║
╚═══════╩════════╩═════════╩═══════════╩════════════════╩═══════════════╩═══════════════════╩═════════════╩══════╝
```

</details> 

#### 11. `rename()`

<details>
<summary>View examples</summary>

```python
# Where rename() expects `new_name = _.old_name`
df >> rename(row_id = _.rowid, 
             gender = _.sex) \
    >> select(_.row_id, _.gender) \
    >> head() \
    >> affiche()
```

```
╔════════╦════════╗
║ row_id ║ gender ║
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

```python
# By default, round() will round all numeric columns to two decimals
df >> mutate(bill_length_mm = _.bill_length_mm.cast(pl.Float64, strict = False),
              bill_depth_mm = _.bill_depth_mm.cast(pl.Float64, strict = False),
              flipper_length_mm = _.flipper_length_mm.cast(pl.Float64, strict = False)) \
    >> _.describe() \
    >> select(_.statistic, _.bill_length_mm, _.bill_depth_mm, _.flipper_length_mm) \
    >> round() \
    >> affiche()
```

```
╔════════════╦════════════════╦═══════════════╦═══════════════════╗
║ statistic  ║ bill_length_mm ║ bill_depth_mm ║ flipper_length_mm ║
╠════════════╬════════════════╬═══════════════╬═══════════════════╣
║ count      ║ 342.0          ║ 342.0         ║ 342.0             ║
║ null_count ║ 2.0            ║ 2.0           ║ 2.0               ║
║ mean       ║ 43.92          ║ 17.15         ║ 200.92            ║
║ std        ║ 5.46           ║ 1.97          ║ 14.06             ║
║ min        ║ 32.1           ║ 13.1          ║ 172.0             ║
║ 25%        ║ 39.2           ║ 15.6          ║ 190.0             ║
║ 50%        ║ 44.5           ║ 17.3          ║ 197.0             ║
║ 75%        ║ 48.5           ║ 18.7          ║ 213.0             ║
║ max        ║ 59.6           ║ 21.5          ║ 231.0             ║
╚════════════╩════════════════╩═══════════════╩═══════════════════╝
```

```python
# But we can also specify columns, and to what decimals
df >> mutate(bill_length_mm = _.bill_length_mm.cast(pl.Float64, strict = False),
              bill_depth_mm = _.bill_depth_mm.cast(pl.Float64, strict = False),
              flipper_length_mm = _.flipper_length_mm.cast(pl.Float64, strict = False)) \
    >> _.describe() \
    >> select(_.statistic, _.bill_length_mm, _.bill_depth_mm, _.flipper_length_mm) \
    >> round(_.bill_length_mm, decimals = 5) \
    >> round(_.bill_depth_mm, _.flipper_length_mm, decimals = 0) \
    >> affiche()
```
```
╔════════════╦════════════════╦═══════════════╦═══════════════════╗
║ statistic  ║ bill_length_mm ║ bill_depth_mm ║ flipper_length_mm ║
╠════════════╬════════════════╬═══════════════╬═══════════════════╣
║ count      ║ 342.0          ║ 342.0         ║ 342.0             ║
║ null_count ║ 2.0            ║ 2.0           ║ 2.0               ║
║ mean       ║ 43.92193       ║ 17.0          ║ 201.0             ║
║ std        ║ 5.45958        ║ 2.0           ║ 14.0              ║
║ min        ║ 32.1           ║ 13.0          ║ 172.0             ║
║ 25%        ║ 39.2           ║ 16.0          ║ 190.0             ║
║ 50%        ║ 44.5           ║ 17.0          ║ 197.0             ║
║ 75%        ║ 48.5           ║ 19.0          ║ 213.0             ║
║ max        ║ 59.6           ║ 22.0          ║ 231.0             ║
╚════════════╩════════════════╩═══════════════╩═══════════════════╝
```

</details> 

## Dependencies
Penguins really just relies on polars for doing all of its data manipulation.

## Notes
Palmer penguin data from [palmerpenguins](https://github.com/allisonhorst/palmerpenguins) R package