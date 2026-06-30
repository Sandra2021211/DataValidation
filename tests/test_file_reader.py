import json
import yaml

from validation.mapped_columns.file_read import FileReader


def test_read_csv(tmp_path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("a,b\n1,2\n3,4\n")

    df = FileReader.read_csv(str(csv_path))

    assert df.shape == (2, 2)
    assert list(df.columns) == ["a", "b"]
    assert df["a"].tolist() == [1, 3]


def test_read_json(tmp_path):
    data = {"hello": "world"}
    json_path = tmp_path / "sample.json"
    json_path.write_text(json.dumps(data))

    result = FileReader.read_json(str(json_path))

    assert result == data


def test_read_yaml(tmp_path):
    data = {"validation_config": {"date_filter": {"start_date": "2025-01-01"}}}
    yaml_path = tmp_path / "sample.yaml"
    yaml_path.write_text(yaml.safe_dump(data))

    result = FileReader.read_yaml(str(yaml_path))

    assert result["validation_config"]["date_filter"]["start_date"] == "2025-01-01"
