import pandas as pd
import json

class FileReader:
    @staticmethod
    def read_csv(path, **kwargs):
        return pd.read_csv(path, **kwargs)

    @staticmethod
    def read_json(path):
        with open(path, 'r') as file:
            return json.load(file)
