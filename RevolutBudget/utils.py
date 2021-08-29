import base64
import io
from typing import List

import pandas as pd

from RevolutBudget.transaction_filters import NoTransfersFilter, NoExchangeFilter, NoCashFilter, NoIncomeFilter

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


def preprocess_transactions(transactions: pd.DataFrame) -> pd.DataFrame:
    filtered_transactions = filter_transactions(transactions)
    preprocessed_transactions = make_columns_numeric(filtered_transactions, ['Paid Out (EUR)'])
    preprocessed_transactions['datetime'] = pd.to_datetime(preprocessed_transactions['Completed Date'], format='%d.%m.%Y')
    preprocessed_transactions.sort_values('datetime', ascending=True, inplace=True)
    return preprocessed_transactions


def filter_transactions(transactions: pd.DataFrame) -> pd.DataFrame:
    filters = [
        NoTransfersFilter(),
        NoExchangeFilter(),
        NoCashFilter(),
        NoIncomeFilter()
    ]
    filtered_transactions = transactions.copy()
    for f in filters:
        filtered_transactions = f.apply(filtered_transactions)
    return filtered_transactions


def comma_separated_string_to_numeric(value):
    return pd.to_numeric('.'.join(value.strip().split(',')))


def make_columns_numeric(df, columns):
    for column in columns:
        df[column] = df[column].apply(comma_separated_string_to_numeric)
    return df