import pandas as pd

from validation.unmapped_columns.without_column_mapper import WithoutColumnMapping


def test_without_column_mapping_infers_column_pairs(tmp_path):
    src_file = tmp_path / "src.csv"
    dest_file = tmp_path / "dest.csv"

    src_file.write_text("CLM_ID,A,B\n1,foo,10\n2,bar,20\n")
    dest_file.write_text("claim_id,a,b\n1,foo,10\n2,bar,20\n")

    mapper = WithoutColumnMapping(str(src_file), str(dest_file), "CLM_ID", "claim_id")
    mapper.run()

    assert mapper.mapping["A"] == "a"
    assert mapper.mapping["B"] == "b"
