# Changelog

All notable changes to `penguins` will be documented in this changelog

## *0.3.4* — 2025-11-10

### Improvements
- `select()`, `mutate()` and `round()` use the more efficient `collect_schema()` for retrieving column names for LazyFrames

### Fixes
- The following functions now play nice with LazyFrames (I knew there'd be bugs):
  - `pasteurize()` 
  - `pull()` 
  - `separate()` 
  - `bind_cols()` 
  - `bind_rows()

## *0.3.3* — 2025-11-09

### Features
- Added compatibly for working with LazyFrames (some bugs to be expected)

## *0.3.2* — 2025-11-08

### Fixes
- Fixed regex search for `starts_with()` and `contains()` helpers

## *0.3.1* — 2025-11-07

### Features
- Adds verb `reframe()` for creating new summary rows based on group summaries

### Improvements
- Helper functions — `starts_with()`, `ends_with()`, and `contains()` — now allow for matching on multiple expressions with the OR operator `|`
    - e.g. df >> select(starts_with("a|b"))
- `affiche()` now handles datetime data type abbreviations

## *0.3.0* — 2025-11-06

### Features
- Dataframes now have the `count_null()` method for counting `null` values by column
- Conditional row assignment with `if_else()` and `case_when()` is now supported in `mutate()` statements
- New verb functions:
  - `drop_null()` — remove rows with `null` values
  - `pull()` — extract a single column as a series or scalar value
  - `sample()` — return a sample of rows from a dataframe 
  - `join()` — join two dataframes on a matching column  
    - Type: "inner", "left", "right", "outer", "cross", "semi", "anti"
  - `pivot_wider()` — pivot a dataframe from long to wide format 
  - `pivot_longer()` — pivot a dataframe from wide to long format 
  - `unite()` — combine multiple columns into one column
  - `separate()` — split a column into multiple columns
  - `bind_cols()` — bind the columns of two dataframes together
  - `bind_rows()` — bind the rows of two dataframes together

### Improvements
- `mutate()` now allows for arithmetic operators (e.g. `+`, `*`, `/`) to be used across columns
- `where()` now allows for the `is_null` and `is_cat` [for the categorical data type] parameters
- `filter()` now has a helper function `row_contains()` for checking which rows in any columns contain given value[s]
- Re-organized helper functions into their own module for cleaner imports

## *0.2.1* — 2025-11-04

### Improvements
- `affiche()` now provides column data types

## *0.2.0* — 2025-11-03

### Features
- **Enhanced `select()` capabilities:**
  - Column ranges using `|` operator
  - Column exclusion using `~` operator  
  - `starts_with()`, `ends_with()`, and `contains()` helpers
  - `where()` for conditional column selection
- **`mutate()` with `across()` support:**
  - Apply operations across multiple columns
  - Works with `where()` for column selection in conjunction with selection helpers (`starts_with()`, `ends_with()`, `contains()`)
  - `where()` also includes checks for `is_numeric()`, `is_integer()`, `is_float()`, `is_string()`, `is_boolean()` and `is_temporal()` 
  - And allow use of inverse operator `~` on selection helpers
- Added changelog file

### Improvements
- Missing values now display as `null` instead of `NA`
- Expanded README with more examples and usage

## *0.1.0* — 2025-11-02

Initial package release

### Features
- Acutis methods: `affiche()`, `count_table()`, `pasteurize()`, `not_in`(), `not_like()`
- Core verbs: `select()`, `filter()`, `mutate()`, `group_by()`, `summarize()`, `head()`, `tail()`, `slice()`, `distinct()`, `arrange()`, `relocate()`, `rename()`, `round()`
- Penguin dataset included

### Improvements
- Special before/after handling for `mutate()`
- Decimals argument for `round()`

## **_Unreleased_**

### Features
- **Methods:** ~~`count_null()`~~
- **New verbs:** ~~`if_else()`~~, ~~`case_when()`~~, ~~`join()`~~, ~~`pivot_longer()`~~, ~~`pivot_wider()`~~, ~~`sample()`~~, ~~`pull()`~~
- **Data cleaning:** ~~`drop_null()`~~
- **Reshaping:** ~~`unite()`~~, ~~`separate()`~~, ~~`bind_rows()`~~, ~~`bind_cols()`~~

### Improvements
- **Additional handling:** ~~`is_categorical()`~~, ~~`is_null()`~~, ~~`row_contains()`~~