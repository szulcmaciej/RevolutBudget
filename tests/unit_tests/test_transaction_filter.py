import unittest
import pandas as pd

from RevolutBudget.transaction_filters import *


class TransactionFilterTest(unittest.TestCase):
    def setUp(self):
        test_data = {
            'Completed Date': ['19.02.2007', '12.12.2020', '14.06.2018', '14.11.2014'],
            'Reference': ['t1', 't2', 't3', 't4'],
            'Category': ['Ogólne', 'Gotówka', 'Przelewy', 'Transport']
        }
        self.df = pd.DataFrame(test_data)

    def test_remove_exchanges(self):
        # given
        self.df['Exchange Rate'] = pd.Series([None,
                                              ' ',
                                              'Kurs wymiany 1 € = 4,6276 zł	',
                                              'Kurs wymiany 1 $ = 4,02 zł	'])
        df_filter = NoExchangeFilter()
        expected_filtered_length = 2

        # when
        filtered = df_filter.apply(self.df)

        # then
        self.assertEqual(len(filtered), expected_filtered_length)

    def test_remove_incomes(self):
        # given
        self.df['Paid In (EUR)'] = pd.Series([None,
                                              ' ',
                                              '683.57',
                                              '24,67'])
        df_filter = NoIncomeFilter()
        expected_filtered_length = 2

        # when
        filtered = df_filter.apply(self.df)

        # then
        self.assertEqual(len(filtered), expected_filtered_length)

    def test_remove_cash(self):
        # given
        df_filter = NoCashFilter()
        expected_filtered_length = 3

        # when
        filtered = df_filter.apply(self.df)

        # then
        self.assertEqual(len(filtered), expected_filtered_length)

    def test_remove_transfers(self):
        # given
        df_filter = NoTransfersFilter()
        expected_filtered_length = 3

        # when
        filtered = df_filter.apply(self.df)

        # then
        self.assertEqual(len(filtered), expected_filtered_length)