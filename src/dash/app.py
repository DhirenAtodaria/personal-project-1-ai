import os

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import config
import requests
import base64

external_stylesheets = [
    "https://use.fontawesome.com/releases/v5.0.7/css/all.css",
    'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
    'https://fonts.googleapis.com/css?family=Roboto&display=swap'
]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
    suppress_callback_exceptions=True
)

app.title = 'DA Food AI Project'

app.layout = html.Div([
    html.Div(children=[
        html.H1(children='Hello', style={'text-align': 'center'}),
        html.Div(children='''
            This is a web-app designed to accept food images and return a prediction on what the item is.
        ''', style={'text-align': 'center'}),
        html.Div(children='''
            The app is created using Python Flask for the API framework, Dash for the front-end and a transfer-learning approach to training the model in PyTorch.
        ''', style={'text-align': 'center', 'margin-bottom': '20px'})], style={'border-bottom': '1px solid black'}),

    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': 'auto',
            'margin-top': '100px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),

    html.Div(children=[
        html.Div(children=[
            html.Div(id='output-image-upload', style={'width': '20%'}),
            html.Div(id='calorieinfo')
        ], style={'width': '100vw', 'height': '30vh', 'display': 'flex', 'justify-content': 'space-around', 'align-items': 'center'}),
        html.Span(id='foodpred')
    ], style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'space-evenly', 'align-items': 'center', 'height': '50vh'})
])


def parse_contents(contents):
    return html.Div(
        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents, style={'width': '100%', 'height': '100%', 'object-fit': 'cover'})
    )


def parse_calorie_info(info):
    return dash_table.DataTable(
        id='table',
        columns=[{"name": 'Calories (100g)', "id": 'Calories (100g)'}, {"name": 'Fats', "id": 'Fats'},
                 {"name": 'Carbs', "id": 'Carbs'}, {"name": 'Protein', "id": 'Protein'}],
        data=info,
        style_cell={'textAlign': 'left', 'width': '150px'}
    )


@app.callback(Output('output-image-upload', 'children'),
              [Input('upload-image', 'contents')])
def update_output(list_contents):
    if list_contents is not None:
        children = parse_contents(list_contents)
        return children


@app.callback(Output('foodpred', 'children'),
              [Input('upload-image', 'contents')])
def food_predict(fooditem):
    if fooditem is not None:
        content_string = fooditem.split(',')
        bytesimage = base64.b64decode(content_string[1])
        response = requests.post(f"{config.API_URL}/predict", files={'file': bytesimage})
        prediction = response.json()['food_name']
        foodnamedic = f'The AI predicts your food name is {prediction}'
        return foodnamedic


@app.callback(Output('calorieinfo', 'children'),
              [Input('foodpred', 'children')])
def macro_retrival(predictname):
    if predictname is not None:
        foodname = predictname.split('is ')[1]
        response = requests.post(f"{config.API_URL}/macros", data={'name': foodname})
        value = response.json()
        info = [value]
        return parse_calorie_info(info)


if __name__ == '__main__':
    app.run_server(debug=config.DEBUG, host=config.HOST)
