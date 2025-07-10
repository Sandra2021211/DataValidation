# Data Validation Pipeline

## Features

* Supports **three validation modes**:

  1. **Full Dataset Validation**
  2. **Custom (Corrupted Window) Validation**
  3. **Automated Column Mapping** (No `mapping.json` required)

* Smart column matching using:

  * **Position-based matching**
  * **Value equality matching**
  * **Fuzzy string similarity** (via `SequenceMatcher`)

* Row-level comparison using **multiprocessing** for improved performance to find any mismatch

* Validates:

  * Column mappings
  * Row counts
  * Data types
  * Duplicate entries
  * Empty rows

---

## 📁 Module Descriptions

### `main_driver.py`

*Pipeline Controller*

* CLI for selecting validation mode
* Loads YAML config dynamically
* Coordinates all steps of validation and comparison

---

### `file_read.py`

*File Reading & Column Validation*

* `FileReader`: Reads `.csv`, `.json`, `.yaml` formats
* Handles file not found, decoding errors
* `ColumnValidator`: Checks all destination columns have valid mappings

---

### `basic_properties.py`

*Basic Dataset Checks*

* `BasicPropertiesValidator` handles:

  * Row count mismatch
  * Data type mismatches
  * Duplicate rows
  * Entirely empty rows

---

### `row_by_row_comparison.py`

*Row-by-Row Validation*

* `RowByRowComparator`: Validates data row-wise using the primary key
* Uses **Python multiprocessing** for faster validation
* Clearly logs mismatches between source and destination rows

---

### `full_validator.py`

*Full Dataset Validation*

* Validates the entire source and destination dataset
* Applies:

  * Column validation
  * Basic property checks (row count, duplicates, data types)
  * Full row-by-row comparison
* Used when validating the **entire dataset** without time window constraints

---

### `custom_validator.py`

*Custom Window-Based Validation*

* Filters source and destination data based on a **custom time window** (from YAML config)
* Applies all validations only within the filtered window:

  * Column validation
  * Basic checks
  * Row-by-row comparison
* Useful when validating **only corrupted or recent slices** of the data

---

### `unmapped_columns/without_column_mapper.py`

*Automated Column Mapping (No Mapping File Required)*

* Matches columns using:

  * `match_by_position()`: Direct index-based comparison
  * `match_by_value()`: Column-wise value matching
  * `match_by_word_similarity()`: Fuzzy matching with `SequenceMatcher`
* Infers and builds column mappings when they’re not explicitly provided

---

### `mapped_columns/` & `unmapped_columns/`

*Project Structure Organization*

* Sub-packages that separate logic for:

  * Mapped column validation
  * Unmapped (automatically detected) column validation
* `__init__.py` makes them importable Python packages
