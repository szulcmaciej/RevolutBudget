import pandas as pd
from abc import ABC, abstractmethod


class TransactionFilter(ABC):
    @abstractmethod
    def apply(self, transactions: pd.DataFrame) -> pd.DataFrame:
        pass


class NoExchangeFilter(TransactionFilter):
    def apply(self, transactions: pd.DataFrame) -> pd.DataFrame:
        return transactions[transactions['Exchange Rate'].apply(lambda x: pd.isna(x) or len(x.strip()) == 0)]


class NoIncomeFilter(TransactionFilter):
    def apply(self, transactions: pd.DataFrame) -> pd.DataFrame:
        return transactions[transactions['Paid In (EUR)'].apply(lambda x: pd.isna(x) or len(x.strip()) == 0)]


class NoCashFilter(TransactionFilter):
    def apply(self, transactions: pd.DataFrame) -> pd.DataFrame:
        return transactions[transactions['Category'] != 'Gotówka']


class NoTransfersFilter(TransactionFilter):
    def apply(self, transactions: pd.DataFrame) -> pd.DataFrame:
        return transactions[transactions['Category'] != 'Przelewy']
