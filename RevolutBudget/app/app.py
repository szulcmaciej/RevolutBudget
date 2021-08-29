import base64
import datetime
import io

import dash_table
import pandas as pd

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html


class RevolutBudgetDashApp:
    def __init__(self):
        self.external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        self.dash_app = dash.Dash(__name__, external_stylesheets=self.external_stylesheets)
        self.set_app_layout()
        self.set_callbacks()
        self.transactions = pd.DataFrame()

    def run(self):
        self.dash_app.run_server()

    @staticmethod
    def parse_uploaded_csv_to_dataframe(contents, filename, date) -> pd.DataFrame:
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        if '.csv' in filename:
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), sep=';')
        else:
            raise ValueError("File uploaded is not CSV")

        return df

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
            html.Div(id='plots',
                     children=[

                     ])
        ])

    def set_callbacks(self):
        @self.dash_app.callback(Output('output-data-upload', 'children'),
                                Input('upload-data', 'contents'),
                                State('upload-data', 'filename'),
                                State('upload-data', 'last_modified'))
        def update_output(list_of_contents, list_of_names, list_of_dates):
            if list_of_contents is not None:
                try:
                    transactions_split_by_file = [
                        self.parse_uploaded_csv_to_dataframe(c, n, d) for c, n, d in
                        zip(list_of_contents, list_of_names, list_of_dates)]
                    all_transactions = pd.concat(transactions_split_by_file)
                    self.transactions = all_transactions
                    message = f'Loaded {len(all_transactions)} transactions'
                except Exception as e:
                    message = f'ERROR: {e}'
                return html.P(message)


if __name__ == '__main__':
    app = RevolutBudgetDashApp()
    app.run()
