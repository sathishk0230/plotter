import io
import base64
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import os

external_stylesheets = ['assets/main.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True
colors = {
    'background': '#FFFFFF',
    'text': '#7FDBFF'
}

def get_numeric_cols(df):
    numeric_col = list()
    for col in df.columns:
        try:
            df[col]=pd.to_numeric(df[col])
            numeric_col.append(col)
        except:
            pass
    return numeric_col



app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Div(id='graph-div'),
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
        multiple=False
    )
    
])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return df

@app.callback(Output('graph-div', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),State('upload-data', 'last_modified')],
               prevent_initial_call=True)
def update_output(content, name, date):
    if content is not None:
        df = parse_contents(content,name,date)
        fig = px.line(df, x=df.columns[0], y=get_numeric_cols(df))
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        
        graph = dcc.Graph(
            id='dcc-graph',
            style={
                'width': '1500px',
                'height': '722px'
            },
            figure = fig
        )
        return graph
    print('exec////////')
    raise PreventUpdate
    # return None
if __name__ == '__main__':
    app.run_server(debug=True)