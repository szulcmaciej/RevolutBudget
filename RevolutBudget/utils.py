from typing import List

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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


def comma_separated_string_to_numeric(value):
    return pd.to_numeric('.'.join(value.strip().split(',')))

# def filter_revolut_data(''):