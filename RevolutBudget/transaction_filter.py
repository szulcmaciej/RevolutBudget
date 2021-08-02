import pandas as pd


def filter_exchanges(df):
    return df[df['Exchange Rate'].apply(lambda x: len(x) <= 1)]


def filter_incomes(df):
    return df[pd.isna(df['Paid In (EUR)'])]


def filter_cash(df):
    return df[df['Category'] != 'Gotówka']


def filter_transfers(df):
    return df[df['Category'] != 'Przelewy']
