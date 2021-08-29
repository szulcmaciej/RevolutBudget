import base64
import io
from typing import List

import pandas as pd

source_files = ['/Users/maciek/Downloads/Revolut-EUR-Maciek.csv',
                '/Users/maciek/Downloads/Revolut-EUR-Ewa.csv']


def read_revolut_data(source_files: List):
    df = None
    for file in source_files:
        part_df = pd.read_csv(file, sep=';')
        if df is None:
            df = part_df
        else:
            df.append(part_df)
    return df


def parse_uploaded_csv_to_dataframe(contents, filename) -> pd.DataFrame:
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    if '.csv' in filename:
        df = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')), sep=';')
    else:
        raise ValueError("File uploaded is not CSV")

    return df


def load_uploaded_transactions(list_of_contents, list_of_names):
    transactions_split_by_file = \
        [parse_uploaded_csv_to_dataframe(c, n) for c, n in zip(list_of_contents, list_of_names)]
    all_transactions = pd.concat(transactions_split_by_file)
    return all_transactions


def comma_separated_string_to_numeric(value):
    return pd.to_numeric('.'.join(value.strip().split(',')))
