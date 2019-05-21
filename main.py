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

tabs_styles = {
    # 'height': '244px'
    'fontWeight': 'bold',
    'fontSize': '1.8em',
}

tabs_styles2 = {
    # 'height': '244px'
    'fontWeight': 'bold',
    'fontSize': '1.2em',
}

tab_selected_style = {
    # 'borderTop': '1px solid #d6d6d6',
    # 'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#72c5ff',
    # 'color': 'white',
    # 'padding': '6px'
}

list_style = {
    # 'borderTop': '2px solid #d6d6d6',
    # 'borderBottom': '2px solid #d6d6d6',
    # 'backgroundColor': '#72c5ff',
    # 'color': 'white',
    # 'padding': '6px',
    'fontWeight': 'bold',
    'fontSize': '1.2em'
}

app.layout = html.Div(children=[

    html.H1(children="Letters, bigrams and trigrams frequency analysis in different languages"),
    # html.Div(children="Projekt wykonany we frameworku Dash"),
    html.Div(" "),

    dcc.Tabs(id="maintabs", children=[
        # ------------------------------------MAIN TAB 1-----------------------------------------
        dcc.Tab(selected_style=tab_selected_style, label='Show exemplary results', children=[
            html.Div([
                html.Div(" "),
                html.Label("Select language to analyze"),
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
                    value="english.json", style=list_style
                ),
                html.Div(" "),
                dcc.Tabs(id="tabs", children=[
                    # -------------------------------LETTERS TAB------------------------------------
                    dcc.Tab(selected_style=tab_selected_style, label='Letters', children=[
                        html.Div([
                            dcc.Graph(
                                id='letters-graph',
                                figure={
                                    'data': [
                                        {'x': [1], 'y': [2]},
                                    ]
                                }
                            )
                        ])
                    ]),
                    # -------------------------------BIGRAMS TAB------------------------------------
                    dcc.Tab(selected_style=tab_selected_style, label='Bigrams', children=[
                        dcc.Graph(
                            id='bigrams-graph',
                            figure={
                                'data': [
                                    {'x': [1], 'y': [2]},
                                ]
                            }
                        )
                    ]),
                    # -------------------------------TRIGRAMS TAB------------------------------------
                    dcc.Tab(selected_style=tab_selected_style, label='Trigrams', children=[
                        dcc.Graph(
                            id='trirams-graph',
                            figure={
                                'data': [
                                    {'x': [1], 'y': [2]},
                                ]
                            }
                        )
                    ]),
                ], style=tabs_styles2)
            ])
        ]),
        # ------------------------------------MAIN TAB 2-----------------------------------------
        dcc.Tab(selected_style=tab_selected_style, label='Run a new analysis', children=[
            dcc.Graph(
                id='example-graph-1',
                figure={
                    'data': [
                        {'x': [1], 'y': [2]},
                    ]
                }
            )
        ]),
    ], style=tabs_styles),

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
        name="Letter frequency",
        text="The exact value of occurrences of selected character",
    ))

    return {
        "data": figure,
        'layout': go.Layout(
            xaxis={'title': 'Letter'},
            yaxis={'title': 'Proportions of occurrences'},  # 'range': [0, 0.2]
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
        name="Bigrams frequency",
        text="The exact value of occurrences of selected bigram"
    ))
    return {
        "data": figure,
        'layout': go.Layout(
            xaxis={'title': 'Bigram'},
            yaxis={'title': 'Proportions of occurrences'},  # 'range': [0, 0.2]
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
        name="Trigram frequency",
        text="The exact value of occurrences of selected trigram",
    ))
    return {
        "data": figure,
        'layout': go.Layout(
            xaxis={'title': 'Trigram'},
            yaxis={'title': 'Proportions of occurrences'},  # 'range': [0, 0.2]
        )
    }


if __name__ == "__main__":
    app.run_server(debug=True)
