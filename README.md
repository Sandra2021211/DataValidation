# Data Validation Pipeline

A polished data validation portfolio project for healthcare claims comparison.
It demonstrates dataset mapping, row-level validation, time-window filtering, and automated schema matching.

## Why this project

This repo is a strong interview asset for data engineering, analytics, or data quality roles because it:

* validates dataset integrity through end-to-end comparison
* supports both mapped and unmapped column workflows
* includes configuration-driven behavior via JSON and YAML
* surfaces mismatches clearly with row-by-row diagnostics

## Key Features

* Full dataset validation using explicit column mappings
* Custom time-window validation for corrupted or recent data slices
* Automatic column inference when mapping metadata is unavailable
* Basic dataset checks: row count, duplicate records, empty rows, and data type comparison
* Row-by-row comparison using multiprocessing for scalability

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run the interactive pipeline controller:

```bash
python validation/main_driver.py
```

Then choose one of the modes:

1. Full Dataset Validation
2. Custom Dataset Validation
3. Without Column Mapping

### Full Dataset Validation

Validates the complete source and destination datasets using `src_data/mapping.json`.

Example:

```bash
python validation/main_driver.py
# choose 1
```

### Custom Dataset Validation

Filters the source and destination datasets by stream time using `src_data/requirements.yaml`.
Use this when you want to validate a specific corrupted time window.

Example:

```bash
python validation/main_driver.py
# choose 2
```

### Without Column Mapping

Infers destination columns automatically when mapping metadata is absent.
This mode is useful when source and destination schema names differ or when a manual mapping file is unavailable.

Example:

```bash
python validation/main_driver.py
# choose 3
```

## Project Structure

* `validation/`
  * `main_driver.py` - interactive controller
  * `mapped_columns/` - mapped-schema validation utilities
    * `file_read.py` - CSV/JSON/YAML loading and mapping validation
    * `basic_properties.py` - row count, duplicate, empty row, and type checks
    * `row_by_row_comparison.py` - primary-key row comparison logic
    * `full_validator.py` - end-to-end mapped dataset validation
    * `custom_validator.py` - filtered time-window validation
  * `unmapped_columns/` - heuristics-driven schema inference
    * `without_column_mapper.py` - automatic column matching utilities
* `src_data/` - sample datasets and configuration files
* `tests/` - unit tests covering validation behavior

## Test Suite

Run the test suite with:

```bash
pytest -q
```

The tests cover:

* file reading for CSV, JSON, and YAML
* column mapping validation
* basic dataset property checks
* row-by-row comparison mismatch detection
* unmapped column inference behavior

## Advantages

* architecture: clear separation of responsibilities between file I/O, validation rules, and comparison logic
* robustness: explicit drift checks for row count, duplicates, and mismatched columns
* flexibility: supports configuration and multiple validation workflows
* practical value: useful for data migration, ETL verification, and data quality monitoring

## Dependencies

* `pandas`
* `PyYAML`
* `pytest`

## Next polish opportunities

* add command-line arguments for file paths and validation modes
* convert print diagnostics to structured logging
* add more formal schema validation and type coercion rules
* include sample reports and failure summaries
