import base64
from flask import Flask, send_from_directory
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import json
from urllib.parse import quote as urlquote
import utils
from collections import OrderedDict
import sys

# analyzer API
import apiAnalyzer

# sample call:
# print(apiAnalyzer.startAnalyzer("anksdajksdjknsadnjksandiuoqwjeiuojzskd"))

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=external_stylesheets)

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

# --------------------------file reader--------------------------
UPLOAD_DIRECTORY = "language-analyzer/text samples new"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


def save_file(name, content):
    data = content.encode("utf8").split(b";base64,")[1]
    with open(UPLOAD_DIRECTORY + "/" + name, "wb") as fp:
        fp.write(base64.decodebytes(data))

    apiAnalyzer.writeAllText("analysis/" + name[:-3] + "json",
                             apiAnalyzer.startAnalyzer(apiAnalyzer.readAllText(os.path.join(UPLOAD_DIRECTORY, name))))

    # List of options is not dynamic, requires page refresh
    options.insert(options.__sizeof__(), {"label": name[:-4], "value": name[:-3] + "json"})


@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)


def processAnalysis(data):
    print("todo")

options = []

def getOprions():
    filesList = os.listdir("analysis")
    for fileName in filesList:
        # reading files and adding to options list
        options.insert(options.__sizeof__(), {"label": fileName[:-5], "value": fileName})


