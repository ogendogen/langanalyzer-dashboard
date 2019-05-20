import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import json
import base64
import io
import datetime
import pandas as pd

import utils

#Przykładowy df do testów
df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'c78bf172206ce24f77d6363a2d754b59/raw/'
    'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
    'usa-agricultural-exports-2011.csv')


def show(df):
    app.layout = html.Div(children=[
        html.H4(children='Litery'),
        generate_table(df)
    ])


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children="Hello Dash"),

    html.Div(children="""
        Dash: A web application framework for Python.
    """),

    dcc.Graph(
        id="output-graph",
        figure={
            "data": [
                {"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar", "name": "SF"},
                {"x": [1, 2, 3], "y": [2, 4, 5], "type": "bar", "name": u"Montréal"},
            ],
            "layout": {
                "title": "Dash Data Visualization"
            }
        }
    ),

    html.Label("Choose language"),
    dcc.Dropdown(
        id="input-dropdown",
        options=[
            {"label": "English", "value": "english.json"},
            {"label": "Norwegian", "value": "norwegian.json"},
            {"label": "Russian", "value": "russian.json"},
            {"label": "Spanish", "value": "spanish.json"}
        ],
        value="english.json"
    ),

    html.A(html.Button('Przykładowy button'),
           href='https://google.com'),

    html.Div([html.Button('Wyświetl tabelę', id='button'),

              html.Div(children=[
                  html.Div(children='Występowanie liter'),
                  # Jakby tu dostać się do dfLetters i reszty to by było fajnie
                  generate_table(df)
              ])
              ])

])


@app.callback(
    Output("output-graph", "figure"),
    [Input("input-dropdown", "value")])
def update_figure(selectedFile):
    fileContent = utils.readAllText("analysis/" + selectedFile)
    jsonObject = json.loads(fileContent)

    lettersJson = jsonObject["letters"]
    bigramsJson = jsonObject["bigrams"]
    trigramsJson = jsonObject["trigrams"]

    dfLetters = pd.DataFrame(eval(lettersJson), index=[0])
    dfBigrams = pd.DataFrame(eval(bigramsJson), index=[0])
    dfTrigrams = pd.DataFrame(eval(trigramsJson), index=[0])

    # dcc.Link("Litery", show(dfLetters))

    print(dfLetters)
    print(dfBigrams)
    print(dfTrigrams)


if __name__ == "__main__":
    app.run_server(debug=True)
