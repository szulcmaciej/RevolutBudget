import pandas as pd

import dash
from dash import no_update
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from RevolutBudget.plots import spending_by_category_plot, spending_by_category_in_months_plot
from RevolutBudget.utils import load_uploaded_transactions, preprocess_transactions


class RevolutBudgetDashApp:
    def __init__(self):
        self.external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        self.dash_app = dash.Dash(__name__, external_stylesheets=self.external_stylesheets)
        self.transactions = pd.DataFrame()
        self.set_app_layout()
        self.set_callbacks()

    def run(self):
        self.dash_app.run_server(debug=True)

    def set_app_layout(self):
        self.dash_app.layout = html.Div([
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            html.Div(id='output-data-upload'),
            html.Div(id='plots')
        ])

    def plots_objects(self):
        preprocessed_transactions = preprocess_transactions(self.transactions)
        return [
            dcc.Graph(id='spending_by_category_plot', figure=spending_by_category_plot(preprocessed_transactions)),
            dcc.Graph(id='spending_by_category_in_months_plot', figure=spending_by_category_in_months_plot(preprocessed_transactions))
        ]

    def set_callbacks(self):
        @self.dash_app.callback(Output('output-data-upload', 'children'),
                                Output('plots', 'children'),
                                Input('upload-data', 'contents'),
                                State('upload-data', 'filename'))
        def load_transactions_from_csv_files(list_of_contents, list_of_names):
            if list_of_contents is not None:
                try:
                    self.transactions = load_uploaded_transactions(list_of_contents, list_of_names)
                    message = f'Successfully loaded {len(self.transactions)} transactions' \
                              f' from {len(list_of_contents)} files'
                    self.set_app_layout()
                except Exception as e:
                    message = f'ERROR: {e}'
                return html.P(message), self.plots_objects()
            else:
                return no_update, no_update


if __name__ == '__main__':
    app = RevolutBudgetDashApp()
    app.run()
