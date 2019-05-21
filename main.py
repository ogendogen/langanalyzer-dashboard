import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import json
# import pandas as pd
import utils

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    html.H1(children="Analiza występowania znaków w różnych językach"),
    # html.Div(children="Projekt wykonany we frameworku Dash"),

    html.Label("Wybierz język do analizy"),
    dcc.Dropdown(
        id="input-dropdown",
        options=[
            {"label": "English", "value": "english.json"},
            {"label": "English 2", "value": "english2.json"},
            {"label": "Finnish", "value": "finnish.json"},
            {"label": "Norwegian", "value": "norwegian.json"},
            {"label": "Norwegian 2", "value": "norwegian2.json"},
            {"label": "Polish", "value": "polish.json"},
            {"label": "Russian", "value": "russian.json"},
            {"label": "Spanish", "value": "spanish.json"}
        ],
        value="english.json"
    ),

    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Litery', children=[
            html.Div([
                dcc.Graph(
                    id='letters-graph',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2],
                             'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 4, 5],
                             'type': 'bar', 'name': u'Montréal'},
                        ]
                    }
                )
            ])
        ]),
        dcc.Tab(label='Bigramy', children=[
            dcc.Graph(
                id='bigrams-graph',
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [1, 4, 1],
                         'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [1, 2, 3],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ]),
        dcc.Tab(label='Trigramy', children=[
            dcc.Graph(
                id='trirams-graph',
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [2, 4, 3],
                         'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [5, 4, 3],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ]),
    ])

])


# --------------------------LETTERS--------------------------
@app.callback(
    Output("letters-graph", "figure"),
    [Input("input-dropdown", "value")])
def update_figure(selectedFile):
    fileContent = utils.readAllText("analysis/" + selectedFile)
    jsonObject = json.loads(fileContent)

    lettersJson = eval(jsonObject["letters"])

    # print(eval(lettersJson))
    literals = list(lettersJson.keys())
    freq = list(lettersJson.values())

    # for key, value in lettersJson.iterItems():
    #     literals.append(key)
    #     freq.append(value)
    # print(literals)
    # print(freq)

    figure = []
    # data = dfLetters.to_dict("records")
    # print(data)
    # for i in lettersJson:
    figure.append(go.Scatter(
        x=literals,
        y=freq,
        name="Występowanie liter",
        text="Dokładna wartość wystąpień zaznaczonego znaku"
    ))

    return {
        "data": figure,
        'layout': go.Layout(
            xaxis={'title': 'Litera'},
            yaxis={'title': 'Odsetek wystąpień'},  # 'range': [0, 0.2]
        )
    }


# --------------------------BIGRAMS--------------------------
@app.callback(
    Output("bigrams-graph", "figure"),
    [Input("input-dropdown", "value")])
def update_figure(selectedFile):
    fileContent = utils.readAllText("analysis/" + selectedFile)
    jsonObject = json.loads(fileContent)

    try:
        bigramsJson = eval(jsonObject["bigrams"])
    except TypeError:
        bigramsJson = eval(jsonObject["digrams"])

    literals = list(bigramsJson.keys())
    freq = list(bigramsJson.values())
    figure = []
    figure.append(go.Scatter(
        x=literals,
        y=freq,
        name="Występowanie bigraów",
        text="Dokładna wartość wystąpień zaznaczonego bigramu"
    ))
    return {
        "data": figure,
        'layout': go.Layout(
            xaxis={'title': 'Bigram'},
            yaxis={'title': 'Odsetek wystąpień'},  # 'range': [0, 0.2]
        )
    }


# --------------------------TRIGRAMS--------------------------
@app.callback(
    Output("trirams-graph", "figure"),
    [Input("input-dropdown", "value")])
def update_figure(selectedFile):
    fileContent = utils.readAllText("analysis/" + selectedFile)
    jsonObject = json.loads(fileContent)

    trigramsJson = eval(jsonObject["trigrams"])

    literals = list(trigramsJson.keys())
    freq = list(trigramsJson.values())
    figure = []
    figure.append(go.Scatter(
        x=literals,
        y=freq,
        name="Występowanie triraów",
        text="Dokładna wartość wystąpień zaznaczonego triramu",
    ))
    return {
        "data": figure,
        'layout': go.Layout(
            xaxis={'title': 'Trigram', 'type': 'category'},
            yaxis={'title': 'Odsetek wystąpień'},  # 'range': [0, 0.2]
        )
    }


if __name__ == "__main__":
    app.run_server(debug=True)
