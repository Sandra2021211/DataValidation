import pandas as pd

from validation.mapped_columns.basic_properties import BasicPropertiesValidator


def test_compare_row_count_match(capsys):
    src_df = pd.DataFrame({"CLM_ID": [1, 2], "value": [10, 20]})
    dest_df = pd.DataFrame({"claim_id": [1, 2], "value": [10, 20]})

    validator = BasicPropertiesValidator(src_df, dest_df, {})
    validator.compare_row_count()
    captured = capsys.readouterr()

    assert "Row counts match" in captured.out


def test_validate_data_types_detects_mismatch(capsys):
    src_df = pd.DataFrame({"A": [1, 2]})
    dest_df = pd.DataFrame({"a": ["1", "2"]})
    validator = BasicPropertiesValidator(src_df, dest_df, {"A": "a"})

    validator.validate_data_types()
    captured = capsys.readouterr()

    assert "Mismatch found:" in captured.out
    assert "A is of datatype int64" in captured.out


def test_check_duplicate_reports_duplicates(capsys):
    df = pd.DataFrame({"a": [1, 1, 2]})
    validator = BasicPropertiesValidator(df, df, {})

    validator.check_duplicate(df, "Test Dataset")
    captured = capsys.readouterr()

    assert "Duplicate rows found in Test Dataset" in captured.out


def test_check_empty_rows_reports_empty_rows(capsys):
    df = pd.DataFrame({"a": [None, "x"], "b": [None, None]})
    validator = BasicPropertiesValidator(df, df, {})

    validator.check_empty_rows(df, "Test Dataset")
    captured = capsys.readouterr()

    assert "Empty rows found in Test Dataset: 1" in captured.out
