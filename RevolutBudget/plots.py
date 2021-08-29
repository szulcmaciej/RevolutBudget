import plotly.express as px
import pandas as pd


def spending_by_category_plot(transactions: pd.DataFrame):
    return px.pie(transactions, values='Paid Out (EUR)', names='Category', title='Spending by category')


def spending_by_category_in_months_plot(transactions: pd.DataFrame):
    fig = px.bar(transactions,
                 x=transactions['datetime'].dt.to_period('M').astype(str),
                 y='Paid Out (EUR)',
                 color='Category',
                 custom_data=['Reference','Completed Date', 'Category']
                )
    fig.update_traces(hovertemplate='<b>%{customdata[0]}</b><br>Paid Out (EUR): %{y}<br>Date: %{customdata[1]}')
    return fig
