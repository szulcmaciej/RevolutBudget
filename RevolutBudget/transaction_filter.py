import pandas as pd


class TransactionFilter:
    @staticmethod
    def remove_exchanges(df):
        return df[df['Exchange Rate'].apply(lambda x: pd.isna(x) or len(x.strip()) == 0)]

    @staticmethod
    def remove_incomes(df):
        return df[df['Paid In (EUR)'].apply(lambda x: pd.isna(x) or len(x.strip()) == 0)]

    @staticmethod
    def remove_cash(df):
        return df[df['Category'] != 'Gotówka']

    @staticmethod
    def remove_transfers(df):
        return df[df['Category'] != 'Przelewy']
