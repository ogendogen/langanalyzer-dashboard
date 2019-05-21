import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import json
import pandas as pd
import utils

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app.config['suppress_callback_exceptions']=True

global tmp
tmp = "english.json"


def update_figure(selectedFile):
    fileContent = utils.readAllText("analysis/" + selectedFile)
    jsonObject = json.loads(fileContent)

    lettersJson = jsonObject["letters"]
    bigramsJson = jsonObject["bigrams"]
    trigramsJson = jsonObject["trigrams"]

    dfLetters = pd.DataFrame(eval(lettersJson), index=[0])
    dfBigrams = pd.DataFrame(eval(bigramsJson), index=[0])
    dfTrigrams = pd.DataFrame(eval(trigramsJson), index=[0])

    frequencies = []
    frequencies.append(dfLetters)
    frequencies.append(dfBigrams)
    frequencies.append(dfTrigrams)

    # print(dfLetters)
    # print(dfBigrams)
    # print(dfTrigrams)
    # print(frequencies)
    return frequencies


app.layout = html.Div(children=[
    html.H1(children="Analiza występowania znaków w różnych językach"),

    html.Div(children="""
        Projekt wykonany we frameworku Dash
    """),

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
    )
])


# Nie ogarniam, sam update działa, ale jak dodasz kod wcześniej to już nie
@app.callback(
    Output("output-graph", "figure"),
    [Input("input-dropdown", "value")])
def update(value):
    print("Value:" + value)
    print("Tmp:" + tmp)
    if value.strip() != tmp.strip():
        print("Fałsz")
        return {
            "data": [
                {"x": ['e', 't', 'a', 'o', 'i', 'h', 'n', 's', 'r', 'd', 'l', 'u', 'c', 'w', 'g', 'f', 'm', 'p', 'y',
                       'b', 'k', 'v', 'x', 'j', 'z', 'q'],
                 "y": [0.12052069, 0.09633176, 0.08231715, 0.07262911, 0.06862672,
                       0.0674048, 0.06644473, 0.05728037, 0.05436273, 0.05042268,
                       0.04310366, 0.02780479, 0.02501185, 0.02369018, 0.02276751,
                       0.02258048, 0.02100945, 0.01910177, 0.01840353, 0.01643351,
                       0.01172041, 0.00746864, 0.00170819, 0.00115957, 0.00096008,
                       0.00073564], "type": "bar", "name": "SciFi"},
            ],
            "layout": {
                "title": "Zmieniony tytuł fałsz"
            }
        }
    else:
        # print("Kolumny: "+str(list(update_figure(value)[0].columns)))
        # print("Wartości:" + str(list(update_figure(value)[0].values)))
        col = str(list(update_figure(value)[0].columns))
        val = str(list(update_figure(value)[0].values))
        print("Wartości poprawione:" + val[7:-2])
        print("Kolumny:" + col)

        return {
            "data": [
                {"x": col, "y": val[7:-2], "type": "bar", "name": "SciFi"},
            ],
            "layout": {
                "title": "Zmieniony tytuł prawda"
            }
        }


if __name__ == "__main__":
    app.run_server(debug=True)
