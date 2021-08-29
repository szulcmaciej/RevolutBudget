import plotly.express as px
import pandas as pd


def spending_by_category_plot(transactions: pd.DataFrame):
    return px.pie(transactions, values='Paid Out (EUR)', names='Category', title='Spending by category')


def spending_by_category_in_months_plot(transactions: pd.DataFrame):
    # TODO make the plot bigger (fullscreen?)
    return px.bar(transactions,
                  x=transactions['Completed Date'].dt.to_period('M').astype(str),
                  y='Paid Out (EUR)',
                  color='Category',
                  title='Spending by category in months')
