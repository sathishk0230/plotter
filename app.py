import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

csv_file = None
for file in os.listdir('file'):
    if file[-4:]=='.csv':
        csv_file=file
        break
if csv_file!=None:
    df = pd.read_csv(os.path.join('file',csv_file))


numeric_col = list()
for col in df.columns:
    try:
        df[col]=pd.to_numeric(df[col])
        numeric_col.append(col)
    except:
        pass

fig = px.line(df, x=df.columns[0], y=numeric_col)

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
fig.update_layout(
    width = 1520,
    height = 700
)


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    dcc.Graph(
        id='example-graph-2',
        figure=fig
    )
    
])

if __name__ == '__main__':
    app.run_server(debug=True)