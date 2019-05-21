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

# Przykładowy df dla tabeli
# df = pd.read_csv(
#     'https://gist.githubusercontent.com/chriddyp/'
#     'c78bf172206ce24f77d6363a2d754b59/raw/'
#     'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
#     'usa-agricultural-exports-2011.csv')
# # Przykładowy df dla grafu
# df2 = pd.read_csv(
#     'https://gist.githubusercontent.com/chriddyp/' +
#     '5d1ea79569ed194d432e56108a04d188/raw/' +
#     'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
#     'gdp-life-exp-2007.csv')

# def show(df):
#     app.layout = html.Div(children=[
#         html.H4(children='Litery'),
#         generate_table(df)
#     ])


# def generate_table(dataframe, max_rows=10):
#     return html.Table(
#         # Header
#         [html.Tr([html.Th(col) for col in dataframe.columns])] +

#         # Body
#         [html.Tr([
#             html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#         ]) for i in range(min(len(dataframe), max_rows))]
#     )


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children="Analiza występowania znaków w różnych językach"),

    html.Div(children="""
        Projekt wykonany we frameworku Dash
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


    # dcc.Graph(
    #     id='life-exp-vs-gdp',
    #     figure={
    #         'data': [
    #             go.Scatter(
    #                 x=df2[df2['continent'] == i]['gdp per capita'],
    #                 y=df2[df2['continent'] == i]['life expectancy'],
    #                 text=df2[df2['continent'] == i]['country'],
    #                 mode='markers',
    #                 opacity=0.7,
    #                 marker={
    #                     'size': 15,
    #                     'line': {'width': 0.5, 'color': 'white'}
    #                 },
    #                 name=i
    #             ) for i in df2.continent.unique()
    #         ],
    #         'layout': go.Layout(
    #             xaxis={'type': 'log', 'title': 'GDP Per Capita'},
    #             yaxis={'title': 'Life Expectancy'},
    #             margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
    #             legend={'x': 0, 'y': 1},
    #             hovermode='closest'
    #         )
    #     }
    # ),

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

    # button nic nie robi, trzeba dodać kolejne @app.callback - tylko, że się sypie
    html.Div([html.Button('Wyświetl tabelę', id='button'),

              html.Div(children=[
                  html.Div(children='Występowanie liter'),
                  # Jakby tu dostać się do dfLetters i reszty to by było fajnie
                #   generate_table(df)
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
    #print(dfBigrams)
    #print(dfTrigrams)

    figure = []
    data = dfLetters.to_dict("records")
    for i in lettersJson:
        figure.append(go.Scatter(
            x = data,
            y = data,
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
        ))
    
    return {
        "data": figure,
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'GDP Per Capita'},
            yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == "__main__":
    app.run_server(debug=True)
