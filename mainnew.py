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
#app.config['suppress_callback_exceptions']=True

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

    #print(dfLetters)
    #print(dfBigrams)
    #print(dfTrigrams)
    print(frequencies)
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

#Nie ogarniam, sam update działa, ale jak dodasz kod wcześniej to już nie
@app.callback(
    Output("output-graph", "figure"),
    [Input("input-dropdown", "value")])
def update(value):
    print("Value:"+value)
    print("Tmp:" + tmp)
    if value.strip() == tmp.strip():
        print("Prawda")
        return
    else:
        return {
            "data": [
                {"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar", "name": "SciFi"},
                {"x": [1, 2, 3], "y": [2, 4, 5], "type": "bar", "name": u"Aha"},
            ],
            "layout": {
                "title": "Zmieniony tytuł"
            }
        }

if __name__ == "__main__":
    app.run_server(debug=True)