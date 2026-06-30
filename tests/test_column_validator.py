import pandas as pd

from validation.mapped_columns.file_read import ColumnValidator


def test_validate_column_mapping_all_mapped(capsys):
    source_df = pd.DataFrame(columns=["A", "B"])
    dest_df = pd.DataFrame(columns=["a", "b"])
    mapping = {"A": "a", "B": "b"}

    ColumnValidator.validate_column_mapping(source_df, dest_df, mapping)
    captured = capsys.readouterr()

    assert "All destination columns are correctly mapped." in captured.out


def test_validate_column_mapping_detects_unmapped(capsys):
    source_df = pd.DataFrame(columns=["A"])
    dest_df = pd.DataFrame(columns=["a", "b"])
    mapping = {"A": "a"}

    ColumnValidator.validate_column_mapping(source_df, dest_df, mapping)
    captured = capsys.readouterr()

    assert "Unmapped destination columns found:" in captured.out
    assert "b" in captured.out