getOprions()
app.layout = html.Div(children=[

    html.H1(children="Letters, bigrams and trigrams frequency analysis in different languages"),
    # html.Div(children="Projekt wykonany we frameworku Dash"),
    html.Div(" "),

    dcc.Tabs(id="maintabs", children=[
        # ------------------------------------MAIN TAB 1-----------------------------------------
        dcc.Tab(selected_style=tab_selected_style, label='Show results', children=[
            html.Div([
                html.Div(" "),
                html.Label("Select language to analyze"),
                dcc.Dropdown(
                    id="input-dropdown",
                    options=options,
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
                        ]),
                        dcc.Tab(selected_style=tab_selected_style, label='Letters', children=[
                            html.Div([
                                dcc.Graph(
                                    id='letters-graph2',
                                    figure={
                                        'data': [
                                            {'x': [1], 'y': [2]},
                                        ]
                                    }
                                )
                            ])
                        ]),
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
                        ),
                        dcc.Graph(
                            id='bigrams-graph2',
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
                        ),
                        dcc.Graph(
                            id='trirams-graph2',
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
        dcc.Tab(selected_style=tab_selected_style, label='Add a new analysis', children=[
            html.H2(" "),
            html.H2("Here you can upload .txt files to analyse"),
            dcc.Upload(
                id="upload-data",
                children=html.Div(
                    ["Drag and drop or click to select a file to upload."]
                ),
                style={
                    "width": "60%",
                    "height": "60px",
                    "lineHeight": "60px",
                    "borderWidth": "2px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "margin": "10px",
                    "fontSize": "1.4em",
                },
                multiple=True,
            ),
            html.H2("File List"),
            html.Ul(id="file-list"),
            html.Div([
                dcc.Graph(
                    id='letters-graph-tab2',
                    figure={
                        'data': [
                            {'x': [1], 'y': [2]},
                        ]
                    }
                )
            ]),
            html.Div([
                dcc.Graph(
                    id='bigrams-graph-tab2',
                    figure={
                        'data': [
                            {'x': [1], 'y': [2]},
                        ]
                    }
                )
            ]),
            html.Div([
                dcc.Graph(
                    id='trigrams-graph-tab2',
                    figure={
                        'data': [
                            {'x': [1], 'y': [2]},
                        ]
                    }
                )
            ])
        ]),
    ], style=tabs_styles),

])


# --------------------------LETTERS--------------------------
# --------------------------sorted---------------------------
@app.callback(
    Output("letters-graph", "figure"),
    [Input("input-dropdown", "value")])
def update_figure(selectedFile):
    fileContent = utils.readAllText("analysis/" + selectedFile)
    jsonObject = json.loads(fileContent)

    lettersJson = eval(str(jsonObject["letters"]))
    sort = OrderedDict(sorted(lettersJson.items(), key=lambda item: item[1], reverse=True))

    literals = list(sort.keys())
    freq = list(sort.values())

    figure = []
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


# --------------------------alphabetical--------------------------
@app.callback(
    Output("letters-graph2", "figure"),
    [Input("input-dropdown", "value")])
def update_figure(selectedFile):
    fileContent = utils.readAllText("analysis/" + selectedFile)
    jsonObject = json.loads(fileContent)

    lettersJson = eval(str(jsonObject["letters"]))
    alphabetical = OrderedDict(sorted(lettersJson.items(), key=lambda item: item[0]))

    literals = list(alphabetical.keys())
    freq = list(alphabetical.values())

    figure = []
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
# --------------------------sorted--------------------------
@app.callback(
    Output("bigrams-graph", "figure"),
    [Input("input-dropdown", "value")])
def update_figure(selectedFile):
    fileContent = utils.readAllText("analysis/" + selectedFile)
    jsonObject = json.loads(fileContent)

    try:
        bigramsJson = eval(str(jsonObject["bigrams"]))
    except TypeError:
        bigramsJson = eval(str(jsonObject["digrams"]))
    except KeyError:
        bigramsJson = eval(str(jsonObject["digrams"]))

    sort = OrderedDict(sorted(bigramsJson.items(), key=lambda item: item[1], reverse=True))
    alphabetical = OrderedDict(sorted(bigramsJson.items(), key=lambda item: item[0]))
    literals = list(sort.keys())
    freq = list(sort.values())
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


# --------------------------alphabetical--------------------------
@app.callback(
    Output("bigrams-graph2", "figure"),
    [Input("input-dropdown", "value")])
def update_figure(selectedFile):
    fileContent = utils.readAllText("analysis/" + selectedFile)
    jsonObject = json.loads(fileContent)

    try:
        bigramsJson = eval(str(jsonObject["bigrams"]))
    except TypeError:
        bigramsJson = eval(str(jsonObject["digrams"]))
    except KeyError:
        bigramsJson = eval(str(jsonObject["digrams"]))

    alphabetical = OrderedDict(sorted(bigramsJson.items(), key=lambda item: item[0]))
    literals = list(alphabetical.keys())
    freq = list(alphabetical.values())
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
# --------------------------sorted--------------------------
@app.callback(
    Output("trirams-graph", "figure"),
    [Input("input-dropdown", "value")])
def update_figure(selectedFile):
    fileContent = utils.readAllText("analysis/" + selectedFile)
    jsonObject = json.loads(fileContent)

    trigramsJson = eval(str(jsonObject["trigrams"]))
    sort = OrderedDict(sorted(trigramsJson.items(), key=lambda item: item[1], reverse=True))

    literals = list(sort.keys())
    freq = list(sort.values())
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


# --------------------------alphabetical--------------------------
@app.callback(
    Output("trirams-graph2", "figure"),
    [Input("input-dropdown", "value")])
def update_figure(selectedFile):
    fileContent = utils.readAllText("analysis/" + selectedFile)
    jsonObject = json.loads(fileContent)

    trigramsJson = eval(str(jsonObject["trigrams"]))
    alphabetical = OrderedDict(sorted(trigramsJson.items(), key=lambda item: item[0]))

    literals = list(alphabetical.keys())
    freq = list(alphabetical.values())
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


# --------------------------FILE READER--------------------------
@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            if ".txt" not in name:
                return [html.Li("Not a txt file! But I'll try my best anyway...")]
            save_file(name, data)

    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]

# ---------------------- FILE READER FOR ANALYSIS: LETTERS ---------------------------
@app.callback(
    Output("letters-graph-tab2", "figure"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):

    if uploaded_file_contents is None:
        exit()

    analysisResult = apiAnalyzer.startAnalyzer(uploaded_file_contents)
    jsonObject = json.loads(analysisResult)

    lettersJson = eval(str(jsonObject["letters"]))
    sort = OrderedDict(sorted(lettersJson.items(), key=lambda item: item[1], reverse=True))

    literals = list(sort.keys())
    freq = list(sort.values())

    figure = []
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

# ----------------------- FILE READER FOR ANALYSIS: BIGRAMS ----------------------
@app.callback(
    Output("bigrams-graph-tab2", "figure"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):

    if uploaded_file_contents is None:
        exit()

    analysisResult = apiAnalyzer.startAnalyzer(uploaded_file_contents)
    jsonObject = json.loads(analysisResult)

    lettersJson = eval(str(jsonObject["bigrams"]))
    sort = OrderedDict(sorted(lettersJson.items(), key=lambda item: item[1], reverse=True))

    literals = list(sort.keys())
    freq = list(sort.values())

    figure = []
    figure.append(go.Scatter(
        x=literals,
        y=freq,
        name="Bigram frequency",
        text="The exact value of occurrences of selected bigram",
    ))

    return {
        "data": figure,
        'layout': go.Layout(
            xaxis={'title': 'Bigram'},
            yaxis={'title': 'Proportions of occurrences'},  # 'range': [0, 0.2]
        )
    }

# ----------------------- FILE READER FOR ANALYSIS: TRIGRAMS ----------------------
@app.callback(
    Output("trigrams-graph-tab2", "figure"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):

    if uploaded_file_contents is None:
        exit()

    analysisResult = apiAnalyzer.startAnalyzer(uploaded_file_contents)
    jsonObject = json.loads(analysisResult)

    lettersJson = eval(str(jsonObject["trigrams"]))
    sort = OrderedDict(sorted(lettersJson.items(), key=lambda item: item[1], reverse=True))

    literals = list(sort.keys())
    freq = list(sort.values())

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
