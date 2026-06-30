import pandas as pd

from validation.mapped_columns.row_by_row_comparison import compare_row_multiprocess, RowByRowComparator


def test_compare_row_multiprocess_missing_destination():
    source_dict = {"key": {"A": 1}}
    dest_dict = {}

    result = compare_row_multiprocess(("key", source_dict, dest_dict, {"A": "a"}))

    assert result == [("key", "row", "missing in destination")]


def test_row_by_row_comparator_reports_mismatch(capsys):
    src_df = pd.DataFrame({"CLM_ID": [1], "A": [100]})
    dest_df = pd.DataFrame({"claim_id": [1], "a": [200]})

    comparator = RowByRowComparator(src_df, dest_df, {"A": "a"}, "CLM_ID", "claim_id")
    comparator.compare()
    captured = capsys.readouterr()

    assert "Mismatches found:" in captured.out
    assert "Source: A-100 , Destination: a-200" in captured.out
