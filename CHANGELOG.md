# Changelog

All notable changes to `penguins` will be documented in this changelog

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
- **Methods:** `count_na()`
- **New verbs:** `if_else()`, `case_when()`, `*_join()`, `pivot_longer()`, `pivot_wider()`, `sample()`, `pull()`
- **Data cleaning:** `drop_na()`, `fill_na()`, `coalesce_by()`
- **Reshaping:** `unite()`, `separate()`, `bind_rows()`, `bind_cols()`

### Improvements
- **Additional handling:** `is_categorical()`, `is_null()`, `col_contains()`